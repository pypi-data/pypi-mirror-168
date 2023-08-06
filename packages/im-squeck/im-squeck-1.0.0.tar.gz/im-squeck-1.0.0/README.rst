############
Squonk2 Deck
############

.. image:: https://img.shields.io/pypi/pyversions/im-squeck
   :alt: PyPI - Python Version
.. image:: https://img.shields.io/pypi/v/im-squeck
   :alt: PyPI
.. image:: https://img.shields.io/github/license/informaticsmatters/squonk2-deck
   :alt: GitHub
.. image:: https://img.shields.io/github/workflow/status/informaticsmatters/squonk2-deck/build
   :alt: GitHub Workflow Status

**Squeck** (Squonk2 Deck) is s Textual-UI (TUI) for the
summary visualisation of multiple Squonk2 environments.

.. image:: docs/images/screenshot.png

**Squeck** uses the `squonk2-python-client`_ to create a **Deck** displaying
summary information for multiple Squonk2 environments and uses Will McGugan's
`textual`_ framework to provide the user with a simple,
text-based user interface modelled on the popular `k9s`_ Kubernetes monitor.

.. _k9s: https://k9scli.io
.. _squonk2-python-client: https://github.com/InformaticsMatters/squonk2-python-client
.. _textual: https://github.com/Textualize/textual

************
Installation
************

**Squeck** is a Python application, written with Python 3.10 and published
to `PyPI`_ and is easily installed using ``pip``::

    pip install im-squeck

.. _pypi: https://pypi.org/project/im-squeck/

*********
Execution
*********

Before running **Squeck** you must have access to at least one Squonk2 environment.
**Squeck** obtains details of the environment through a YAML-based
*environments* file. An example file, ``environments``, is located in the root
of this project:

..  code-block:: yaml

    ---

    # An example Squeck environments file.
    #
    # It provides all the connection details for one or more Squonk2 environments.
    # It is expected to be found in the user's home directory
    # as '~/.squonk2/environments' or the user can 'point' to it by setting
    # 'SQUONK2_ENVIRONMENT_FILE', e.g. 'export SQUONK2_ENVIRONMENT_FILE=~/my-env'

    # The 'environments' block defines one or more environments.
    # Each has a name. Here we define an environment called 'site-a'
    # but environments can be called anything YAML accepts as a key,
    # although it would aid consistency if you restrict your names to letters
    # and hyphens.
    environments:
      site-a:
        # The hostname of the keycloak server, without a 'http' prefix
        # and without a '/auth' suffix.
        keycloak-hostname: example.com
        # The realm name used for the Squonk2 environment.
        keycloak-realm: squonk2
        # The Keycloak client IDs of the Account Server and Data Manager.
        # The Account Server client ID is optional.
        keycloak-as-client-id: account-server-api
        keycloak-dm-client-id: data-manager-api
        # The hostnames of the Account Server and Data Manager APIs,
        # without a 'http' prefix and without an 'api' suffix.
        # If you have not provided an Account Server client ID its
        # hostname value is not required.
        as-hostname: as.example.com
        dm-hostname: dm.example.com
        # The username and password of an admin user that has access
        # to the Account Server and Data Manager.
        # The user *MUST* have admin rights.
        admin-user: dlister
        admin-password: blob1234

    # The final part of the file is a 'default' property,
    # which Squeck uses to select the an environment from the block above
    # when all else fails. It's simply the name of one of the environment
    # declarations above.
    default: site-a

When **Squeck** starts it will look for the environments file in your home
directory, in the file ``~/.squonk2/environments``. If you place your populated
environments file there you need do nothing else prior to running **Squeck**.
If you prefer to put your ``environments`` file elsewhere, or have multiple
files, set the path to your file using the environment variable
``SQUONK2_ENVIRONMENTS_FILE``::

    export SQUONK2_ENVIRONMENTS_FILE=~/my-squonk2-environments

With an environments file in place you can run **Squeck**::

    squeck

Logging
-------

You can enable logging from **Squeck** and the underlying textual framework by
setting the environment variable ``SQUONK2_LOGFILE`` when running the
application::

    SQUONK2_LOGFILE=./squeck.log squeck

Debugging
---------

`Textual`_ doesn't like anything being written to the console so printing
(even to ``stderr``) will topple the display. That's why ``stderr`` is
diverted when the application is running and nothing is printed.
There comes a time, though, when you need to see the error log.
For these times you can run **Squeck** without stderr diverted::

    squeck --enable-stderr
