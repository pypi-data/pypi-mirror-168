# spaCy Token Parser (spacy-token-parser)
Use spaCy to Parse Input Tokens

## Usage

Call the service with this code
```python
from spacy_token_parser import parse_tokens

parse_tokens(input_text.split())
```

The output is a tuple.

The first element of the tuple is a list of dictionary tokens (below).  

The second element of the tuple is a wrapped instance of `spacy.tokens.doc.Doc`.

### List Output
```json
[
   {
      "dep":"compound",
      "ent":"NORP",
      "head":"5665575797947403677",
      "id":"6042939320535660714",
      "is_alpha":true,
      "is_punct":false,
      "is_stop":false,
      "is_wordnet":true,
      "lemma":"american",
      "noun_number":"singular",
      "other":{
         "head_i":3,
         "head_idx":24,
         "head_orth":5665575797947403677,
         "head_text":"films",
         "i":0,
         "idx":0,
         "orth":6042939320535660714
      },
      "pos":"PROPN",
      "sentiment":0.0,
      "shape":"xxxx",
      "tag":"NNP",
      "tense":"",
      "text":"american",
      "verb_form":"",
      "x":0,
      "y":8
   },
   {
      "dep":"compound",
      "ent":"",
      "head":"5665575797947403677",
      "id":"16602643206033239142",
      "is_alpha":true,
      "is_punct":false,
      "is_stop":false,
      "is_wordnet":true,
      "lemma":"silent",
      "noun_number":"singular",
      "other":{
         "head_i":3,
         "head_idx":24,
         "head_orth":5665575797947403677,
         "head_text":"films",
         "i":1,
         "idx":9,
         "orth":16602643206033239142
      },
      "pos":"PROPN",
      "sentiment":0.0,
      "shape":"xxxx",
      "tag":"NNP",
      "tense":"",
      "text":"silent",
      "verb_form":"",
      "x":8,
      "y":14
   },
   {
      "dep":"compound",
      "ent":"",
      "head":"5665575797947403677",
      "id":"16417888112635110788",
      "is_alpha":true,
      "is_punct":false,
      "is_stop":false,
      "is_wordnet":true,
      "lemma":"feature",
      "noun_number":"singular",
      "other":{
         "head_i":3,
         "head_idx":24,
         "head_orth":5665575797947403677,
         "head_text":"films",
         "i":2,
         "idx":16,
         "orth":16417888112635110788
      },
      "pos":"NOUN",
      "sentiment":0.0,
      "shape":"xxxx",
      "tag":"NN",
      "tense":"",
      "text":"feature",
      "verb_form":"",
      "x":14,
      "y":21
   },
   {
      "dep":"ROOT",
      "ent":"",
      "head":"5665575797947403677",
      "id":"5665575797947403677",
      "is_alpha":true,
      "is_punct":false,
      "is_stop":false,
      "is_wordnet":true,
      "lemma":"film",
      "noun_number":"plural",
      "other":{
         "head_i":3,
         "head_idx":24,
         "head_orth":5665575797947403677,
         "head_text":"films",
         "i":3,
         "idx":24,
         "orth":5665575797947403677
      },
      "pos":"NOUN",
      "sentiment":0.0,
      "shape":"xxxx",
      "tag":"NNS",
      "tense":"",
      "text":"films",
      "verb_form":"",
      "x":21,
      "y":26
   }
]
```