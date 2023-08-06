# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacy_token_parser',
 'spacy_token_parser.dmo',
 'spacy_token_parser.dto',
 'spacy_token_parser.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'nltk==3.7', 'spacy==3.3', 'wordnet-lookup']

setup_kwargs = {
    'name': 'spacy-token-parser',
    'version': '0.1.12',
    'description': 'Use spaCy to Parse Input Tokens',
    'long_description': '# spaCy Token Parser (spacy-token-parser)\nUse spaCy to Parse Input Tokens\n\n## Usage\n\nCall the service with this code\n```python\nfrom spacy_token_parser import parse_tokens\n\nparse_tokens(input_text.split())\n```\n\nThe output is a tuple.\n\nThe first element of the tuple is a list of dictionary tokens (below).  \n\nThe second element of the tuple is a wrapped instance of `spacy.tokens.doc.Doc`.\n\n### List Output\n```json\n[\n   {\n      "dep":"compound",\n      "ent":"NORP",\n      "head":"5665575797947403677",\n      "id":"6042939320535660714",\n      "is_alpha":true,\n      "is_punct":false,\n      "is_stop":false,\n      "is_wordnet":true,\n      "lemma":"american",\n      "noun_number":"singular",\n      "other":{\n         "head_i":3,\n         "head_idx":24,\n         "head_orth":5665575797947403677,\n         "head_text":"films",\n         "i":0,\n         "idx":0,\n         "orth":6042939320535660714\n      },\n      "pos":"PROPN",\n      "sentiment":0.0,\n      "shape":"xxxx",\n      "tag":"NNP",\n      "tense":"",\n      "text":"american",\n      "verb_form":"",\n      "x":0,\n      "y":8\n   },\n   {\n      "dep":"compound",\n      "ent":"",\n      "head":"5665575797947403677",\n      "id":"16602643206033239142",\n      "is_alpha":true,\n      "is_punct":false,\n      "is_stop":false,\n      "is_wordnet":true,\n      "lemma":"silent",\n      "noun_number":"singular",\n      "other":{\n         "head_i":3,\n         "head_idx":24,\n         "head_orth":5665575797947403677,\n         "head_text":"films",\n         "i":1,\n         "idx":9,\n         "orth":16602643206033239142\n      },\n      "pos":"PROPN",\n      "sentiment":0.0,\n      "shape":"xxxx",\n      "tag":"NNP",\n      "tense":"",\n      "text":"silent",\n      "verb_form":"",\n      "x":8,\n      "y":14\n   },\n   {\n      "dep":"compound",\n      "ent":"",\n      "head":"5665575797947403677",\n      "id":"16417888112635110788",\n      "is_alpha":true,\n      "is_punct":false,\n      "is_stop":false,\n      "is_wordnet":true,\n      "lemma":"feature",\n      "noun_number":"singular",\n      "other":{\n         "head_i":3,\n         "head_idx":24,\n         "head_orth":5665575797947403677,\n         "head_text":"films",\n         "i":2,\n         "idx":16,\n         "orth":16417888112635110788\n      },\n      "pos":"NOUN",\n      "sentiment":0.0,\n      "shape":"xxxx",\n      "tag":"NN",\n      "tense":"",\n      "text":"feature",\n      "verb_form":"",\n      "x":14,\n      "y":21\n   },\n   {\n      "dep":"ROOT",\n      "ent":"",\n      "head":"5665575797947403677",\n      "id":"5665575797947403677",\n      "is_alpha":true,\n      "is_punct":false,\n      "is_stop":false,\n      "is_wordnet":true,\n      "lemma":"film",\n      "noun_number":"plural",\n      "other":{\n         "head_i":3,\n         "head_idx":24,\n         "head_orth":5665575797947403677,\n         "head_text":"films",\n         "i":3,\n         "idx":24,\n         "orth":5665575797947403677\n      },\n      "pos":"NOUN",\n      "sentiment":0.0,\n      "shape":"xxxx",\n      "tag":"NNS",\n      "tense":"",\n      "text":"films",\n      "verb_form":"",\n      "x":21,\n      "y":26\n   }\n]\n```',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://python-poetry.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)
