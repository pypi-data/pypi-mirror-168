# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cihai', 'cihai.data', 'cihai.data.decomp', 'cihai.data.unihan']

package_data = \
{'': ['*']}

install_requires = \
['appdirs', 'kaptan', 'sqlalchemy<1.4', 'unihan-etl>=0.18.0,<0.19.0']

setup_kwargs = {
    'name': 'cihai',
    'version': '0.17.1a0',
    'description': 'Library for CJK (chinese, japanese, korean) language data.',
    'long_description': '# cihai &middot; [![Python Package](https://img.shields.io/pypi/v/cihai.svg)](https://pypi.org/project/cihai/) [![License](https://img.shields.io/github/license/cihai/cihai.svg)](https://github.com/cihai/cihai/blob/master/LICENSE) [![Code Coverage](https://codecov.io/gh/cihai/cihai/branch/master/graph/badge.svg)](https://codecov.io/gh/cihai/cihai)\n\nPython library for [CJK](https://cihai.git-pull.com/glossary.html#term-cjk) (chinese, japanese,\nkorean) data.\n\nThis project is under active development. Follow our progress and check back for updates!\n\n## Quickstart\n\n### API / Library (this repository)\n\n```console\n$ pip install --user cihai\n```\n\n```python\nfrom cihai.core import Cihai\n\nc = Cihai()\n\nif not c.unihan.is_bootstrapped:  # download and install Unihan to db\n    c.unihan.bootstrap(unihan_options)\n\nquery = c.unihan.lookup_char(\'好\')\nglyph = query.first()\nprint("lookup for 好: %s" % glyph.kDefinition)\n# lookup for 好: good, excellent, fine; well\n\nquery = c.unihan.reverse_char(\'good\')\nprint(\'matches for "good": %s \' % \', \'.join([glph.char for glph in query]))\n# matches for "good": 㑘, 㑤, 㓛, 㘬, 㙉, 㚃, 㚒, 㚥, 㛦, 㜴, 㜺, 㝖, 㤛, 㦝, ...\n```\n\nSee [API](https://cihai.git-pull.com/api.html) documentation and\n[/examples](https://github.com/cihai/cihai/tree/master/examples).\n\n### CLI ([cihai-cli](https://cihai-cli.git-pull.com))\n\n```console\n$ pip install --user cihai-cli\n```\n\nCharacter lookup:\n\n```console\n$ cihai info 好\n```\n\n```yaml\nchar: 好\nkCantonese: hou2 hou3\nkDefinition: good, excellent, fine; well\nkHangul: 호\nkJapaneseOn: KOU\nkKorean: HO\nkMandarin: hǎo\nkTang: "*xɑ̀u *xɑ̌u"\nkTotalStrokes: "6"\nkVietnamese: háo\nucn: U+597D\n```\n\nReverse lookup:\n\n```console\n$ cihai reverse library\n```\n\n```yaml\nchar: 圕\nkCangjie: WLGA\nkCantonese: syu1\nkCihaiT: \'308.302\'\nkDefinition: library\nkMandarin: tú\nkTotalStrokes: \'13\'\nucn: U+5715\n--------\n```\n\n### UNIHAN data\n\nAll datasets that cihai uses have stand-alone tools to export their data. No library required.\n\n- [unihan-etl](https://unihan-etl.git-pull.com) - [UNIHAN](http://unicode.org/charts/unihan.html)\n  data exports for csv, yaml and json.\n\n## Developing\n\n```console\n$ git clone https://github.com/cihai/cihai.git`\n```\n\n```console\n$ cd cihai/\n```\n\n[Bootstrap your environment and learn more about contributing](https://cihai.git-pull.com/contributing/). We use the same conventions / tools across all cihai projects: `pytest`, `sphinx`, `flake8`, `mypy`, `black`, `isort`, `tmuxp`, and file watcher helpers (e.g. `entr(1)`).\n\n## Quick links\n\n- [Quickstart](https://cihai.git-pull.com/quickstart.html)\n- [Datasets](https://cihai.git-pull.com/datasets.html) a full list of current and future data sets\n- Python [API](https://cihai.git-pull.com/api.html)\n- [Roadmap](https://cihai.git-pull.com/design-and-planning/)\n- Python support: >= 3.7, pypy\n- Source: <https://github.com/cihai/cihai>\n- Docs: <https://cihai.git-pull.com>\n- Changelog: <https://cihai.git-pull.com/history.html>\n- API: <https://cihai.git-pull.com/api.html>\n- Issues: <https://github.com/cihai/cihai/issues>\n- Test coverage: <https://codecov.io/gh/cihai/cihai>\n- pypi: <https://pypi.python.org/pypi/cihai>\n- OpenHub: <https://www.openhub.net/p/cihai>\n- License: MIT\n\n[![Docs](https://github.com/cihai/cihai/workflows/docs/badge.svg)](https://cihai.git-pull.com/)\n[![Build Status](https://github.com/cihai/cihai/workflows/tests/badge.svg)](https://github.com/cihai/cihai/actions?query=workflow%3A%22tests%22)\n',
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cihai.git-pull.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
