#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Use spaCy to Parse Input Tokens """


from baseblock import Stopwatch  # type: ignore
from baseblock import BaseObject  # type: ignore

from spacy_token_parser.dmo import TokenParserSpacy
from spacy_token_parser.dmo import TokenParserWordnet
from spacy_token_parser.dmo import TokenParserNormalize
from spacy_token_parser.dmo import TokenParserPunctuation
from spacy_token_parser.dmo import TokenParserCoordinates
from spacy_token_parser.dmo import TokenParserSquots
from spacy_token_parser.dmo import TokenParserResultSet
from spacy_token_parser.dmo import TokenParserPostProcess

from spacy_token_parser.dto.typedefs import InputTokens
from spacy_token_parser.dto.typedefs import ParseInputTokensResult


class ParseInputTokens(BaseObject):
    """ Use spaCy to Parse Input Tokens """

    def __init__(self):
        """ Change Log

        Created:
            1-Oct-2021
            craigtrim@gmail.com
        Updated:
            13-Oct-2021
            craigtrim@gmail.com
            *   refactored into component parts in pursuit of
                https://github.com/grafflr/graffl-core/issues/41
        Updated:
            16-Sept-2022
            craigtrim@gmail.com
            *   integrate 'token-parser-postprocess'
                https://github.com/craigtrim/spacy-token-parser/issues/3
            *   rename all components
                https://github.com/craigtrim/spacy-token-parser/issues/3
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                tokens: InputTokens) -> ParseInputTokensResult:

        sw = Stopwatch()

        tokens = TokenParserSquots().process(tokens)
        doc = TokenParserSpacy().process(' '.join(tokens))

        results = TokenParserResultSet().process(doc)
        results = TokenParserPunctuation().process(results)
        results = TokenParserNormalize().process(results)
        results = TokenParserCoordinates().process(results)
        results = TokenParserWordnet().process(results)
        results = TokenParserPostProcess().process(results)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Input Token Parsing Completed",
                f"\tTotal Tokens: {len(results)}",
                f"\tTotal Time: {str(sw)}"]))

        return {
            'tokens': results,
            'doc': doc
        }
