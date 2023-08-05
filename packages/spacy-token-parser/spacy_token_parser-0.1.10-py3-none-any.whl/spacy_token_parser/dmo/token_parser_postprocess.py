#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Add Wordnet Flag to Token """


from baseblock import BaseObject


from spacy_token_parser.dto import Stemmer
from spacy_token_parser.dto import Normalizer


class TokenParserPostProcess(BaseObject):
    """ Post Process an """

    def __init__(self):
        """ Change Log

        Created:
            16-Sept-2022
            craigtrim@gmail.com
            *   handle post-processing
                https://github.com/craigtrim/spacy-token-parser/issues/2
            *   rename component
                https://github.com/craigtrim/spacy-token-parser/issues/3
        """
        BaseObject.__init__(self, __name__)
        self._stem = Stemmer().input_text
        self._normalize = Normalizer().process

    def process(self,
                tokens: list) -> list:

        for d_token in tokens:
            ## ---------------------------------------------------------- ##
            # Update:       DO NOT use lemma as basis for 'normal' form
            # Reference:    https://github.com/craigtrim/spacy-token-parser/issues/2
            #               https://github.com/grafflr/graffl-core/issues/46#issuecomment-943708492
            # Old Code:     self._normalizer.input_text(token['lemma'])
            ## ---------------------------------------------------------- ##
            d_token['normal'] = self._normalize(d_token['text'])

            if d_token['is_punct']:
                d_token['stem'] = d_token['normal']
            else:
                d_token['stem'] = str(
                    self._stem(d_token['normal']))
            del d_token['lemma']

        return tokens
