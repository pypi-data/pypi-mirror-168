# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markdown_callouts']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.3,<4.0.0']

entry_points = \
{'markdown.extensions': ['callouts = markdown_callouts:CalloutsExtension']}

setup_kwargs = {
    'name': 'markdown-callouts',
    'version': '0.3.0',
    'description': 'Markdown extension: a classier syntax for admonitions',
    'long_description': '# markdown-callouts\n\n**Extension for [Python-Markdown][]: a classier syntax for [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#usage)**\n\n[![PyPI](https://img.shields.io/pypi/v/markdown-callouts)](https://pypi.org/project/markdown-callouts/)\n[![GitHub](https://img.shields.io/github/license/oprypin/markdown-callouts)](https://github.com/oprypin/markdown-callouts/blob/master/LICENSE.md)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/oprypin/markdown-callouts/CI)](https://github.com/oprypin/markdown-callouts/actions?query=event%3Apush+branch%3Amaster)\n\n[python-markdown]: https://python-markdown.github.io/\n[admonition]: https://python-markdown.github.io/extensions/admonition/\n[mkdocs]: https://www.mkdocs.org/\n[documentation site]: https://oprypin.github.io/markdown-callouts/\n\n## Installation\n\n```shell\npip install markdown-callouts\n```\n\nIf using MkDocs, [enable the extension in **mkdocs.yml**](https://www.mkdocs.org/user-guide/configuration/#markdown_extensions):\n\n```yaml\nmarkdown_extensions:\n  - callouts\n```\n\n**Continue to the [documentation site][].**\n\n## Usage\n\nThis adds a new block-level syntax to Markdown, to put a paragraph of text into a block that\'s specially highlighted and set apart from the rest of the text.\n\n**Example:**\n\n```markdown\nNOTE: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod\nnulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor\nmassa, nec semper lorem quam in massa.\n```\n\n**Result**, [using *mkdocs-material*](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#usage):\n\n![Screenshot](https://user-images.githubusercontent.com/371383/119063216-dc001700-b9d8-11eb-8092-763e5d02d9f4.png)\n\nCollapsible blocks also have a syntax for them:\n\n```markdown\n>? NOTE: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod\n> nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor\n> massa, nec semper lorem quam in massa.\n```\n\nThis instead shows up as an initially-closed `<details>` block.\n\n### Graceful degradation\n\nThis extension produces the same results as the *[admonition][]* extension, but with a syntax that is much less intrusive and has a very reasonable fallback look for "vanilla" renderers.\n\nE.g. compare what you would\'ve seen above if we actually wrote that Markdown and fed it to GitHub\'s Markdown parser:\n\n<table markdown="1">\n<tr><th>"Callouts" syntax</th></tr>\n<tr><td>\n\nNOTE: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod\nnulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor\nmassa, nec semper lorem quam in massa.\n\n</td></tr>\n<tr><th>"Admonition" syntax</th></tr>\n<tr><td>\n\n!!! note\n\n    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod\n    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor\n    massa, nec semper lorem quam in massa.\n\n</td></tr>\n</table>\n\n---\n\n**Continue to the [documentation site][].**\n',
    'author': 'Oleh Prypin',
    'author_email': 'oleh@pryp.in',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/oprypin/markdown-callouts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
