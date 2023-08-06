# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat_sentencebreak']

package_data = \
{'': ['*']}

install_requires = \
['mdformat>=0.7.16,<0.8.0']

entry_points = \
{'mdformat.parser_extension': ['sentencebreak = mdformat_sentencebreak:plugin']}

setup_kwargs = {
    'name': 'mdformat-sentencebreak',
    'version': '0.1.0',
    'description': 'Adds a really simple and naive sentence breaking scheme to mdformat',
    'long_description': '# mdformat-sentencebreak\n\nAn [mdformat](https://github.com/executablebooks/mdformat) plugin that adds line wrapping based on sentence completion marks.\n\n## Behavior\n\nThis input ....\n\n```text\n> Long sentences are broken at punctuation marks,\n> unless the generated sentence would be extremely small\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.\n\n> And it will not break sentences if\n> they are inside something else ... emphasis for example\n**Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.**\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.\n**Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.**\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.\n\n> Sentences are kept separate if they end in punctuation\n\nSome.\nVery.\nSmall.\nSeries.\nof.\nSentences.\n\n> Sentences are combined if they do not end in punctuation.\n\na\nvery\nsloppy\nsentence\n\n```\n\nWill get this ....\n\n```\nLorem ipsum dolor sit amet,\nconsectetur adipiscing elit,\nsed do eiusmod tempor incididunt ut labore et dolore magna.\n\n**Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.**\n\nLorem ipsum dolor sit amet,\nconsectetur adipiscing elit,\nsed do eiusmod tempor incididunt ut labore et dolore magna.\n**Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.**\nLorem ipsum dolor sit amet,\nconsectetur adipiscing elit,\nsed do eiusmod tempor incididunt ut labore et dolore magna.\n\nSome.\nVery.\nSmall.\nSeries.\nof.\nSentences.\n\na very sloppy sentence\n```\n\n## Installation\n\n> pip install {{NOT YET PUBLISHED}}\n',
    'author': 'J. Sebastian Paez',
    'author_email': 'jspaezp@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
