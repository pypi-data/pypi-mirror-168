""""""""""""""""""""""""""
MastodonAmnesia
""""""""""""""""""""""""""

|Repo| |Downloads| |Codestyle| |Safety| |pip-audit| |Version| |Wheel| |CI| |AGPL|


***!!! BEWARE, THIS TOOL WILL DELETE SOME OF YOUR MASTODON TOOTS !!!***

MastodonAmnesia is a command line (CLI) tool to delete old toots from Mastodon or Pleroma instances.
It respects rate limits imposed by servers.

Install and run from `PyPi <https://pypi.org>`_
=================================================

It's ease to install MastodonAmnesia from Pypi using the following command::

    pip install mastodon_amnesia

Once installed MastodonManesia can be started by typing ``mastodonamnesia`` into the command line.

Install and run from `Source <https://codeberg.org/MarvinsMastodonTools/mastodonamnesia>`_
==============================================================================================

Alternatively you can run MastodonAmnesia from source by cloning the repository using the following command line::

    git clone https://codeberg.org/MarvinsMastodonTools/mastodonamnesia.git

MastodonAmnesia uses `Poetry <https://python-poetry.org/>`_ for dependency control, please install Poetry before proceeding further.

Before running, make sure you have all required python modules installed. With Poetry this is as easy as::

    poetry install --no-dev

Run MastodonAmnesia with the command `poetry run mastodonamnesia`

Configuration / First Run
=========================

MastodonAmnesia will ask for all necessary parameters when run for the first time and store them in ```config.json``
file in the current directory.

Licensing
=========
MastodonAmnesia is licensed under the `GNU Affero General Public License v3.0 <http://www.gnu.org/licenses/agpl-3.0.html>`_

Supporting MastodonAmnesia
==========================

There are a number of ways you can support MastodonAmnesia:

- Create an issue with problems or ideas you have with/for MastodonAmnesia
- You can `buy me a coffee <https://www.buymeacoffee.com/marvin8>`_.
- You can send me small change in Monero to the address below:

Monero donation address
-----------------------
``86ZnRsiFqiDaP2aE3MPHCEhFGTeipdQGJZ1FNnjCb7s9Gax6ZNgKTyUPmb21WmT1tk8FgM7cQSD5K7kRtSAt1y7G3Vp98nT``


.. |AGPL| image:: https://www.gnu.org/graphics/agplv3-with-text-162x68.png
    :alt: AGLP 3 or later
    :target:  https://codeberg.org/MarvinsMastodonTools/mastodonamnesia/src/branch/main/LICENSE.md

.. |Repo| image:: https://img.shields.io/badge/repo-Codeberg.org-blue
    :alt: Repo at Codeberg.org
    :target: https://codeberg.org/MarvinsMastodonTools/mastodonamnesia

.. |Downloads| image:: https://pepy.tech/badge/mastodonamnesia
    :alt: Download count
    :target: https://pepy.tech/project/mastodonamnesia

.. |Codestyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style: black
    :target: https://github.com/psf/black

.. |Safety| image:: https://img.shields.io/badge/Safety--DB-checked-green
    :alt: Checked against PyUp Safety DB
    :target: https://pyup.io/safety/

.. |pip-audit| image:: https://img.shields.io/badge/pip--audit-checked-green
    :alt: Checked with pip-audit
    :target: https://pypi.org/project/pip-audit/

.. |Version| image:: https://img.shields.io/pypi/pyversions/mastodonamnesia
    :alt: PyPI - Python Version

.. |Wheel| image:: https://img.shields.io/pypi/wheel/mastodonamnesia
    :alt: PyPI - Wheel

.. |CI| image:: https://ci.codeberg.org/api/badges/MarvinsMastodonTools/mastodonamnesia/status.svg
    :alt: CI / Woodpecker
    :target: https://ci.codeberg.org/MarvinsMastodonTools/mastodonamnesia
