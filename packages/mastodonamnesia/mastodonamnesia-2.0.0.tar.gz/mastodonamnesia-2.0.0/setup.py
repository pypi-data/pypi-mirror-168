# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mastodonamnesia']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'arrow>=1.2.1,<2.0.0',
 'minimal-activitypub>=0.2.0,<0.3.0',
 'outdated>=0.2.1,<0.3.0',
 'rich>=12.0.0,<13.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'typing-extensions>=4.2.0,<5.0.0']

entry_points = \
{'console_scripts': ['mastodonamnesia = '
                     'mastodonamnesia.mastodon_amnesia:start']}

setup_kwargs = {
    'name': 'mastodonamnesia',
    'version': '2.0.0',
    'description': 'deletes old Mastodon toots',
    'long_description': '""""""""""""""""""""""""""\nMastodonAmnesia\n""""""""""""""""""""""""""\n\n|Repo| |Downloads| |Codestyle| |Safety| |pip-audit| |Version| |Wheel| |CI| |AGPL|\n\n\n***!!! BEWARE, THIS TOOL WILL DELETE SOME OF YOUR MASTODON TOOTS !!!***\n\nMastodonAmnesia is a command line (CLI) tool to delete old toots from Mastodon or Pleroma instances.\nIt respects rate limits imposed by servers.\n\nInstall and run from `PyPi <https://pypi.org>`_\n=================================================\n\nIt\'s ease to install MastodonAmnesia from Pypi using the following command::\n\n    pip install mastodon_amnesia\n\nOnce installed MastodonManesia can be started by typing ``mastodonamnesia`` into the command line.\n\nInstall and run from `Source <https://codeberg.org/MarvinsMastodonTools/mastodonamnesia>`_\n==============================================================================================\n\nAlternatively you can run MastodonAmnesia from source by cloning the repository using the following command line::\n\n    git clone https://codeberg.org/MarvinsMastodonTools/mastodonamnesia.git\n\nMastodonAmnesia uses `Poetry <https://python-poetry.org/>`_ for dependency control, please install Poetry before proceeding further.\n\nBefore running, make sure you have all required python modules installed. With Poetry this is as easy as::\n\n    poetry install --no-dev\n\nRun MastodonAmnesia with the command `poetry run mastodonamnesia`\n\nConfiguration / First Run\n=========================\n\nMastodonAmnesia will ask for all necessary parameters when run for the first time and store them in ```config.json``\nfile in the current directory.\n\nLicensing\n=========\nMastodonAmnesia is licensed under the `GNU Affero General Public License v3.0 <http://www.gnu.org/licenses/agpl-3.0.html>`_\n\nSupporting MastodonAmnesia\n==========================\n\nThere are a number of ways you can support MastodonAmnesia:\n\n- Create an issue with problems or ideas you have with/for MastodonAmnesia\n- You can `buy me a coffee <https://www.buymeacoffee.com/marvin8>`_.\n- You can send me small change in Monero to the address below:\n\nMonero donation address\n-----------------------\n``86ZnRsiFqiDaP2aE3MPHCEhFGTeipdQGJZ1FNnjCb7s9Gax6ZNgKTyUPmb21WmT1tk8FgM7cQSD5K7kRtSAt1y7G3Vp98nT``\n\n\n.. |AGPL| image:: https://www.gnu.org/graphics/agplv3-with-text-162x68.png\n    :alt: AGLP 3 or later\n    :target:  https://codeberg.org/MarvinsMastodonTools/mastodonamnesia/src/branch/main/LICENSE.md\n\n.. |Repo| image:: https://img.shields.io/badge/repo-Codeberg.org-blue\n    :alt: Repo at Codeberg.org\n    :target: https://codeberg.org/MarvinsMastodonTools/mastodonamnesia\n\n.. |Downloads| image:: https://pepy.tech/badge/mastodonamnesia\n    :alt: Download count\n    :target: https://pepy.tech/project/mastodonamnesia\n\n.. |Codestyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :alt: Code style: black\n    :target: https://github.com/psf/black\n\n.. |Safety| image:: https://img.shields.io/badge/Safety--DB-checked-green\n    :alt: Checked against PyUp Safety DB\n    :target: https://pyup.io/safety/\n\n.. |pip-audit| image:: https://img.shields.io/badge/pip--audit-checked-green\n    :alt: Checked with pip-audit\n    :target: https://pypi.org/project/pip-audit/\n\n.. |Version| image:: https://img.shields.io/pypi/pyversions/mastodonamnesia\n    :alt: PyPI - Python Version\n\n.. |Wheel| image:: https://img.shields.io/pypi/wheel/mastodonamnesia\n    :alt: PyPI - Wheel\n\n.. |CI| image:: https://ci.codeberg.org/api/badges/MarvinsMastodonTools/mastodonamnesia/status.svg\n    :alt: CI / Woodpecker\n    :target: https://ci.codeberg.org/MarvinsMastodonTools/mastodonamnesia\n',
    'author': 'marvin8',
    'author_email': 'marvin8@tuta.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/MarvinsMastodonTools/mastodonamnesia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
