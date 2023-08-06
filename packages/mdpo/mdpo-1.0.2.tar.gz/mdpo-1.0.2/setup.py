# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mdpo', 'mdpo.md2po', 'mdpo.md2po2md', 'mdpo.mdpo2html', 'mdpo.po2md']

package_data = \
{'': ['*']}

install_requires = \
['contextlib-chdir>=1.0.1,<2.0.0',
 'importlib-metadata-argparse-version>=0.1.0,<0.2.0',
 'polib>=1.1.0,<2.0.0',
 'pymd4c>=1.1.2,<1.2.0']

extras_require = \
{':python_version < "3.10"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['md2po = mdpo.md2po.__main__:main',
                     'md2po2md = mdpo.md2po2md.__main__:main',
                     'mdpo2html = mdpo.mdpo2html.__main__:main',
                     'po2md = mdpo.po2md.__main__:main']}

setup_kwargs = {
    'name': 'mdpo',
    'version': '1.0.2',
    'description': 'Markdown files translation using PO files.',
    'long_description': '<p align="center">\n  <a href="https://github.com/mondeja/mdpo"><img src="https://raw.githubusercontent.com/mondeja/mdpo/master/mdpo.png" alt="mdpo" width="400"></a>\n</h1>\n\n<h4 align="center">Markdown files translation using PO files</h4>\n\n<p align="center">\n  <a href="https://pypi.org/project/mdpo/">\n    <img src="https://img.shields.io/pypi/v/mdpo"\n         alt="PyPI">\n  </a>\n  <a href="https://pypi.org/project/mdpo/">\n    <img src="https://img.shields.io/pypi/pyversions/mdpo?labelColor=333333">\n  </a>\n  <a href="https://github.com/mondeja/mdpo/blob/master/LICENSE">\n    <img src="https://img.shields.io/pypi/l/mdpo?color=light-green">\n  </a>\n</p>\n\n<h2 align="center">\n  <a href="https://mondeja.github.io/mdpo/">Documentation</a>\n</h2>\n\n<p align="center">\nComplies with <a href="https://spec.commonmark.org/">CommonMark Specification</a>\n<a href="https://spec.commonmark.org/0.29">v0.29</a> and\n<a href="https://spec.commonmark.org/0.30">v0.30</a>, supporting some\nadditional features.\n</p>\n\n## Status\n\n[![Documentation status][doc-image]][doc-link]\n[![Tests][tests-image]][tests-link]\n[![Coverage status][coverage-image]][coverage-link]\n\n## Installation\n\n```bash\npip install mdpo\n```\n\n[tests-image]: https://img.shields.io/github/workflow/status/mondeja/mdpo/Test?logo=github&label=tests\n[tests-link]: https://github.com/mondeja/mdpo/actions?query=workflow%3ATest\n[coverage-image]: https://img.shields.io/coveralls/github/mondeja/mdpo?logo=coveralls\n[coverage-link]: https://coveralls.io/github/mondeja/mdpo\n[doc-image]: https://img.shields.io/github/workflow/status/mondeja/mdpo/Test?label=docs&logo=readthedocs&logoColor=white\n[doc-link]: https://mondeja.github.io/mdpo/\n',
    'author': 'Álvaro Mondéjar Rubio',
    'author_email': 'mondejar1994@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mondeja/mdpo',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
