# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teletgcf', 'teletgcf.bot', 'teletgcf.plugins']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'Telethon==1.25.0',
 'aiohttp>=3.7.4,<4.0.0',
 'cryptg>=0.2.post2,<0.3',
 'hachoir>=3.1.2,<4.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'pytesseract>=0.3.7,<0.4.0',
 'python-dotenv>=0.17.0,<0.18.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=10.3.0,<11.0.0',
 'tg-login>=0.0.2,<0.0.3',
 'typer>=0.3.2,<0.4.0',
 'verlat>=0.1.0,<0.2.0',
 'watermark.py>=0.0.3,<0.0.4']

entry_points = \
{'console_scripts': ['teletgcf = teletgcf.cli:app']}

setup_kwargs = {
    'name': 'teletgcf',
    'version': '0.2.13.post0',
    'description': 'The ultimate tool to automate custom telegram message forwarding.',
    'long_description': '<!-- markdownlint-disable -->\n\n<p align="center">\n<a href = "https://github.com/aahnik/tgcf" > <img src = "https://user-images.githubusercontent.com/66209958/115183360-3fa4d500-a0f9-11eb-9c0f-c5ed03a9ae17.png" alt = "tgcf logo"  width=120> </a>\n</p>\n\n<h1 align="center"> tgcf </h1>\n\n<p align="center">\nThe ultimate tool to automate custom telegram message forwarding.\n</p>\n\n<p align="center">\n<a href="https://github.com/aahnik/tgcf/blob/main/LICENSE"><img src="https://img.shields.io/github/license/aahnik/tgcf" alt="GitHub license"></a>\n<a href="https://github.com/aahnik/tgcf/stargazers"><img src="https://img.shields.io/github/stars/aahnik/tgcf?style=social" alt="GitHub stars"></a>\n<a href="https://github.com/aahnik/tgcf/issues"><img src="https://img.shields.io/github/issues/aahnik/tgcf" alt="GitHub issues"></a>\n<img src="https://img.shields.io/pypi/v/tgcf" alt="PyPI">\n<a href="https://twitter.com/intent/tweet?text=Wow:&amp;url=https%3A%2F%2Fgithub.com%2Faahnik%2Ftgcf"><img src="https://img.shields.io/twitter/url?style=social&amp;url=https%3A%2F%2Fgithub.com%2Faahnik%2Ftgcf" alt="Twitter"></a>\n</p>\n<p align="center">\n<a href="https://github.com/aahnik/tgcf/actions/workflows/quality.yml"><img src="https://github.com/aahnik/tgcf/actions/workflows/quality.yml/badge.svg" alt="Code Quality"></a>\n</p>\n<!-- markdownlint-enable -->\n\nLive-syncer, Auto-poster, backup-bot, cloner, chat-forwarder, duplicator, ...\n\nCall it whatever you like! tgcf can fulfill your custom needs.\n\nThe *key features* are:\n\n1. Forward messages as "forwarded" or\nsend a copy of the messages from source to destination chats.\n\n    > A chat can be anything: a group, channel, person or even another bot.\n\n2. Supports two [modes](https://github.com/aahnik/tgcf/wiki/Past-vs-Live-modes-explained)\nof operation _past_ or _live_.\n\n    > The past mode deals with all existing messages,\n    > while the live mode is for upcoming ones.\n\n3. You may [login](https://github.com/aahnik/tgcf/wiki/Login-with-a-bot-or-user-account)\nwith a _bot_ or an _user_ account.\n\n    > Telegram imposes certain\n    [limitations](https://github.com/aahnik/tgcf/wiki/Using-bot-accounts#limitations)\n    on bot accounts.\n    You may use an user account to perform the forwards if you wish.\n\n4. Perform custom manipulation on messages.\n\n    > You can\n    [filter](https://github.com/aahnik/tgcf/wiki/How-to-use-filters-%3F),\n    [format](https://github.com/aahnik/tgcf/wiki/Format-text-before-sending-to-destination),\n    [replace](https://github.com/aahnik/tgcf/wiki/Text-Replacement-feature-explained),\n    [watermark](https://github.com/aahnik/tgcf/wiki/How-to-use--watermarking-%3F),\n    [ocr](https://github.com/aahnik/tgcf/wiki/You-can-do-OCR)\n    and do whatever else you need !\n\n5. Detailed [wiki](https://github.com/aahnik/tgcf/wiki) +\nVideo tutorial.\n    > You can also [get help](#getting-help) from the community.\n\n6. If you are a python developer, writing\n[plugins](https://github.com/aahnik/tgcf/wiki/How-to-write-a-plugin-for-tgcf-%3F)\nfor tgcf is like stealing candy from a baby.\n    > Plugins modify the message before they are sent to the destination chat.\n\nWhat are you waiting for? Star the repo and click Watch to recieve updates.\n\n<!-- markdownlint-disable -->\n## Video Tutorial\n\nA youtube video is coming soon. [Subscribe](https://www.youtube.com/channel/UCcEbN0d8iLTB6ZWBE_IDugg) to get notified.\n\n<!-- markdownlint-enable -->\n\n## Installation\n\n- If you are an **Windows** user, who is not familiar with the command line, the\n[Windows guide](https://github.com/aahnik/tgcf/wiki/Run-tgcf-on-Windows)\nis for you.\n\n- To install tgcf on **Android** (Termux), there exists an installer script,\nthat allows you to install all dependencies by running just a single line command.\nRead the\n[guide for android](https://github.com/aahnik/tgcf/wiki/Run-on-Android-using-Termux)\nto learn.\n\n- If you are familiar with **Docker**, you may read the\n[docker guide](https://github.com/aahnik/tgcf/wiki/Install-and-run-using-docker)\nfor an isolated installation.\n\n- Otherwise for **Linux/Mac**,\n    you may install `tgcf` via python\'s package manager `pip`.\n\n    > **Note:** Make sure you have Python 3.8 or above installed.\n    Go to [python.org](https://python.org) to download python.\n\n    Open your terminal and run the following commands.\n\n    ```shell\n    pip install --upgrade tgcf\n    ```\n\n    To check if the installation succeeded, run\n\n    ```shell\n    tgcf --version\n    ```\n\n## Usage\n\nConfiguring `tgcf` is easy. You just need two files in your present directory\n(from which tgcf is invoked).\n\n- [`.env`](https://github.com/aahnik/tgcf/wiki/Environment-Variables)\n: To define your environment variables easily.\n\n- [`tgcf.config.yml`](https://github.com/aahnik/tgcf/wiki/How-to-configure-tgcf-%3F)\n: An `yaml` file to configure how `tgcf` behaves.\n\nIn your terminal, just run `tgcf live` or `tgcf past` to start `tgcf`.\nIt will prompt you to enter your phone no. or bot token, when you run it\nfor the first time.\n\nFor more details run `tgcf --help` or [read wiki](https://github.com/aahnik/tgcf/wiki/CLI-Usage).\n\n## Deploy to Cloud\n\nClick on [this link](https://m.do.co/c/98b725055148) and get **free 100$**\non Digital Ocean.\n\n[![DigitalOcean Referral Badge](https://web-platforms.sfo2.digitaloceanspaces.com/WWW/Badge%203.svg)](https://www.digitalocean.com/?refcode=98b725055148&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)\n\n> **NOTE** You will get nothing if you directly sign up from Digital Ocean Home Page.\n> **Use the link** above, or **click on the big fat button** above to get free 100$.\n\nDeploying to a cloud server is an easier alternative if you cannot install\non your own machine.\nCloud servers are very reliable and great for running `tgcf` in live mode\nfor a long time.\n\nYou can enjoy smooth one-click deploys to the major cloud providers.\n\n- [Heroku](https://github.com/aahnik/tgcf/wiki/Deploy-to-Heroku)\n- [Digital Ocean](https://github.com/aahnik/tgcf/wiki/Deploy-to-Digital-Ocean)\n- [Gitpod](https://github.com/aahnik/tgcf/wiki/Run-for-free-on-Gitpod")\n- [Python Anywhere](https://github.com/aahnik/tgcf/wiki/Run-on-PythonAnywhere)\n- [Google Cloud Run](https://github.com/aahnik/tgcf/wiki/Run-on-Google-Cloud)\n- [GitHub Actions](https://github.com/aahnik/tgcf/wiki/Run-tgcf-in-past-mode-periodically)\n\n## Getting Help\n\n- First of all [read the wiki](https://github.com/aahnik/tgcf/wiki)\nand [watch the videos](https://www.youtube.com/channel/UCcEbN0d8iLTB6ZWBE_IDugg)\nto get started.\n\n- Type your question in GitHub\'s Search bar on the top left of this page,\nand click "In this repository".\nGo through the issues, discussions and wiki pages that appear in the result.\nTry re-wording your query a few times before you give up.\n\n- If your question does not already exist,\nfeel free to ask your questions in the\n[Discussion forum](https://github.com/aahnik/tgcf/discussions/new).\nPlease avoid duplicates.\n\n- For reporting bugs or requesting a new feature please use the [issue tracker](https://github.com/aahnik/tgcf/issues/new)\nof the repo.\n\n## Contributing\n\nPRs are most welcome! Read the [contributing guidelines](/.github/CONTRIBUTING.md)\nto get started.\n\nIf you are not a developer, you may also contribute financially to\nincentivise the development of any custom feature you need.\n',
    'author': 'jabrapatel800',
    'author_email': 'jabrapatel800@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jabrapatel800/teletgcf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
