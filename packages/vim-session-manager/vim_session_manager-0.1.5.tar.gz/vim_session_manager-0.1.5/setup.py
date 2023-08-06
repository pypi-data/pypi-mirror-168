# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vim_session_manager']

package_data = \
{'': ['*']}

install_requires = \
['inquirer>=2.9.2,<3.0.0', 'result>=0.7.0,<0.8.0', 'rich>=11.0.0,<12.0.0']

entry_points = \
{'console_scripts': ['vsm = vim_session_manager.__main__:main']}

setup_kwargs = {
    'name': 'vim-session-manager',
    'version': '0.1.5',
    'description': 'A small python program for managing vim sessions',
    'long_description': '<div align="center">\n  <h1>Vim Session Manager</h1>\n  <p>A manager for the under-utilized `mksession` command in vim</p>\n  <img alt="GitHub issues" src="https://img.shields.io/github/issues/mattcoding4days/vsm?color=red&logo=github&style=for-the-badge">\n  <img alt="GitHub" src="https://img.shields.io/github/license/mattcoding4days/vsm?color=green&logo=github&style=for-the-badge">\n  <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/mattcoding4days/vsm?color=blue&logo=github&style=for-the-badge">\n  <img alt="GitHub forks" src="https://img.shields.io/github/forks/mattcoding4days/vsm?logo=github&style=for-the-badge">\n  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/mattcoding4days/vsm?color=orange&logo=github&style=for-the-badge">\n  <img alt="Lines of code" src="https://img.shields.io/tokei/lines/github/mattcoding4days/vsm?label=Source%20Lines%20of%20code&logo=github&style=for-the-badge">\n</div>\n\n## :information_source: Reasoning\n\n> If you use vim or neovim on a daily basis and work in large codebases, it is probably not uncommon for you\n> to have 10+ tabs open at a time, with various splits. Once you close this vim session the layout is lost to the ethers.\n> the `mksession` command in vim(neovim) can save you, thus saving the session to a directory, promising to return you to your\n> work exactly how you left it. However, the problem is most of us accrue many of these session files scattered about, personally\n> I have 28 vim session files, easily loading them, rememembering the context of each one, and removing stale sessions becomes a hassle.\n> enter `vsm` (Vim Session Manager), it allows you to list, open, and remove sessions files, either interactively or by name.\n\n## :superhero_man: Features\n\n#### Current planned features\n\n  * [x] Open session by name (regex filtered)\n  * [x] Remove session by name (regex filtered)\n  * [x] List all sessions\n  * [x] Open sessions from an interactive prompt\n  * [x] Batch session file removal from an interactive prompt\n  * [x] Manages different vim variations (vim, nvim, gvim, macvim etc..)\n  * [ ] Show programmer statistics for each session when listed\n\n#### Current planned packaging \n\n  * [x] Pip install from this repo\n  * [x] Build and install manually with poetry\n  * [x] Pip install from pypi\n\n## Installing\n\n1. Install from pypi\n\n> [Check it out on Pypi](https://pypi.org/project/vim-session-manager/#description)\n\n`pip install vim-session-manager`\n\n2. Pip Installing from the git repo\n\n```bash\n# Copy and run this command\npip install git+https://github.com/mattcoding4days/vsm.git#egg=vim_session_manager --user\n```\n\n## :mage: Usage\n\n### Set up\n\n> NOTE that an environement variable `VIM_SESSIONS` is expected on the system,\n> if it is not defined `vsm` will default to `~/.config/vim_sessions` when it looks\n> for your session files.\n\n* bash/zsh `export VIM_SESSIONS="path/to/where/you/want/to/store/your/sessions"`\n\n* fish `set -Ux VIM_SESSIONS "path/to/where/you/want/to/store/your/sessions"`\n\n### Create session files easier\n\n> Add the below snippet to your `.vimrc` or `init.vim` to make creating\n> new session files much easier.\n\n```vim\nif isdirectory(expand($VIM_SESSIONS))\n  nnoremap mk :mksession $VIM_SESSIONS/\n  nnoremap mo :mksession! $VIM_SESSIONS/\nelse\n  nnoremap mk :echo "VIM_SESSIONS directory does not exist, get vim session manager at https://github.com/mattcoding4days/vsm"<CR>\n  nnoremap mo :echo "VIM_SESSIONS directory does not exist, get vim session manager at https://github.com/mattcoding4days/vsm"<CR>\nendif\n```\n\n<div align="center">\n  <h3>Exploring the help menu for subcommands</h3>\n  <img width="800" height="300" src="assets/vsm_help.gif">\n  <br>\n</div>\n\n<div align="center">\n  <h3>Managing many variations of vim installed on the system</h3>\n  <img width="800" height="300" src="assets/vsm_vim_variant.gif">\n  <br>\n</div>\n\n<div align="center">\n  <h3>Open a session file interactively</h3>\n  <img width="800" height="300" src="assets/vsm_open_interactive.gif">\n  <br>\n</div>\n\n<div align="center">\n  <h3>Open session file by name</h3>\n  <img width="800" height="300" src="assets/vsm_open_name.gif">\n  <br>\n</div>\n\n<div align="center">\n  <h3>Remove session file(s) interactively (one or many)</h3>\n  <p>Note that only the arrow keys are supported for movement, and the space bar is used to select/unselect</p>\n  <img width="800" height="300" src="assets/vsm_remove_interactive.gif">\n  <br>\n</div>\n\n<div align="center">\n  <h3>Remove a single session file by name (with regex matching)</h3>\n  <img width="800" height="300" src="assets/vsm_remove_name.gif">\n  <br>\n</div>\n\n## :construction_worker: Development\n\n> The project is managed by [Python Poetry](https://python-poetry.org/) and uses python >= 3.10.1.\n> Note: mypy static analyzing currently will not work as it does not yet support the match statement\n\n### :keyboard: Commands to help you out\n\n> NOTE: if you are installing poetry, DO NOT install it with pip\n> `curl -sSL https://install.python-poetry.org | python3 -`\n\n#### Install the package\n`poetry install`\n\n#### Run the tests to verify everything worked\n`pytest`\n\n#### Start a poetry shell and run the executable\n`poetry shell`\n`vsm --help`\n\n\n## :package: 3rd party libraries\n\n> Vim Session Manager uses the following Python libraries\n\n1. [result for Rust like elegance](https://github.com/rustedpy/result)\n\n2. [inquirer for fancy prompt driven selection](https://pypi.org/project/inquirer/)\n\n3. [rich, make terminal programs great again](https://github.com/Textualize/rich)\n\n## :scroll: Documentation\n\n> To be completed\n',
    'author': 'Matt Williams',
    'author_email': 'matt.k.williams@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mattcoding4days/vsm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.1,<4.0.0',
}


setup(**setup_kwargs)
