# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xiaomi_flashable_firmware_creator_gui',
 'xiaomi_flashable_firmware_creator_gui.components',
 'xiaomi_flashable_firmware_creator_gui.helpers']

package_data = \
{'': ['*'],
 'xiaomi_flashable_firmware_creator_gui': ['data/settings.json', 'i18n/*']}

install_requires = \
['PyQt5>=5.15.2,<6.0.0', 'xiaomi_flashable_firmware_creator>=2.2.8,<3.0.0']

entry_points = \
{'console_scripts': ['xiaomi_flashable_firmware_creator_g = '
                     'xiaomi_flashable_firmware_creator_gui.main:main']}

setup_kwargs = {
    'name': 'xiaomi-flashable-firmware-creator-gui',
    'version': '2.3.12',
    'description': 'Create flashable firmware zip from MIUI Recovery ROMs!',
    'long_description': '## Xiaomi Flashable Firmware Creator GUI\n\nCreate flashable firmware zip from MIUI Recovery ROMs!\n\n[![Crowdin](https://badges.crowdin.net/mi-flashable-firmware-creator/localized.svg)](https://crowdin.com/project/mi-flashable-firmware-creator)\n\n[![PyPI version](https://badge.fury.io/py/xiaomi-flashable-firmware-creator-gui.svg)](https://pypi.org/project/xiaomi-flashable-firmware-creator-gui/)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python%203-3776AB?style=flat\\&labelColor=3776AB\\&logo=python\\&logoColor=white\\&link=https://www.python.org/)](https://www.python.org/)\n[![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](#) <br />\n[![PayPal](https://img.shields.io/badge/PayPal-Donate-00457C?style=flat\\&labelColor=00457C\\&logo=PayPal\\&logoColor=white\\&link=https://www.paypal.me/yshalsager)](https://www.paypal.me/yshalsager)\n[![Patreon](https://img.shields.io/badge/Patreon-Support-F96854?style=flat\\&labelColor=F96854\\&logo=Patreon\\&logoColor=white\\&link=https://www.paypal.me/yshalsager)](https://www.paypal.me/yshalsager)\n[![Liberapay](https://img.shields.io/badge/Liberapay-Support-F6C915?style=flat\\&labelColor=F6C915\\&logo=Liberapay\\&logoColor=white\\&link=https://liberapay.com/yshalsager)](https://liberapay.com/yshalsager)\n\nXiaomi Flashable Firmware Creator is a tool that generates flashable firmware-update packages from official MIUI ROMS.\n\nIt supports creating untouched firmware, non-arb firmware, firmware + vendor flashable zip, and firmware-less ROMs.\n[![screenshot](https://raw.githubusercontent.com/XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator-gui/master/screenshots/1.png)](https://xiaomifirmwareupdater.com/projects/xiaomi-flashable-firmware-creator/)\n\n### Features:\n\n*   Easy-to-use interface\n*   Multilanguage support (more than 25 languages!). Thanks to our community members!\n\n#### Screenshots:\n\n[Here](https://github.com/XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator-gui/tree/master/screenshots)\n\n### Installation\n\n**Using pip**\nYou can simply install this tool using Python pip.\n\n```shell script\npip install xiaomi_flashable_firmware_creator_gui\n```\n\n**Manual Installation**\n\n*   Clone this repo using `git clone`\n*   Make sure that you have Python3 installed with pip version higher than 19 on your device.\n*   Install the required packages by running the following command in cloned repo folder.\n\n```shell script\npip3 install .\n```\n\n### GUI Usage:\n\n*   Run the tool.\n\n```shell script\nxiaomi_flashable_firmware_creator_g\n```\n',
    'author': 'yshalsager',
    'author_email': 'ysh-alsager@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://xiaomifirmwareupdater.com/projects/xiaomi-flashable-firmware-creator/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
