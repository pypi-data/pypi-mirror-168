# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kagi',
 'kagi.management',
 'kagi.management.commands',
 'kagi.migrations',
 'kagi.tests',
 'kagi.views']

package_data = \
{'': ['*'], 'kagi': ['static/kagi/*', 'templates/kagi/*']}

install_requires = \
['Django>=2.2', 'qrcode>=6.1,<8.0', 'webauthn>=0.4,<0.5']

setup_kwargs = {
    'name': 'kagi',
    'version': '0.3.0',
    'description': 'Django app for WebAuthn and TOTP-based multi-factor authentication',
    'long_description': 'Kagi\n====\n\n|coc| |build-status| |coverage| |readthedocs| |pypi|\n\n\n.. |coc| image:: https://img.shields.io/badge/%E2%9D%A4-code%20of%20conduct-blue.svg\n    :target: https://github.com/justinmayer/kagi/blob/master/CODE_OF_CONDUCT.rst\n    :alt: Code of Conduct\n\n.. |build-status| image:: https://img.shields.io/github/workflow/status/justinmayer/kagi/build\n    :target: https://github.com/justinmayer/kagi/actions\n    :alt: Build Status\n\n.. |coverage| image:: https://img.shields.io/badge/coverage-100%25-brightgreen\n    :target: https://github.com/justinmayer/kagi\n    :alt: Code Coverage\n\n.. |readthedocs| image:: https://readthedocs.org/projects/kagi/badge/?version=latest\n    :target: https://kagi.readthedocs.io/en/latest/\n    :alt: Documentation Status\n\n.. |pypi| image:: https://img.shields.io/pypi/v/kagi.svg\n    :target: https://pypi.org/project/kagi/\n    :alt: PyPI Version\n\n\nKagi provides support for FIDO WebAuthn security keys and TOTP tokens in Django.\n\nKagi is a relatively young project and has not yet been fully battle-tested.\nIts use in a high-impact environment should be accompanied by a thorough\nunderstanding of how it works before relying on it.\n\nInstallation\n------------\n\n::\n\n    python -m pip install kagi\n\nAdd ``kagi`` to ``INSTALLED_APPS`` and include ``kagi.urls`` somewhere in your\nURL patterns. Set: ``LOGIN_URL = "kagi:login"``\n\nMake sure that Django’s built-in login view does not have a\n``urlpattern``, because it will authenticate users without their second\nfactor. Kagi provides its own login view to handle that.\n\nDemo\n----\n\nTo see a demo, use the test project included in this repository and perform the\nfollowing steps (creating and activating a virtual environment first is optional).\n\nFirst, install Poetry_::\n\n    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -\n\nClone the Kagi source code and switch to its directory::\n\n    git clone https://github.com/justinmayer/kagi.git && cd kagi\n\nInstall dependencies, run database migrations, create a user, and serve the demo::\n\n    poetry install\n    poetry shell\n    invoke migrate\n    python testproj/manage.py createsuperuser\n    invoke serve\n\nYou should now be able to see the demo project login page in your browser at:\nhttp://localhost:8000/kagi/login\n\nSupported browsers and versions can be found here: https://caniuse.com/webauthn\nFor domains other than ``localhost``, WebAuthn requires that the site is served\nover a secure (HTTPS) connection.\n\nSince you haven’t added any security keys yet, you will be logged in with just a\nusername and password. Once logged in and on the multi-factor settings page,\nchoose “Manage WebAuthn keys” and then “Add another key” and follow the provided\ninstructions. Once WebAuthn and/or TOTP has been successfully configured, your\naccount will be protected by multi-factor authentication, and when you log in\nthe next time, your WebAuthn key or TOTP token will be required.\n\nYou can manage the keys attached to your account on the key management page at:\nhttp://localhost:8000/kagi/keys\n\n\nUsing WebAuthn Keys on Linux\n============================\n\nSome distros don’t come with udev rules to make USB HID /dev/\nnodes accessible to normal users. If your key doesn’t light up\nand start flashing when you expect it to, this might be what is\nhappening. See https://github.com/Yubico/libu2f-host/issues/2 and\nhttps://github.com/Yubico/libu2f-host/blob/master/70-u2f.rules for some\ndiscussion of the rule to make it accessible. If you just want a quick\ntemporary fix, you can run ``sudo chmod 666 /dev/hidraw*`` every time\nafter you plug in your key (the files disappear after unplugging).\n\n\nGratitude\n=========\n\nThis project would not exist without the significant contributions made by\n`Rémy HUBSCHER <https://github.com/natim>`_.\n\nThanks to Gavin Wahl for `django-u2f <https://github.com/gavinwahl/django-u2f>`_,\nwhich served as useful initial scaffolding for this project.\n\n\n.. _Poetry: https://python-poetry.org/docs/#installation\n',
    'author': 'Justin Mayer',
    'author_email': 'entroP@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/justinmayer/kagi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
