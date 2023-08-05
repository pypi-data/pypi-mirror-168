"""
    MastodonAmnesia - deletes old Mastodon toots
    Copyright (C) 2021  Mark S Burgunder

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import argparse
import asyncio
import logging
import sys
from math import ceil
from typing import Any
from typing import cast
from typing import Dict
from typing import Optional
from typing import Tuple

import aiohttp
import arrow
from aiohttp.client_exceptions import ClientError
from minimal_activitypub.client_2_server import ActivityPub
from minimal_activitypub.client_2_server import ActivityPubError
from minimal_activitypub.client_2_server import RatelimitError
from outdated import check_outdated
from rich import print  # pylint: disable=redefined-builtin
from rich import traceback
from tqdm import tqdm
from tqdm import trange

from . import __display_name__
from . import __package_name__
from . import __version__
from .control import Configuration


traceback.install(show_locals=True)
logger = logging.getLogger(__display_name__)
logger.setLevel(logging.DEBUG)


async def main() -> None:  # noqa: max-complexity: 13
    """Main logic to run MastodonAmnesia."""

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    dry_run, config = await setup_shop()

    now = arrow.now()
    oldest_to_keep = now.shift(seconds=-config.bot.delete_after)

    print(f"Welcome to {__display_name__} {__version__}")
    logger.debug("main -Welcome to %s %s", __display_name__, __version__)

    check_updates()

    try:
        session = aiohttp.ClientSession()

        instance = ActivityPub(
            instance=config.mastodon.instance,
            access_token=config.mastodon.access_token,
            session=session,
        )
        await instance.determine_instance_type()
        user_info = await instance.verify_credentials()
        account_id = user_info["id"]
        user_name = user_info["username"]
        print(
            f"We are removing toots older than {oldest_to_keep} "
            f"from {config.mastodon.instance}@{user_name}"
        )

        toots = await instance.get_account_statuses(account_id=account_id)
    except RatelimitError:
        print(
            f"RateLimited during startup, [red]Please wait until[/red] "
            f"{instance.ratelimit_reset} before trying again"
        )
        sys.exit(429)
    except (ClientError, ActivityPubError):
        logger.exception("!!! Cannot continue.")
        sys.exit(100)

    toots_to_delete = []
    title = "Finding toots to delete"
    progress_bar = tqdm(
        desc=f"{title:.<60}",
        ncols=120,
        unit="toots",
        position=0,
        bar_format="{l_bar} {n_fmt} at {rate_fmt}",
    )
    while True:
        try:
            for toot in toots:
                logger.debug(
                    "Processing toot: %s from %s",
                    toot.get("url"),
                    toot.get("created_at"),
                )

                logger.debug(
                    "Oldest to keep vs toot created at %s > %s",
                    oldest_to_keep,
                    toot.get("created_at"),
                )

                if should_keep(
                    toot=toot,
                    oldest_to_keep=oldest_to_keep,
                    config=config,
                ):
                    logger.info(
                        "Not deleting toot: "
                        "Bookmarked: %s - "
                        "My Fav: %s - "
                        "Pinned: %s - "
                        "Poll: %s - "
                        "Attachements: %s - "
                        "Faved: %s - "
                        "Boosted: %s - "
                        "DM: %s -+- "
                        "Created At: %s -+- "
                        "%s",
                        toot.get("bookmarked"),
                        toot.get("favourited"),
                        toot.get("pinned"),
                        (toot.get("poll") is not None),
                        len(toot.get("media_attachments")),
                        toot.get("favourites_count"),
                        toot.get("reblogs_count"),
                        (toot.get("visibility") == "direct"),
                        toot.get("created_at"),
                        toot.get("url"),
                    )

                else:
                    toots_to_delete.append(toot)

                progress_bar.update()

            # Get More toots if available:
            if instance.pagination_max_id:
                toots = await instance.get_account_statuses(
                    account_id=account_id, max_id=instance.pagination_max_id
                )
                if len(toots) == 0:
                    break
            else:
                break

        except RatelimitError:
            await sleep_off_ratelimiting(instance=instance)

    progress_bar.close()

    total_toots_to_delete = len(toots_to_delete)

    # If dry-run has been specified, print out list of toots that would be deleted
    if dry_run:
        print("\n--dry-run or -d specified. [yellow][bold]No toots will be deleted")
        for toot in toots_to_delete:
            print(
                f"[red]Would[/red] delete toot"
                f" {toot.get('url')} from {toot.get('created_at')}"
            )
        print(f"Total of {total_toots_to_delete} toots would be deleted.")

    # Dry-run has not been specified... delete toots!
    else:
        await delete_toots(instance, toots_to_delete)
        print(f"All old toots deleted! Total of {total_toots_to_delete} toots deleted")

    # await mastodon.close()
    await session.close()


async def setup_shop() -> Tuple[bool, Configuration]:
    """Processes command line arguments, establishes debug logging to file if
    specified, loads configuration.

    Returns:
        bool: true if this is a dry-run, i.e. no toots should be actually deleted.
        Configuration: config for this run of the MastodonAmnesia.
    """
    parser = argparse.ArgumentParser(description="Delete old toots.")
    parser.add_argument(
        "-c",
        "--config-file",
        action="store",
        default="config.json",
        dest="config_file",
        help="Name of configuration file to use",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        help="Only print out which toots would be deleted. No actual deletion occurs",
        action="store_true",
        dest="dry_run",
    )
    parser.add_argument(
        "-l",
        "--debug-log-file",
        action="store",
        dest="debug_log_file",
        help="Path of filename to save DEBUG log messages to",
    )
    args = parser.parse_args()
    file_log_formatter = logging.Formatter(
        "%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )
    if args.debug_log_file:
        file_handler = logging.FileHandler(filename=args.debug_log_file)
        file_handler.setFormatter(file_log_formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
    config = await Configuration.load_config(config_file_name=args.config_file)
    return args.dry_run, config


async def delete_toots(
    instance: ActivityPub, toots_to_delete: list[dict[str, Any]]
) -> None:
    """Method to delete all toots that should be deleted."""
    title = "Deleting toots"
    total_toots_to_delete = len(toots_to_delete)
    if total_toots_to_delete > 0:
        with tqdm(
            desc=f"{title:.<60}",
            ncols=120,
            total=total_toots_to_delete,
            unit="toots",
            position=0,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} at {rate_fmt}",
        ) as progress_bar:

            while len(toots_to_delete) > 0:

                responses = await asyncio.gather(
                    *[delete_single_toot(i, instance) for i in toots_to_delete]
                )

                # Filter out any responses that are None...
                # Those encountered Rate Limiting
                deleted_toots = [toot for toot in responses if toot is not None]

                progress_bar.update(len(deleted_toots))

                if len(deleted_toots) < len(toots_to_delete):
                    await sleep_off_ratelimiting(instance=instance)

                for toot in deleted_toots:
                    toots_to_delete.remove(toot)


async def sleep_off_ratelimiting(instance: ActivityPub) -> None:
    """Determines time needed to wait and waits for rate limiting to be
    over."""

    logger.debug(
        "sleep_off_ratelimiting - Rate limited: Limit: %s - resetting at: %s",
        instance.ratelimit_remaining,
        instance.ratelimit_reset,
    )
    reset_at = arrow.get(instance.ratelimit_reset).datetime
    now = arrow.now().datetime
    need_to_wait = ceil((reset_at - now).total_seconds())

    logger.info(
        "Need to wait %s seconds (until %s) to let server 'cool down'",
        need_to_wait,
        arrow.get(instance.ratelimit_reset),
    )
    bar_title = "Waiting to let server 'cool-down'"
    for _i in trange(
        need_to_wait,
        desc=f"{bar_title:.<60}",
        unit="s",
        ncols=120,
        bar_format="{desc}: {percentage:3.0f}%|{bar}| Eta: {remaining} - Elapsed: {elapsed}",
        position=1,
    ):
        await asyncio.sleep(1)


async def delete_single_toot(
    toot: dict[str, Any], instance: ActivityPub
) -> Optional[dict[str, Any]]:
    """Deletes a single toot."""
    return_toot: Optional[dict[str, Any]] = toot
    try:
        await instance.delete_status(toot["id"])
        logger.info(
            "delete_single_toot - Deleted toot %s from %s",
            toot.get("url"),
            toot.get("created_at"),
        )
    except RatelimitError:
        logger.debug(
            "delete_single_toot - toot id = %s - ratelimit_remaining = %s - ratelimit_reset = %s",
            toot["id"],
            instance.ratelimit_remaining,
            instance.ratelimit_reset,
        )
        return_toot = None

    return return_toot


def check_updates() -> None:
    """Check if there is a newer version of MastodonAmnesia available on
    PyPI."""
    is_outdated = False
    try:
        is_outdated, pypi_version = check_outdated(
            package=__package_name__,
            version=__version__,
        )
        if is_outdated:
            print(
                f"[bold][red]!!! New version of {__display_name__} ({pypi_version}) "
                f"is available on PyPI.org !!!\n"
            )
            logger.debug(
                "check_updates - New version of %s (%s) is available on PyPI.org",
                __display_name__,
                pypi_version,
            )
    except ValueError:
        print(
            "[yellow]Notice - Your version is higher than last published version on PyPI"
        )
        logger.debug(
            "check_updates - Notice - Your version is higher than last published version on PyPI"
        )


def should_keep(
    toot: Dict[str, Any], oldest_to_keep: arrow.Arrow, config: Configuration
) -> bool:
    """Function to determine if toot should be kept even though it might be a
    candidate for deletion."""

    # Kind of agree, but alternative would be harder to read IMHO
    # pylint: disable=too-many-return-statements

    toot_created_at = arrow.get(cast(int, toot.get("created_at")))
    if toot_created_at >= oldest_to_keep:
        return True

    if config.bot.skip_deleting_bookmarked and bool(toot.get("bookmarked")):
        return True

    if config.bot.skip_deleting_faved and bool(toot.get("favourited")):
        return True

    if config.bot.skip_deleting_pinned and bool(toot.get("pinned")):
        return True

    if config.bot.skip_deleting_poll and bool(toot.get("poll")):
        return True

    if config.bot.skip_deleting_dm and toot.get("visibility") == "direct":
        return True

    medias = toot.get("media_attachments")
    if (
        config.bot.skip_deleting_media
        and isinstance(medias, list)
        and bool(len(medias))
    ):
        return True

    favourites = toot.get("favourites_count", 0)
    if (
        config.bot.skip_deleting_faved_at_least
        and favourites >= config.bot.skip_deleting_faved_at_least
    ):
        return True

    reblogs = toot.get("reblogs_count", 0)
    if (
        config.bot.skip_deleting_boost_at_least
        and reblogs >= config.bot.skip_deleting_boost_at_least
    ):
        return True

    return False


def start() -> None:
    """Main entry point for app."""
    asyncio.run(main())


# run main programs
if __name__ == "__main__":
    start()
