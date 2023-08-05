# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.pelican_bibtex_reader']

package_data = \
{'': ['*']}

install_requires = \
['pelican>=4.5']

extras_require = \
{'markdown': ['markdown>=3.2']}

setup_kwargs = {
    'name': 'pelican-bibtex-reader',
    'version': '0.1.0',
    'description': 'A Pelican reader to process BibTeX files',
    'long_description': 'Pelican BibTeX Reader: A Plugin for Pelican\n====================================================\n\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-bibtex-reader)](https://pypi.org/project/pelican-bibtex-reader/)\n![License](https://img.shields.io/pypi/l/pelican-bibtex-reader?color=blue)\n\nA Pelican reader to process BibTeX files\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-bibtex-reader\n\nUsage\n-----\n\nThis plugin uses [python-bibtexparser](https://github.com/sciunto-org/python-bibtexparser) to parse properly formatted BibTeX files for use in\n[Pelican](https://getpelican.com/). Just put a BibTeX file\nwith ending `.bib` anywhere in your content directory.\n\nThe content provided by this plugin consists of only a\ncrude HTML rendering of the key-value pairs of each\nentry. However, the full bibtex database is available\nas Python object in the metadata of the page (key: `bibtexdatabase`).\nUsing an appropriate template, nice lists of literature\ncan be rendered, easily. Check out [the literature list on my homepage](https://andreas.fischer-family.online/pages/publications.html)\nfor an example.\n\nMetadata needed for Pelican \n(such as the title, the date, or the template to be used)\ncan be added at the top of the `.bib`-file, using the following syntax:\n\n```\n% Title: Some title\n% Date: 01.02.2023\n% ...\n% Feel free to write anything else; only\n% key: value\n% pairs are parsed. All other comments are ignored.\n\n@MISC{...}\n```\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/balanceofcowards/pelican-bibtex-reader/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\nLicense\n-------\n\nThis project is licensed under the AGPL-3.0 license.\n',
    'author': 'Andreas Fischer',
    'author_email': '_@ndreas.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/balanceofcowards/pelican-bibtex-reader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
