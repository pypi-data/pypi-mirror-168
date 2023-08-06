# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyuga', 'hyuga.sym']

package_data = \
{'': ['*']}

install_requires = \
['hy>=0.24.0,<0.25.0',
 'hyrule>=0.2,<0.3',
 'pygls>=0.12.1,<0.13.0',
 'toolz>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['hyuga = hyuga.__main__:main']}

setup_kwargs = {
    'name': 'hyuga',
    'version': '0.0.7',
    'description': 'Hyuga - Yet Another Hy Language Server',
    'long_description': "Hyuga - Yet Another Hy Language Server\n======================================\n\n[![PyPI version](https://badge.fury.io/py/hyuga.svg)](https://badge.fury.io/py/hyuga)\n\nForked from [hy-language-server](https://github.com/rinx/hy-language-server).\n\nVerified-working Hy version: [0.24.0](https://github.com/hylang/hy/tree/stable)\n\n## Feature\n\n- `textDocument/did{Open,Change}`\n- `textDocument/completion`\n  - Presents candidates all modules installed in your system, classes/functions in opening source.\n- `textDocument/hover`\n\n## Screenshots\n\n![Hyuga sample movie](https://raw.githubusercontent.com/sakuraiyuta/hyuga/images/hyuga-image.gif)\n\n\n## Install\n\n### plain install\n\n```bash\npip3 install hyuga\n```\n\n### [neovim(nvim)](https://github.com/neovim/neovim) + [vim-lsp](https://github.com/prabirshrestha/vim-lsp) + [vim-lsp-settings]()\n\n**Note:** Currently `vim-lsp-settings` doesn't have installer for Hyuga.\nYou can test with [my vim-lsp-settings branch](https://github.com/sakuraiyuta/vim-lsp-settings/tree/add-lang/hyuga).\n\nSample for dein:\n\n```vim\ncall dein#add('sakuraiyuta/vim-lsp-settings', {'rev': 'add-lang/hyuga'})\n```\n\nAnd open `*.hy` file with `filetype=hy`, then run `:LspInstallServer`\n\n### [Visual Studio Code(VSCode)](https://code.visualstudio.com)\n\nTODO: implement\n\n## Development\n\n### Setup\n\n- Install [poetry](https://github.com/python-poetry/poetry).\n- Clone this project: `git clone https://github.com/sakuraiyuta/hyuga.git`\n- In project directory, execute `poetry install`.\n\n### Test\n\n```bash\npoetry run pytest tests\n```\n\n## License\n\nMIT\n",
    'author': 'Yuuta Sakurai',
    'author_email': 'sakurai.yuta@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
