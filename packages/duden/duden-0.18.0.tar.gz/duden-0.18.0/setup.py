# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['duden']

package_data = \
{'': ['*'],
 'duden': ['locale/*',
           'locale/de_DE/LC_MESSAGES/*',
           'locale/eo/LC_MESSAGES/*',
           'locale/es_ES/LC_MESSAGES/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'crayons>=0.4.0,<0.5.0',
 'pyxdg>=0.28,<0.29',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['duden = duden.cli:main']}

setup_kwargs = {
    'name': 'duden',
    'version': '0.18.0',
    'description': 'CLI-based german dictionary',
    'long_description': '# Duden [![Version](http://img.shields.io/pypi/v/duden.svg?style=flat)](https://pypi.python.org/pypi/duden/)\n\n**duden** is a CLI-based program and python module, which can provide various information about given german word. The provided data are parsed from german dictionary [duden.de](https://duden.de).\n\n![duden screenshot](screenshot.png)\n\n## Installation\n```console\npip3 install duden\n```\n\n## Usage\n\n### CLI\n```console\n$ duden Löffel\n\nLöffel, der\n===========\nWord type: Substantiv, maskulin\nCommonness: 2/5\nSeparation: Löf|fel\nMeaning overview:\n 0.  a. [metallenes] [Ess]gerät, an dessen unterem Stielende eine schalenartige Vertiefung sitzt und das zur Aufnahme von Suppe, Flüssigkeiten, zur Zubereitung von Speisen o.\u2002Ä. verwendet wird\n     b. (Medizin) Kürette\n\n 1. (Jägersprache) Ohr von Hase und Kaninchen\n\nSynonyms:\nOhr; [Ge]hörorgan; (salopp) Horcher, Horchlappen, Lauscher; (Jägersprache) Loser, Teller\n```\n\n<details>\n<summary>Full CLI syntax (expand)</summary>\n\n```console\n$ duden --help\nusage: duden [-h] [--title] [--name] [--article] [--part-of-speech]\n             [--frequency] [--usage] [--word-separation]\n             [--meaning-overview] [--synonyms] [--origin]\n             [--compounds [COMPOUNDS]] [-g [GRAMMAR]] [--export]\n             [--words-before] [--words-after] [-r RESULT] [--fuzzy]\n             [--no-cache] [-V] [--phonetic] [--alternative-spellings]\n             word\n\npositional arguments:\n  word\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --title               display word and article\n  --name                display the word itself\n  --article             display article\n  --part-of-speech      display part of speech\n  --frequency           display commonness (1 to 5)\n  --usage               display context of use\n  --word-separation     display proper separation (line separated)\n  --meaning-overview    display meaning overview\n  --synonyms            list synonyms (line separated)\n  --origin              display origin\n  --compounds [COMPOUNDS]\n                        list common compounds\n  -g [GRAMMAR], --grammar [GRAMMAR]\n                        list grammar forms\n  --export              export parsed word attributes in yaml format\n  --words-before        list 5 words before this one\n  --words-after         list 5 words after this one\n  -r RESULT, --result RESULT\n                        display n-th (starting from 1) result in case of multiple words matching the input\n  --fuzzy               enable fuzzy word matching\n  --no-cache            do not cache retrieved words\n  -V, --version         print program version\n  --phonetic            display pronunciation\n  --alternative-spellings\n                        display alternative spellings\n```\n</details>\n\n### Module usage\n\n```python\n>>> import duden\n>>> w = duden.get(\'Loeffel\')\n>>> w.name\n\'Löffel\'\n>>> w.word_separation\n[\'Löf\', \'fel\']\n>>> w.synonyms\n\'Ohr; [Ge]hörorgan; (salopp) Horcher, Horchlappen, Lauscher; (Jägersprache) Loser, Teller\'\n```\nFor more examples see [usage documentation](docs/usage.md).\n\n## Development\n\nDependencies and packaging are managed by [Poetry](https://python-poetry.org/).\n\nInstall the virtual environment and enter it with\n```console\n$ poetry install\n$ poetry shell\n```\n\n### Testing and code style\n\nTo execute data tests, run\n```console\n$ pytest\n```\n\nTo run python style autoformaters (isort, black), run\n```console\n$ make autoformat\n```\n\n### Localization\n\nApart from English, this package has partial translations to German, Spanish, and Esperanto languages.\n\nTo test duden in other languages, set the `LANG` environment variable before running duden like so:\n```console\nLANG=de_DE.UTF-8 duden Kragen\nLANG=es_ES.UTF-8 duden Kragen\nLANG=eo_EO.UTF-8 duden Kragen\n```\n\nThe translations are located in the [duden/locale/](duden/locale/) directory as the `*.po` and `duden.pot` files. The `duden.pot` file defines all translatable strings in series of text blocks formatted like this:\n```\n#: main.py:82\nmsgid "Commonness:"\nmsgstr ""\n```\nwhile the individual language files provides translations to the strings identified by `msgid` like this:\n```\n#: main.py:82\nmsgid "Commonness:"\nmsgstr "Häufigkeit:"\n```\nNote that the commented lines like `#: main.py:82` do not have any functional meaning, and can get out of sync.\n\n### Publishing\n\nTo build and publish the package to (test) PyPI, you can use one of these shortcut commands:\n```console\n$ make pypi-publish-test\n$ make pypi-publish\n```\n(these also take care of building the localization files before calling `poetry publish`)\n\nPoetry configuration for PyPI and Test PyPI credentials are well covered in [this SO answer](https://stackoverflow.com/a/72524326).\n\n#### Including localization data in the package\n\nIn order for the localization data to be included in the resulting python package, the `*.po` files must be compiled using the\n```\n$ make localization\n```\ncommand before building the package with `poetry`.\n\n## Supported versions of Python\n\n* Python 3.4+\n',
    'author': 'Radomír Bosák',
    'author_email': 'radomir.bosak@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/radomirbosak/duden',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
