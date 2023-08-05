# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['minimal_activitypub']

package_data = \
{'': ['*']}

install_requires = \
['Brotli>=1.0.9,<2.0.0',
 'aiodns>=3.0.0,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'arrow>=1.2.1,<2.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'rich>=12.0.0,<13.0.0']

setup_kwargs = {
    'name': 'minimal-activitypub',
    'version': '0.2.1',
    'description': 'Minimal inplementation of ActivityPub Interface',
    'long_description': '""""""""""""""""""""""""""""""""""\nMinimal-ActivityPub\n""""""""""""""""""""""""""""""""""\n|Repo| |Downloads| |Codestyle| |Safety| |pip-audit| |Version| |Wheel| |CI| |AGPL|\n\n\nMinimal-ActivityPub is a minimal Python implementation of the ActivityPub rest API used by\n`Mastodon <https://joinmastodon.org/>`_,\n`Pleroma <https://pleroma.social/>`_,\nand others. This implementation makes use of asyncio where appropriate. It is intended to be used as a library by other\napplications. No standalone functionality is provided.\n\nMinimal refers to the fact that only API calls I need for my other projects;\n`MastodonAmnesia <https://codeberg.org/MarvinsMastodonTools/mastodonamnesia>`_ and\n`TootBot <https://codeberg.org/MarvinsMastodonTools/tootbot>`_ are implemented.\n\n**DO NOT** expect a full or complete implementation of all `ActivityPub API <https://activitypub.rocks/>`_ functionality.\n\n==================================\nAPI Methods Implemented currently\n==================================\n\n----------------------------------\nClient to Server Methods\n----------------------------------\n- get_auth_token\n- verify_credentials\n- determine_instance_type\n- get_account_statuses\n- delete_status\n\n----------------------------------\nServer to Server Methods\n----------------------------------\nNo API methods for server to server communications have been implemented.\n\n==================================\nUsage\n==================================\nMinimal-ActivityPub is available on `PyPi <https://pypi.org/>`_ as `minimal-activitypub` and can be added to an\napplication the same as any other python library.\n\nAdd `minimal-activitypub` as a requirement to your project and/or install using pip::\n\n    pip install minimal-activitypub\n\n----------------------------------\nWorkflow overview\n----------------------------------\nIn general you need the authenticate to an ActivityPub server instance. To do so you require an `access_token`, so generally\nyou\'ll want to use the method ``get_auth_token`` when setting up the initial connection.\n\nAfter that I think it is a good idea to verify the credentials using the ``verify_credentials`` method and determine the\nserver type using the ``determine_instance_type`` method.\n\nAfter that you use which ever method(s) that are needed for your use case.\n\n.. Todo: Add individual explanation for each method.\n\n==================================\nContributing\n==================================\nMinimal-ActivityPub is using `Poetry <https://python-poetry.org/>`_ for dependency control, please install Poetry if you\'d like to contribute.\n\nTo make sure you have all required python modules installed with Poetry is as easy as `poetry install` in the root of the\nproject directory\n\n==================================\nLicensing\n==================================\nMinimal-ActivityPub is licences under licensed under the `GNU Affero General Public License v3.0 <http://www.gnu.org/licenses/agpl-3.0.html>`_\n\n==================================\nSupporting Minimal-ActivityPub\n==================================\n\nThere are a number of ways you can support Minimal-ActivityPub:\n\n- Create an issue with problems or ideas you have with/for Minimal-ActivityPub\n- You can `buy me a coffee <https://www.buymeacoffee.com/marvin8>`_.\n- You can send me small change in Monero to the address below:\n\n----------------------------------\nMonero donation address:\n----------------------------------\n`8ADQkCya3orL178dADn4bnKuF1JuVGEG97HPRgmXgmZ2cZFSkWU9M2v7BssEGeTRNN2V5p6bSyHa83nrdu1XffDX3cnjKVu`\n\n\n.. |AGPL| image:: https://www.gnu.org/graphics/agplv3-with-text-162x68.png\n   :alt: `AGLP 3 or later <https://codeberg.org/MarvinsMastodonTools/minimal-activitypub/src/branch/main/LICENSE.md>`_\n\n.. |Repo| image:: https://img.shields.io/badge/repo-Codeberg.org-blue\n   :alt: `Repo <https://codeberg.org/MarvinsMastodonTools/minimal-activitypub>`_\n\n.. |Downloads| image:: https://pepy.tech/badge/minimal-activitypub\n   :alt: `Downloads <https://pepy.tech/project/minimal-activitypub>`_\n\n.. |Codestyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :alt: `Code style: black <https://github.com/psf/black>`_\n\n.. |Safety| image:: https://img.shields.io/badge/Safety--DB-checked-green\n   :alt: `Checked against <https://pyup.io/safety/>`_\n\n.. |pip-audit| image:: https://img.shields.io/badge/pip--audit-checked-green\n   :alt: `Checked with <https://pypi.org/project/pip-audit/>`_\n\n.. |Version| image:: https://img.shields.io/pypi/pyversions/minimal-activitypub\n   :alt: PyPI - Python Version\n\n.. |Wheel| image:: https://img.shields.io/pypi/wheel/minimal-activitypub\n   :alt: PyPI - Wheel\n\n.. |CI| image:: https://ci.codeberg.org/api/badges/MarvinsMastodonTools/minimal-activitypub/status.svg\n   :alt: `CI / Woodpecker <https://ci.codeberg.org/MarvinsMastodonTools/minimal-activitypub>`_\n',
    'author': 'marvin8',
    'author_email': 'marvin8@tuta.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/MarvinsMastodonTools/mastodonamnesia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
