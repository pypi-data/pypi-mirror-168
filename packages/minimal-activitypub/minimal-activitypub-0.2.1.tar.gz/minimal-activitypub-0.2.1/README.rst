""""""""""""""""""""""""""""""""""
Minimal-ActivityPub
""""""""""""""""""""""""""""""""""
|Repo| |Downloads| |Codestyle| |Safety| |pip-audit| |Version| |Wheel| |CI| |AGPL|


Minimal-ActivityPub is a minimal Python implementation of the ActivityPub rest API used by
`Mastodon <https://joinmastodon.org/>`_,
`Pleroma <https://pleroma.social/>`_,
and others. This implementation makes use of asyncio where appropriate. It is intended to be used as a library by other
applications. No standalone functionality is provided.

Minimal refers to the fact that only API calls I need for my other projects;
`MastodonAmnesia <https://codeberg.org/MarvinsMastodonTools/mastodonamnesia>`_ and
`TootBot <https://codeberg.org/MarvinsMastodonTools/tootbot>`_ are implemented.

**DO NOT** expect a full or complete implementation of all `ActivityPub API <https://activitypub.rocks/>`_ functionality.

==================================
API Methods Implemented currently
==================================

----------------------------------
Client to Server Methods
----------------------------------
- get_auth_token
- verify_credentials
- determine_instance_type
- get_account_statuses
- delete_status

----------------------------------
Server to Server Methods
----------------------------------
No API methods for server to server communications have been implemented.

==================================
Usage
==================================
Minimal-ActivityPub is available on `PyPi <https://pypi.org/>`_ as `minimal-activitypub` and can be added to an
application the same as any other python library.

Add `minimal-activitypub` as a requirement to your project and/or install using pip::

    pip install minimal-activitypub

----------------------------------
Workflow overview
----------------------------------
In general you need the authenticate to an ActivityPub server instance. To do so you require an `access_token`, so generally
you'll want to use the method ``get_auth_token`` when setting up the initial connection.

After that I think it is a good idea to verify the credentials using the ``verify_credentials`` method and determine the
server type using the ``determine_instance_type`` method.

After that you use which ever method(s) that are needed for your use case.

.. Todo: Add individual explanation for each method.

==================================
Contributing
==================================
Minimal-ActivityPub is using `Poetry <https://python-poetry.org/>`_ for dependency control, please install Poetry if you'd like to contribute.

To make sure you have all required python modules installed with Poetry is as easy as `poetry install` in the root of the
project directory

==================================
Licensing
==================================
Minimal-ActivityPub is licences under licensed under the `GNU Affero General Public License v3.0 <http://www.gnu.org/licenses/agpl-3.0.html>`_

==================================
Supporting Minimal-ActivityPub
==================================

There are a number of ways you can support Minimal-ActivityPub:

- Create an issue with problems or ideas you have with/for Minimal-ActivityPub
- You can `buy me a coffee <https://www.buymeacoffee.com/marvin8>`_.
- You can send me small change in Monero to the address below:

----------------------------------
Monero donation address:
----------------------------------
`8ADQkCya3orL178dADn4bnKuF1JuVGEG97HPRgmXgmZ2cZFSkWU9M2v7BssEGeTRNN2V5p6bSyHa83nrdu1XffDX3cnjKVu`


.. |AGPL| image:: https://www.gnu.org/graphics/agplv3-with-text-162x68.png
   :alt: `AGLP 3 or later <https://codeberg.org/MarvinsMastodonTools/minimal-activitypub/src/branch/main/LICENSE.md>`_

.. |Repo| image:: https://img.shields.io/badge/repo-Codeberg.org-blue
   :alt: `Repo <https://codeberg.org/MarvinsMastodonTools/minimal-activitypub>`_

.. |Downloads| image:: https://pepy.tech/badge/minimal-activitypub
   :alt: `Downloads <https://pepy.tech/project/minimal-activitypub>`_

.. |Codestyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :alt: `Code style: black <https://github.com/psf/black>`_

.. |Safety| image:: https://img.shields.io/badge/Safety--DB-checked-green
   :alt: `Checked against <https://pyup.io/safety/>`_

.. |pip-audit| image:: https://img.shields.io/badge/pip--audit-checked-green
   :alt: `Checked with <https://pypi.org/project/pip-audit/>`_

.. |Version| image:: https://img.shields.io/pypi/pyversions/minimal-activitypub
   :alt: PyPI - Python Version

.. |Wheel| image:: https://img.shields.io/pypi/wheel/minimal-activitypub
   :alt: PyPI - Wheel

.. |CI| image:: https://ci.codeberg.org/api/badges/MarvinsMastodonTools/minimal-activitypub/status.svg
   :alt: `CI / Woodpecker <https://ci.codeberg.org/MarvinsMastodonTools/minimal-activitypub>`_
