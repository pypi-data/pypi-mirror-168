# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sphinxawesome_theme']

package_data = \
{'': ['*'], 'sphinxawesome_theme': ['static/*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0', 'python-dotenv>=0.19,<0.22', 'sphinx>4']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.1,<5.0.0'],
 'docs': ['myst-parser>=0.18,<0.19',
          'sphinx-autobuild>=2021.3.14,<2022.0.0',
          'sphinx-sitemap>=2.2.0,<3.0.0']}

entry_points = \
{'sphinx.html_themes': ['sphinxawesome_theme = sphinxawesome_theme']}

setup_kwargs = {
    'name': 'sphinxawesome-theme',
    'version': '3.3.5',
    'description': 'An awesome theme for the Sphinx documentation generator',
    'long_description': '<h1 align="center">Sphinx awesome theme</h1>\n\n<p align="center">\n   <img src="https://img.shields.io/github/license/kai687/sphinxawesome-theme?color=blue&style=for-the-badge" alt="MIT license">\n   <img src="https://img.shields.io/pypi/v/sphinxawesome-theme?color=eb5&style=for-the-badge&logo=pypi" alt="PyPI version">\n   <img src="https://img.shields.io/netlify/e6d20a5c-b49e-4ebc-80f6-59fde8f24e22?logo=netlify&style=for-the-badge" alt="Netlify Deploy">\n   <img src="https://img.shields.io/github/workflow/status/kai687/sphinxawesome-theme/Lint?label=Lint&logo=Github&style=for-the-badge" alt="Lint">\n</p>\n\n<p align="center">\n   Create beautiful and awesome documentation websites with <a href="https://www.sphinx-doc.org/en/master/">Sphinx</a>.\n   See how the theme looks like on <a href="https://sphinxawesome.xyz">sphinxawesome.xyz</a>.\n</p>\n\n## Get started\n\nTo use this theme for your documentation, install it via `pip` and add it to your\nSphinx configuration.\n\n1. Install the theme as a Python package:\n\n   ```console\n   pip install sphinxawesome-theme\n   ```\n\n   See [How to install the theme](https://sphinxawesome.xyz/how-to/install/) for more information.\n\n1. Set `html_theme` in the Sphinx configuration file `conf.py`:\n\n   ```python\n   html_theme = "sphinxawesome_theme"\n   ```\n\n1. Add the theme as an extension in the Sphinx configuration file `conf.py`:\n\n   ```python\n   extensions = ["sphinxawesome_theme"]\n   ```\n\n   See [How to load the theme](https://sphinxawesome.xyz/how-to/load/) for more information.\n\nFor more information about configuring the theme for your use case,\nsee [How to configure the theme](https://sphinxawesome.xyz/how-to/options/).\n\n## Features\n\nWith the Awesome Theme, you can build readable, functional, and beautiful documentation websites.\nThese features enhance the user experience:\n\n### Awesome code blocks\n\nThe code block shows the language of the code in a header.\nEach code block has a **Copy** button for easy copying.\nThis theme enhances Sphinx\'s `code-block` directive with:\n\n- `emphasize-added`: highlight lines that should be added to code\n- `emphasize-removed`: highlight lines that should be removed from the code\n- `emphasize-text: TEXT`: highlight `TEXT` in the code block to emphasize placeholder text the user should replace.\n\n### Collapsible elements\n\nNested navigation links allow you to reach all pages from all other pages.\nYou can make code object definitions, like methods, classes, or modules,\ncollapsible as well, to focus on one item at a time.\n\n<!-- vale Awesome.SpellCheck = NO -->\n\n### Better headerlinks\n\nClicking the link icon after a header or caption automatically copies the URL to the clipboard.\n\n<!-- vale Awesome.SpellCheck = YES -->\n\n### DocSearch\n\nIf you have an Algolia DocSearch account for your documentation (it\'s free for open source projects),\nyou can use DocSearch for a search-as-you-type experience with autocomplete.\n\n### Better keyboard navigation\n\n<!-- vale 18F.Clarity = NO -->\n\nUse the `Tab` key to quickly skip through all sections on the page.\nUse the `Space` key to expand or collapse items in the navigation menu or in code definitions.\n',
    'author': 'Kai Welke',
    'author_email': 'kai687@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://sphinxawesome.xyz',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
