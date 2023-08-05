# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Normalize Input Text """


from functools import lru_cache

from baseblock import BaseObject


class Normalizer(BaseObject):
    """ Normalize Input Text """

    __hyphens = {
        "\u058a": "U+058A",
        "\u1806": "U+1806",
        "\u2010": "U+2010",
        "\u2011": "U+2011",
        "\u2012": "U+2012",
        "\u2013": "U+2013",
        "\u2014": "U+2014",
        "\u2015": "U+2015",
        "\u2053": "U+2053",
        "\u207b": "U+207B",
        "\u208b": "U+208B",
        "\u2212": "U+2212",
        "\u2e3a": "U+2E3A",
        "\u2e3b": "U+2E3B",
        "\u301c": "U+301C",
        "\u3030": "U+3030",
        "\ufe58": "U+FE58",
        "\ufe63": "U+FE63",
        "\uff0d": "U+FF0D"
    }

    __squotes = [
        "\u2019",
        "\u2018",
        "\u201b",
        "`"
    ]

    __dquotes = [
        "\u201c",
        "\u201d",
        "\u00ab",
        "\u00bb",
        "\u201e",
        "``",
        "\u00b4\u00b4"
    ]

    def __init__(self):
        """ Change Log

        Created:
            1-Oct-2021
            craigtrim@gmail.com
        Updated:
            31-Aug-2022
            craigtrim@gmail.com
            *   simplify normalization package
        Updated:
            16-Sept-2022
            craigtrim@gmail.com
            *   migrate to 'spacy-token-parse' and hard-code dictionaries
                https://github.com/craigtrim/spacy-token-parser/issues/2
        """
        BaseObject.__init__(self, __name__)

    @lru_cache(maxsize=1024, typed=True)
    def process(self,
                input_text: str) -> str:

        if type(input_text) != str:
            raise ValueError

        hyphens = [x for x in self.__hyphens if x in input_text]
        for hyphen in hyphens:
            input_text = input_text.replace(hyphen, '-')

        dquotes = [x for x in self.__dquotes if x in input_text]
        for dquote in dquotes:
            input_text = input_text.replace(dquote, '"')

        squotes = [x for x in self.__squotes if x in input_text]
        for squote in squotes:
            input_text = input_text.replace(squote, "'")

        return input_text.strip().lower()
