# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xiaomi_flashable_firmware_creator',
 'xiaomi_flashable_firmware_creator.extractors',
 'xiaomi_flashable_firmware_creator.extractors.handlers',
 'xiaomi_flashable_firmware_creator.extractors.ota_payload_extractor',
 'xiaomi_flashable_firmware_creator.helpers']

package_data = \
{'': ['*'], 'xiaomi_flashable_firmware_creator': ['binaries/*', 'templates/*']}

install_requires = \
['protobuf>=3.15,<5.0', 'remotezip>=0.9.2,<0.10.0']

entry_points = \
{'console_scripts': ['xiaomi_flashable_firmware_creator = '
                     'xiaomi_flashable_firmware_creator.xiaomi_flashable_firmware_creator:main']}

setup_kwargs = {
    'name': 'xiaomi-flashable-firmware-creator',
    'version': '2.2.8',
    'description': 'Create flashable firmware zip from MIUI Recovery ROMs!',
    'long_description': '## Xiaomi Flashable Firmware Creator\n\nCreate flashable firmware zip from MIUI Recovery ROMs!\n\n[![PyPI version](https://badge.fury.io/py/xiaomi-flashable-firmware-creator.svg)](https://pypi.org/project/xiaomi-flashable-firmware-creator/)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python%203-3776AB?style=flat\\&labelColor=3776AB\\&logo=python\\&logoColor=white\\&link=https://www.python.org/)](https://www.python.org/)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/9c1f6cee01b74ef8a2fd0f0c787596a8)](https://www.codacy.com/gh/XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator/dashboard?utm_source=github.com\\&utm_medium=referral\\&utm_content=XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator\\&utm_campaign=Badge_Grade)\n[![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](#) <br />\n[![PayPal](https://img.shields.io/badge/PayPal-Donate-00457C?style=flat\\&labelColor=00457C\\&logo=PayPal\\&logoColor=white\\&link=https://www.paypal.me/yshalsager)](https://www.paypal.me/yshalsager)\n[![Patreon](https://img.shields.io/badge/Patreon-Support-F96854?style=flat\\&labelColor=F96854\\&logo=Patreon\\&logoColor=white\\&link=https://www.paypal.me/yshalsager)](https://www.paypal.me/yshalsager)\n[![Liberapay](https://img.shields.io/badge/Liberapay-Support-F6C915?style=flat\\&labelColor=F6C915\\&logo=Liberapay\\&logoColor=white\\&link=https://liberapay.com/yshalsager)](https://liberapay.com/yshalsager)\n\nXiaomi Flashable Firmware Creator is a tool that generates flashable firmware-update packages from official MIUI ROMS.\n\nIt supports creating untouched firmware, non-arb firmware, firmware + vendor flashable zip, and firmware-less ROMs from any local zip file or direct link of the zip file.\n\n### Installation\n\nYou can simply install this tool using Python pip.\n\n```shell script\npip install xiaomi_flashable_firmware_creator\n```\n\n### CLI Usage\n\n```shell script\nxiaomi_flashable_firmware_creator [-h] (-F FIRMWARE | -N NONARB | -L FIRMWARELESS | -V VENDOR) [-o OUTPUT]\n```\n\n**Examples:**\n\n*   Creating normal (untouched) firmware:\n\n```shell script\nxiaomi_flashable_firmware_creator -F [MIUI ZIP]\n```\n\n*   Creating non-arb firmware (without anti-rollback):\n\n```shell script\nxiaomi_flashable_firmware_creator -N [MIUI ZIP]\n```\n\n*   Creating firmware-less ROM (stock untouched ROM with just firmware removed):\n\n```shell script\nxiaomi_flashable_firmware_creator -L [MIUI ZIP]\n```\n\n*   Creating firmware + vendor flashable zip:\n\n```shell script\nxiaomi_flashable_firmware_creator -V [MIUI ZIP]\n```\n\n### Using from other Python scripts\n\n```python\nfrom xiaomi_flashable_firmware_creator.firmware_creator import FlashableFirmwareCreator\n\n# initialize firmware creator object with the following parameters:\n# input_file: zip file to extract from. It can be a local path or a remote direct url.\n# process: Which mode should the tool use. This must be one of "firmware", "nonarb", "firmwareless" or "vendor".\n# out_dir: The output directory to store the extracted file in.\n\nfirmware_creator = FlashableFirmwareCreator(input_zip, process, output_dir)\n# Now, you can either use auto() method to create the new zip file or do stuff at your own using firmware_creator public methods.\nnew_zip = firmware_creator.auto()\n```\n',
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
