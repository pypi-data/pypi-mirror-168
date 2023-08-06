# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bleak',
 'bleak.backends',
 'bleak.backends.bluezdbus',
 'bleak.backends.corebluetooth',
 'bleak.backends.p4android',
 'bleak.backends.p4android.recipes.bleak',
 'bleak.backends.winrt']

package_data = \
{'': ['*'], 'bleak.backends.p4android': ['java/com/github/hbldh/bleak/*']}

install_requires = \
['async-timeout>=3.0.0,<5']

extras_require = \
{':platform_system == "Darwin"': ['pyobjc-core>=8.5,<9.0',
                                  'pyobjc-framework-CoreBluetooth>=8.5,<9.0',
                                  'pyobjc-framework-libdispatch>=8.5,<9.0'],
 ':platform_system == "Linux"': ['dbus-fast>=1.4.0,<2.0.0'],
 ':platform_system == "Windows"': ['bleak-winrt>=1.1.1,<2.0.0'],
 ':python_version < "3.8"': ['typing-extensions>=4.2.0,<5.0.0']}

setup_kwargs = {
    'name': 'bleak',
    'version': '0.18.0',
    'description': 'Bluetooth Low Energy platform Agnostic Klient',
    'long_description': '=====\nbleak\n=====\n\n.. figure:: https://raw.githubusercontent.com/hbldh/bleak/master/Bleak_logo.png\n    :target: https://github.com/hbldh/bleak\n    :alt: Bleak Logo\n    :scale: 50%\n\n\n.. image:: https://github.com/hbldh/bleak/workflows/Build%20and%20Test/badge.svg\n    :target: https://github.com/hbldh/bleak/actions?query=workflow%3A%22Build+and+Test%22\n    :alt: Build and Test\n\n.. image:: https://img.shields.io/pypi/v/bleak.svg\n    :target: https://pypi.python.org/pypi/bleak\n\n.. image:: https://img.shields.io/pypi/dm/bleak.svg\n    :target: https://pypi.python.org/pypi/bleak\n    :alt: PyPI - Downloads\n\n.. image:: https://readthedocs.org/projects/bleak/badge/?version=latest\n    :target: https://bleak.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\nBleak is an acronym for Bluetooth Low Energy platform Agnostic Klient.\n\n* Free software: MIT license\n* Documentation: https://bleak.readthedocs.io.\n\nBleak is a GATT client software, capable of connecting to BLE devices\nacting as GATT servers. It is designed to provide a asynchronous,\ncross-platform Python API to connect and communicate with e.g. sensors.\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    $ pip install bleak\n\nFeatures\n--------\n\n* Supports Windows 10, version 16299 (Fall Creators Update) or greater\n* Supports Linux distributions with BlueZ >= 5.43\n* OS X/macOS support via Core Bluetooth API, from at least OS X version 10.11\n* Android backend compatible with python-for-android\n\nBleak supports reading, writing and getting notifications from\nGATT servers, as well as a function for discovering BLE devices.\n\nUsage\n-----\n\nTo discover Bluetooth devices that can be connected to:\n\n.. code-block:: python\n\n    import asyncio\n    from bleak import BleakScanner\n\n    async def main():\n        devices = await BleakScanner.discover()\n        for d in devices:\n            print(d)\n\n    asyncio.run(main())\n\n\nConnect to a Bluetooth device and read its model number:\n\n.. code-block:: python\n\n    import asyncio\n    from bleak import BleakClient\n\n    address = "24:71:89:cc:09:05"\n    MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"\n\n    async def main(address):\n        async with BleakClient(address) as client:\n            model_number = await client.read_gatt_char(MODEL_NBR_UUID)\n            print("Model Number: {0}".format("".join(map(chr, model_number))))\n\n    asyncio.run(main(address))\n\nDO NOT NAME YOUR SCRIPT ``bleak.py``! It will cause a circular import error.\n\nSee examples folder for more code, for instance example code for connecting to a\n`TI SensorTag CC2650 <http://www.ti.com/ww/en/wireless_connectivity/sensortag/>`_\n',
    'author': 'Henrik Blidh',
    'author_email': 'henrik.blidh@nedomkull.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hbldh/bleak',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
