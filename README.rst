The byro Mailman plugin
==========================

This is a plugin for `byro`_. It allows to automatically and manually
(un)subscribe members to mailman mailinglists if mailman-api_ has been
installed on the mailman server.

Several mailinglists may be managed, and you can configure on a per-list basis
if members should be automatically added and/or removed from the list.

Development setup
-----------------

1. Make sure that you have a working byro development setup`.

2. Clone this repository, eg to ``local/byro-mailman``.

3. Activate the virtual environment you use for byro development.

4. Execute ``python setup.py develop`` within this directory to register this application with byro's plugin registry.

5. Restart your local byro server. The plugin is now in use.

6. To generate local translation files: ``django-admin makemessages -l de -i build -i dist -i "*egg*"``


License
-------

Copyright 2018 rixx

Released under the terms of the Apache License 2.0


.. _byro: https://github.com/byro/byro
.. _mailman-api: http://mailman-api.readthedocs.io/en/stable/quickstart.html
