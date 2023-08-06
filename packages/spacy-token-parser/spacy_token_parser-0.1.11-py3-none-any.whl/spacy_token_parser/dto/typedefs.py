#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Define Strict Types for the Project """


from typing import Any
from typing import List
from typing import Dict
from typing import Tuple
from typing import TypedDict

from spacy.tokens import Doc


class DependencyNodes(TypedDict):
    entities: List[Any]
    tokens: List[Any]
    swaps: List[Any]
    ontologies: List[Any]


class DependencyGraph(TypedDict):
    edges: List
    nodes: DependencyNodes


InputTokens = List[str]

ParseResults = List[Dict[Any, Any]]


# Service Output from `ParseInputTokens`
class ParseInputTokensResult(TypedDict):
    tokens: ParseResults
    doc: Doc
