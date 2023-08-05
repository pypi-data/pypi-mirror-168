# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['docutils>=0.18.0,<0.19.0', 'myst_parser']

entry_points = \
{'pytest11': ['sphinx = pytest_doctest_docutils']}

setup_kwargs = {
    'name': 'gp-libs',
    'version': '0.0.1a11',
    'description': 'Internal utilities for projects following git-pull python package spec',
    'long_description': '# gp-libs &middot; [![Python Package](https://img.shields.io/pypi/v/gp-libs.svg)](https://pypi.org/project/gp-libs/) [![License](https://img.shields.io/github/license/git-pull/gp-libs.svg)](https://github.com/git-pull/gp-libs/blob/master/LICENSE) [![Code Coverage](https://codecov.io/gh/git-pull/gp-libs/branch/master/graph/badge.svg)](https://codecov.io/gh/git-pull/gp-libs)\n\nIncubating / [dogfooding] some sphinx extensions and pytest plugins on\ngit-pull projects, e.g. [cihai], [vcs-python], or [tmux-python].\n\n[dogfooding]: https://en.wikipedia.org/wiki/Eating_your_own_dog_food\n[cihai]: https://github.com/cihai\n[vcs-python]: https://github.com/vcs-python\n[tmux-python]: https://github.com/tmux-python\n\n## `doctest` for reStructured and markdown\n\nTwo components:\n\n1. `doctest_docutils` module: Same specification as `doctest`, but can parse reStructuredText\n   and markdown\n2. `pytest_doctest_docutils`: Pytest plugin, collects test items for pytest for reStructuredText and markdown files\n\n   This means you can do:\n\n   ```console\n   $ pytest docs\n   ```\n\n### doctest module\n\nThis extends standard library `doctest` to support anything docutils can parse.\nIt can parse reStructuredText (.rst) and markdown (.md).\n\nSee more: <https://gp-libs.git-pull.com/doctest/>\n\n#### Supported styles\n\nIt supports two barebones directives:\n\n- docutils\' `doctest_block`\n\n  ```rst\n  >>> 2 + 2\n  4\n  ```\n\n- `.. doctest::` directive\n\n  reStructuredText:\n\n  ```rst\n  .. doctest::\n\n     >>> 2 + 2\n     4\n  ```\n\n  Markdown (requires [myst-parser]):\n\n  ````markdown\n  ```{doctest}\n  >>> 2 + 2\n  4\n  ```\n  ````\n\n[myst-parser]: https://myst-parser.readthedocs.io/en/latest/\n\n#### Usage\n\nThe `doctest_docutils` module preserves standard library\'s usage conventions:\n\n##### reStructuredText\n\n```console\n$ python -m doctest_docutils README.rst -v\n```\n\nThat\'s what `doctest` does by design.\n\n##### Markdown\n\nIf you install [myst-parser], doctest will run on .md files.\n\n```console\n$ python -m doctest_docutils README.md -v\n```\n\n### pytest plugin\n\n_This plugin disables [pytest\'s standard `doctest` plugin]._\n\nThis plugin integrates with the `doctest_docutils` module with pytest to enable seamless testing of docs, `conftest.py` fixtures and all.\n\n```console\n$ pytest docs/\n```\n\nLike the above module, it supports docutils\' own `doctest_block` and a basic\n`.. doctest::` directive.\n\nSee more: <https://gp-libs.git-pull.com/doctest/pytest.html>\n\n[pytest\'s standard `doctest` plugin]: https://docs.pytest.org/en/stable/how-to/doctest.html#doctest\n\n## sphinx plugins\n\n### Plain-text issue linker (`linkify-issues`)\n\nWe need to parse plain text, e.g. #99999, to point to the project tracker at\nhttps://github.com/git-pull/gp-libs/issues/99999. This way the markdown looks\ngood anywhere you render it, including GitHub and GitLab.\n\n#### Configuration\n\nIn your _conf.py_:\n\n1. Add `\'linkify_issues\'` to `extensions`\n\n   ```python\n   extensions = [\n       # ...\n       "linkify_issues",\n   ]\n   ```\n\n2. Configure your issue URL, `issue_url_tpl`:\n\n   ```python\n   # linkify_issues\n   issue_url_tpl = \'https://github.com/git-pull/gp-libs/issues/{issue_id}\'\n   ```\n\n   The config variable is formatted via {meth}`str.format` where `issue_id` is\n   `42` if the text is \\#42.\n\nSee more: <https://gp-libs.git-pull.com/linkify_issues/>\n\n### Table of contents for autodoc\n\n`sphinx.ext.autodoc` doesn\'t link objects in the table of contents. So we need a\nplugin to help.\n\nSee more: <https://gp-libs.git-pull.com/sphinx_toctree_autodoc_fix/>\n\n#### Configuration\n\n1. Add `\'sphinx_toctree_autodoc_fix\'` to `extensions`\n\n   ```python\n   extensions = [\n       # ...\n       "sphinx_toctree_autodoc_fix",\n   ]\n   ```\n\n## Install\n\n```console\n$ pip install --user gp-libs\n```\n\n### Developmental releases\n\nYou can test the unpublished version of g before its released.\n\n- [pip](https://pip.pypa.io/en/stable/):\n\n  ```console\n  $ pip install --user --upgrade --pre gp-libs\n  ```\n\n# More information\n\n- Python support: >= 3.7, pypy\n- Source: <https://github.com/git-pull/gp-libs>\n- Docs: <https://gp-libs.git-pull.com>\n- Changelog: <https://gp-libs.git-pull.com/history.html>\n- Issues: <https://github.com/git-pull/gp-libs/issues>\n- Test Coverage: <https://codecov.io/gh/git-pull/gp-libs>\n- pypi: <https://pypi.python.org/pypi/gp-libs>\n- License: [MIT](https://opensource.org/licenses/MIT).\n\n[![Docs](https://github.com/git-pull/gp-libs/workflows/docs/badge.svg)](https://gp-libs.git-pull.com)\n[![Build Status](https://github.com/git-pull/gp-libs/workflows/tests/badge.svg)](https://github.com/git-pull/gp-libs/actions?query=workflow%3A%22tests%22)\n',
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gp-libs.git-pull.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
