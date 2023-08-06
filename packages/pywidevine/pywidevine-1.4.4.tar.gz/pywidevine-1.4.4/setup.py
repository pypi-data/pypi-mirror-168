# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywidevine']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.4,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'lxml>=4.9.1',
 'protobuf==3.19.5',
 'pycryptodome>=3.15.0,<4.0.0',
 'pymp4>=1.2.0,<2.0.0',
 'requests>=2.28.1,<3.0.0']

extras_require = \
{'serve': ['aiohttp>=3.8.1,<4.0.0', 'PyYAML>=6.0,<7.0']}

entry_points = \
{'console_scripts': ['pywidevine = pywidevine.main:main']}

setup_kwargs = {
    'name': 'pywidevine',
    'version': '1.4.4',
    'description': 'Widevine CDM (Content Decryption Module) implementation in Python.',
    'long_description': '<p align="center">\n    <img src="docs/images/widevine_icon_24.png"> <a href="https://github.com/rlaphoenix/pywidevine">pywidevine</a>\n    <br/>\n    <sup><em>Python Widevine CDM implementation.</em></sup>\n</p>\n\n<p align="center">\n    <a href="https://github.com/rlaphoenix/pywidevine/actions/workflows/ci.yml">\n        <img src="https://github.com/rlaphoenix/pywidevine/actions/workflows/ci.yml/badge.svg" alt="Build status">\n    </a>\n    <a href="https://pypi.org/project/pywidevine">\n        <img src="https://img.shields.io/badge/python-3.7%2B-informational" alt="Python version">\n    </a>\n    <a href="https://deepsource.io/gh/rlaphoenix/pywidevine">\n        <img src="https://deepsource.io/gh/rlaphoenix/pywidevine.svg/?label=active+issues" alt="DeepSource">\n    </a>\n</p>\n\n## Features\n\n- 🛡️ Security-first approach; All user input has Signatures verified\n- 👥 Remotely accessible Server/Client CDM code\n- 📦 Supports parsing and serialization of WVD (v2) provisions\n- 🛠️ Class for creation, parsing, and conversion of PSSH data\n- 🧩 Plug-and-play installation via PIP/PyPI\n- 🗃️ YAML configuration files\n- ❤️ Forever FOSS!\n\n## Installation\n\n*Note: Requires [Python] 3.7.0 or newer with PIP installed.*\n\n```shell\n$ pip install pywidevine\n```\n\nYou now have the `pywidevine` package installed and a `pywidevine` executable is now available.\nCheck it out with `pywidevine --help` - Voilà 🎉!\n\n### From Source Code\n\nThe following steps are instructions on download, preparing, and running the code under a Poetry environment.\nYou can skip steps 3-5 with a simple `pip install .` call instead, but you miss out on a wide array of benefits.\n\n1. `git clone https://github.com/rlaphoenix/pywidevine`\n2. `cd pywidevine`\n3. (optional) `poetry config virtualenvs.in-project true` \n4. `poetry install`\n5. `poetry run pywidevine --help`\n\nAs seen in Step 5, running the `pywidevine` executable is somewhat different to a normal PIP installation.\nSee [Poetry\'s Docs] on various ways of making calls under the virtual-environment.\n\n  [Python]: <https://python.org>\n  [Poetry]: <https://python-poetry.org>\n  [Poetry\'s Docs]: <https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment>\n\n## Usage\n\nThe following is a minimal example of using pywidevine in a script. It gets a License for Bitmovin\'s\nArt of Motion Demo. There\'s various stuff not shown in this specific example like:\n\n- Privacy Mode\n- Setting Service Certificates\n- Remote CDMs and Serving\n- Choosing a License Type to request\n- Creating WVD files\n- and much more!\n\nJust take a look around the Cdm code to see what stuff does. Everything is documented quite well.\nThere\'s also various functions in `main.py` that showcases a lot of features.\n\n```py\nfrom pywidevine.cdm import Cdm\nfrom pywidevine.device import Device\nfrom pywidevine.pssh import PSSH\n\nimport requests\n\n# prepare pssh\npssh = PSSH("AAAAW3Bzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAADsIARIQ62dqu8s0Xpa"\n            "7z2FmMPGj2hoNd2lkZXZpbmVfdGVzdCIQZmtqM2xqYVNkZmFsa3IzaioCSEQyAA==")\n\n# load device\ndevice = Device.load("C:/Path/To/A/Provision.wvd")\n\n# load cdm\ncdm = Cdm.from_device(device)\n\n# open cdm session\nsession_id = cdm.open()\n\n# get license challenge\nchallenge = cdm.get_license_challenge(session_id, pssh)\n\n# send license challenge (assuming a generic license server SDK with no API front)\nlicence = requests.post("https://...", data=challenge)\nlicence.raise_for_status()\n\n# parse license challenge\ncdm.parse_license(session_id, licence.content)\n\n# print keys\nfor key in cdm.get_keys(session_id):\n    print(f"[{key.type}] {key.kid.hex}:{key.key.hex()}")\n\n# close session, disposes of session data\ncdm.close(session_id)\n```\n\n## Troubleshooting\n\n### Executable `pywidevine` was not found\n\nMake sure the Python installation\'s Scripts directory is added to your Path Environment Variable.\n\nIf this happened under a Poetry environment, make sure you use the appropriate Poetry-specific way of calling\nthe executable. You may make this executable available globally by adding the .venv\'s Scripts folder to your\nPath Environment Variable.\n\n## Disclaimer\n\n1. This project requires a valid Google-provisioned Private Key and Client Identification blob which are not\n   provided by this project.\n2. Public test provisions are available and provided by Google to use for testing projects such as this one.\n3. License Servers have the ability to block requests from any provision, and are likely already blocking test\n   provisions on production endpoints.\n4. This project does not condone piracy or any action against the terms of the DRM systems.\n5. All efforts in this project have been the result of Reverse-Engineering, Publicly available research, and Trial\n   & Error.\n\n## Key and Output Security\n\n*Licenses, Content Keys, and Decrypted Data is not secure in this CDM implementation.*\n\nThe Content Decryption Module is meant to do all downloading, decrypting, and decoding of content, not just license\nacquisition. This Python implementation only does License Acquisition within the CDM.\n\nThe section of which a \'Decrypt Frame\' call is made would be more of a \'Decrypt File\' in this implementation. Just\nreturning the original file in plain text defeats the point of the DRM. Even if \'Decrypt File\' was somehow secure, the\nContent Keys used to decrypt the files are already exposed to the caller anyway, allowing them to manually decrypt.\n\nAn attack on a \'Decrypt Frame\' system would be analogous to doing an HDMI capture or similar attack. This is because it\nwould require re-encoding the video by splicing each individual frame with the right frame-rate, syncing to audio, and\nmore.\n\nWhile a \'Decrypt Video\' system would be analogous to downloading a Video and passing it through a script. Not much of\nan attack if at all. The only protection against a system like this would be monitoring the provision and acquisitions\nof licenses and prevent them. This can be done by revoking the device provision, or the user or their authorization to\nthe service.\n\nThere isn\'t any immediate way to secure either Key or Decrypted information within a Python environment that is not\nHardware backed. Even if obfuscation or some other form of Security by Obscurity was used, this is a Software-based\nContent Protection Module (in Python no less) with no hardware backed security. It would be incredibly trivial to break\nany sort of protection against retrieving the original video data.\n\nThough, it\'s not impossible. Google\'s Chrome Browser CDM is a simple library extension file programmed in C++ that has\nbeen improving its security using math and obscurity for years. It\'s getting harder and harder to break with its latest\nversions only being beaten by Brute-force style methods. However, they have a huge team of very skilled workers, and\nmaking a CDM in C++ has immediate security benefits and a lot of methods to obscure and obfuscate the code.\n\n## Credit\n\n- Widevine Icon &copy; Google.\n- The awesome community for their shared research and insight into the Widevine Protocol and Key Derivation.\n\n## License\n\n[GNU General Public License, Version 3.0](LICENSE)\n',
    'author': 'rlaphoenix',
    'author_email': 'rlaphoenix@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rlaphoenix/pywidevine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
