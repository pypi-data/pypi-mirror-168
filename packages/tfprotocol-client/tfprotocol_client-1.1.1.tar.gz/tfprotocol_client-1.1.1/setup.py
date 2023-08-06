# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfprotocol_client',
 'tfprotocol_client.connection',
 'tfprotocol_client.extensions',
 'tfprotocol_client.misc',
 'tfprotocol_client.models',
 'tfprotocol_client.security']

package_data = \
{'': ['*']}

install_requires = \
['multipledispatch>=0.6.0,<0.7.0', 'pycryptodome>=3.15.0,<4.0.0']

setup_kwargs = {
    'name': 'tfprotocol-client',
    'version': '1.1.1',
    'description': 'Transfer Protocol client implemented in python.',
    'long_description': "================================================\nTFProtocol Client Implemented in Python :snake:\n================================================\n.. image:: https://github.com/GoDjango-Development/tfprotocol_client_py/actions/workflows/publish-to-pypi-and-testpypi.yml/badge.svg?branch=master\n    :target: https://github.com/GoDjango-Development/tfprotocol_client_py/actions/workflows/publish-to-pypi-and-testpypi.yml\n\n.. image:: https://github.com/GoDjango-Development/tfprotocol_client_py/actions/workflows/test-package-code.yml/badge.svg\n    :target: https://github.com/GoDjango-Development/tfprotocol_client_py/actions/workflows/test-package-code.yml\n\n.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg\n    :target: https://GitHub.com/lagcleaner/tfprotocol_client_py/graphs/commit-activity\n\n.. image:: https://img.shields.io/github/issues/lagcleaner/tfprotocol_client_py.svg\n    :target: https://GitHub.com/lagcleaner/tfprotocol_client_py/issues/\n\n.. image:: https://img.shields.io/github/issues-closed/lagcleaner/tfprotocol_client_py.svg\n    :target: https://GitHub.com/lagcleaner/tfprotocol_client_py/issues?q=is%3Aissue+is%3Aclosed\n\n----------------\nIntroduction \n----------------\n\nThe especifications for the *Transference Protocol* is available in this `repository\n<https://github.com/GoDjango-Development/TFProtocol/blob/main/doc/>`_.\n\n\n---------------------------\nInstallation :floppy_disk:\n---------------------------\n\n.. image:: https://img.shields.io/pypi/v/tfprotocol-client.svg\n    :target: https://pypi.org/project/tfprotocol-client/\n\nThe package is available at `pypi <https://pypi.org/project/tfprotocol-client/>`_, to be installed from **pip** with the\nnext command:\n\n.. code-block:: bash\n\n    pip install tfprotocol_client\n\n-------------------------\nA Simple Example :memo:\n-------------------------\n\nTo use the *Transference Protocol* through this library, you must create an instance of\n*TfProtocol* with the specified parameters and have an online server to connect to.\n\n.. code-block:: python\n\n    from tfprotocol_client.misc.constants import RESPONSE_LOGGER\n    from tfprotocol_client.tfprotocol import TfProtocol\n\n    ADDRESS = 'tfproto.expresscuba.com'\n    PORT = 10345\n    clienthash = '<clienthash>'\n    publickey = '<publickey>'\n\n    proto = TfProtocol('0.0', publickey, clienthash, ADDRESS, PORT)\n    proto.connect()\n    proto.echo_command('Hello World', response_handler=RESPONSE_LOGGER)\n    proto.disconnect()\n\n\n---------------------------\nFor Contributors :wrench:\n---------------------------\n\n.. image:: https://img.shields.io/github/contributors/lagcleaner/tfprotocol_client_py.svg\n    :target: https://GitHub.com/lagcleaner/tfprotocol_client_py/graphs/contributors/\n\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nDevelopment Environment Installation :computer:\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\nTo set up the development environment, all you need as a prerequisite is to have Python 2.7\nor 3.5+ and `poetry <https://python-poetry.org/>`_ installed. If you need to install poetry\nfollow `these steps <https://python-poetry.org/docs/#installation>`_ and come back. \n\nWith this in mind, to install the necessary dependencies and create a python environment for\nthis project, proceed to run the following command in the root directory of the project.\n\n.. code-block:: bash\n\n    poetry install\n\n\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nProject Structure :open_file_folder:\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\nThis library is made up of 5 folders and the particular implementations of the ``TfProtocolSuper``\nclass, the folders are structured as follows:\n\n- **connection**: where all socket and low-level communication is located.\n- **models** where the complex objects used all over the package are defined.\n- **security** where is implemented the methods and classes to encrypt and decrypt the messages for communication and also the utils for do the hashing stuff where is needed.\n- **misc** to hold all utils and not related to any other folder concept.\n- **extensions** where are all the extensions for the *Transfer Protocol Client* .\n\nHere the visual schema for all the classes and his relations with others:\n\n.. image:: ./doc/statics/classes.png\n    :alt: class relations\n    :align: center\n\n^^^^^^^^^^^^^^^^^^^^\nPublishing :rocket:\n^^^^^^^^^^^^^^^^^^^^\n\nTo publish the package you need to run the following command in the root directory of the package:\n\n.. code-block:: bash\n\n    poetry publish\n\n.. image:: https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg\n    :target: mailto://lagcleaner@gmail.com\n",
    'author': 'Leonel Garcia',
    'author_email': 'lagcleaner@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lagcleaner/tfprotocol_client_py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
