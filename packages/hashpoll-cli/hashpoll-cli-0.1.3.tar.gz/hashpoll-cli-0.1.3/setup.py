# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hashpoll_cli', 'hashpoll_cli.helpers']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'rich>=12.5.1,<13.0.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['hashpoll = hashpoll_cli.__main__:app']}

setup_kwargs = {
    'name': 'hashpoll-cli',
    'version': '0.1.3',
    'description': 'A handy CLI tool for creating polls for Hashnode. Made with ❤️ by @hashpoll.',
    'long_description': "# Hashpoll (CLI)\n\n![Hashpoll Banner](assets/Hashpoll.png)\n\nHashpoll is a hashnode widget that enables seamless polls on any post. It is a lightweight tool that generates code for you to put in hashnode's widget field to create polls that just blend in with the rest of your content. You can use it directly from the command line or through the Web interface, and manage your poll as needed.\n\nHashpoll CLI is a handy tool to extend and supplement Hashpoll. It allows you to seamlessly create polls from the command line. The tool automatically gives you the code to place in the widgets section of Hashnode. \n\n## Installation\n\nInstall hashpoll-cli with pip\n\n```bash\n  pip install hashpoll-cli\n```\n    \n## Commands\n\n### Create\nThis is the command to create polls from the CLI.  \n\n```bash\nhashpoll create [question] --option1 [option1] --option2 [option2] --option3 [option3] --option4 [option4]\n```\nor\n```bash\npython -m hashpoll create [question] --option1 [option1] --option2 [option2] --option3 [option3] --option4 [option4]\n```\n\n[![asciicast](https://asciinema.org/a/pZfU2ZIyot72RmtSD6yzfSioz.svg)](https://asciinema.org/a/pZfU2ZIyot72RmtSD6yzfSioz)\n\n#### Tips\n1. Put the question or options (if multiple words) in quotes to avoid the terminal registering this as multiple arguments.\n2. If you miss adding one of the options, the program will prompt you for entering them.\n\n### View\nThis is a command for viewing all details of a particular poll.\n\n```bash\nhashpoll view [Poll ID]\n```\n\nor \n\n```bash\npython -m hashpoll view [Poll ID]\n```\n\n[![asciicast](https://asciinema.org/a/LHrMNStGjVkRMP4hbGu5otF0L.svg)](https://asciinema.org/a/LHrMNStGjVkRMP4hbGu5otF0L)\n\n### Vote\nThis is a command to vote on a specific poll.\n\n```bash\nhashpoll vote [Poll ID] [Option Number]\n```\n\nor\n\n```bash\npython -m hashpoll vote [Poll ID] [Option Number]\n```\n\n[![asciicast](https://asciinema.org/a/1FDpi9gaVHZqeaLuxKAnjXecg.svg)](https://asciinema.org/a/1FDpi9gaVHZqeaLuxKAnjXecg)\n\n### Open-poll\nThis is a simple command to open a poll in the default browser.\n\n```bash\nhashpoll open-poll [Poll ID]\n```\n\nor\n\n```bash\npython -m hashpoll open-poll [Poll ID]\n```\n\n[![asciicast](https://asciinema.org/a/wA9D9Smrwx3H1dVkiaXZ1FzWC.svg)](https://asciinema.org/a/wA9D9Smrwx3H1dVkiaXZ1FzWC)\n\n### Results\nThis is a command to fetch the current data from poll responses.\n\n```bash\nhashpoll results [Poll ID]\n```\n\nor\n\n```bash\npython -m hashpoll results [Poll ID]\n```\n\n[![asciicast](https://asciinema.org/a/p455OvYTuy6e7Q9bECDWWDkbT.svg)](https://asciinema.org/a/p455OvYTuy6e7Q9bECDWWDkbT)\n\n### Code\nThis is handy commad to generate the Hashnode Widget Code for a particular poll.\n\n```bash\nhashpoll code [Poll ID]\n```\n\nor \n\n```bash\npython -m hashpoll code [Poll ID]\n```\n\n[![asciicast](https://asciinema.org/a/0R0xeOpRnSphSxKHOvVNcq2uR.svg)](https://asciinema.org/a/0R0xeOpRnSphSxKHOvVNcq2uR)\n## Features\n\n- Lightweight\n- CLI and Web Based\n- Seamless\n- Easy-to-integrate\n\n\n## Authors\n\n- [@Arpan-206](https://github.com/Arpan-206)\n\n\n## Tech Stack\n\n**Client:** AWS Amplify, Svelte, Typer, Rich, PicoCSS\n\n**Server:** Node, AWS Amplify, FastAPI\n\n## Roadmap\n\n- Password Protection\n\n- In-depth analytics\n\n- Authentication\n\n- Ability to modify a poll\n\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n\n\n## Acknowledgements\n\nHashpoll would like to thank the teams behind the following projects as they played a crucial part in enabling Hahpoll.\n\n - [AWS Amplify](https://aws.amazon.com/amplify/)\n - [Hashnode](https://hashnode.com/)\n - [FastAPI](https://fastapi.tiangolo.com/)\n - [Typer](https://typer.tiangolo.com/)\n - [PicoCSS](https://picocss.com/)\n\n\n## Feedback\n\nIf you have any feedback, please reach out to us at [arpan@hackersreboot.tech](mailto:arpan@hackersreboot.tech).\n\n\n## Contributing\n\nContributions are always welcome!\n\nSee `contributing.md` for ways to get started.\n\nPlease adhere to this project's `code of conduct`.",
    'author': 'Arpan Pandey',
    'author_email': 'arpan@hackersreboot.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Arpan-206/hashpoll-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
