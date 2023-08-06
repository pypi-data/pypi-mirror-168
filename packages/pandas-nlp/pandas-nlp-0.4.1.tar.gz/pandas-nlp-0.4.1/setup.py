# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_nlp']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'fasttext>=0.9.2,<0.10.0',
 'pandas>=1.3.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'spacy>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'pandas-nlp',
    'version': '0.4.1',
    'description': 'Pandas extension with NLP functionalities',
    'long_description': '# NLP Pandas\n\nIt\'s an extension for pandas providing some NLP functionalities for strings.\n\n[![build](https://github.com/jaume-ferrarons/pandas-nlp/actions/workflows/push-event.yml/badge.svg?branch=master)](https://github.com/jaume-ferrarons/pandas-nlp/actions/workflows/push-event.yml)\n[![version](https://img.shields.io/pypi/v/pandas_nlp?logo=pypi&logoColor=white)](https://pypi.org/project/pandas-nlp/)\n\n## Installation\n\nInstall with:\n```bash\npip install -U pandas-nlp\n```\n\n### Requirements \n- python >= 3.8\n\n## Key features\n\n### Language detection\n```python\nimport pandas as pd\nimport pandas_nlp\n\ndf = pd.DataFrame({\n    "id": [1, 2, 3, 4, 5],\n    "text": [\n        "I like cats",\n        "Me gustan los gatos",\n        "M\'agraden els gats",\n        "J\'aime les chats",\n        "Ich mag Katzen",\n    ],\n})\ndf.text.nlp.language()\n```\n**Output**\n```\n0    en\n1    es\n2    ca\n3    fr\n4    de\nName: text_language, dtype: object\n```\n\n### String embedding\n```python\nimport pandas as pd\nimport pandas_nlp\n\ndf = pd.DataFrame(\n    {"id": [1, 2, 3], "text": ["cat", "dog", "violin"]}\n)\ndf.text.nlp.embedding()\n```\n**Output**\n```\n0    [2.0860276, 0.78038394, 0.20159146, -1.2828196...\n1    [0.96052396, 1.0350337, 0.11549556, -1.2252672...\n2    [1.2934866, 0.10021937, 0.71453714, -1.3288003...\nName: text_embedding, dtype: object\n```\n\n### String embedding\n```python\nimport pandas as pd\nimport pandas_nlp\n\ndf = pd.DataFrame(\n    {"id": [0, 1], "text": ["Hello, how are you?", "Code. Sleep. Eat"]}\n)\ndf.text.nlp.sentences()\n```\n**Output**\n```python\n0    [Hello, how are you?]\n1     [Code., Sleep., Eat]\nName: text_sentences, dtype: object\n```',
    'author': 'Jaume Ferrarons',
    'author_email': 'jaume.ferrarons@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jaume-ferrarons/pandas-nlp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
