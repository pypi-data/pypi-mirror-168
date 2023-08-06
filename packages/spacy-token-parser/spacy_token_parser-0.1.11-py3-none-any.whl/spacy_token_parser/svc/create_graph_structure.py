#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Transform NLU results into a Graph Structure """


from baseblock import BaseObject  # type: ignore
from typing import Any
from typing import List
from typing import Dict
from typing import Tuple
from typing import TypedDict

from spacy.tokens import Doc
from spacy_token_parser.dto.typedefs import ParseResults
from spacy_token_parser.dto.typedefs import DependencyGraph


class CreateGraphStructure(BaseObject):
    """ Transform NLU results into a Graph Structure

    The output is a dictionary with 'nodes' and 'edges'
    """

    def __init__(self):
        """ Change Log

        Created:
            2-Sept-2022
            craigtrim@gmail.com
        Updated:
            17-Sept-2022
            craigtrim@gmail.com
            *   migrated to 'spacy-token-parser'
        """
        BaseObject.__init__(self, __name__)

    @staticmethod
    def _transform_token_type(d_token: dict) -> dict:
        return {
            "ID": d_token['id'],
            "Label": d_token['text'],
            "PartOfSpeech": d_token['pos'],
            "Tag": d_token['tag'],
            "Dependency": d_token['dep'],
            "Shape": d_token['shape'],
            "Coords": f"{d_token['x']}, {d_token['y']}",
            "Stemmed": d_token['stem'],
            "OriginalText": d_token['text'],
            "NormalizedText": d_token['normal'],
            "Type": "TOKEN",
            "head": d_token['head'],
            "other": d_token['other'],
        }

    @staticmethod
    def _transform_ent_type(ent_id: str,
                            d_token: dict) -> dict:
        return {
            "ID": ent_id,
            "Label": d_token['ent'],
            "OriginalText": d_token['ent'],
            "Type": "ENT",
        }

    @staticmethod
    def _transform_swap_type(swap_token_id: str,
                             d_token: dict) -> dict:
        return {
            "ID": swap_token_id,
            "Label": d_token['swaps']['canon'],
            "Coords": f"{d_token['x']}, {d_token['y']}",
            "Canon": d_token['swaps']['canon'],
            "OriginalText": d_token['text'],
            "Confidence": d_token['swaps']['confidence'],
            "Type": "SWAP",
        }

    @staticmethod
    def _transform_ontology_type(ontology_id: str,
                                 ontology_name: str) -> dict:
        return {
            "ID": ontology_id,
            "Label": ontology_name,
            "Name": ontology_name,
            "Type": "ONTOLOGY",
        }

    @staticmethod
    def _generate_edge(start_id: str, end_id: str, name: str) -> dict:
        return {
            "start": start_id,
            "end": end_id,
            "name": name
        }

    def process(self,
                results: ParseResults) -> DependencyGraph:
        """ Entry Point

        Args:
            results (list): the deepNLU results

        Returns:
            list: a flat list
        """

        edges = []  # relationships (edges) between nodes

        ent_nodes = []  # promote ENT attributes as nodes
        swap_nodes = []  # swap nodes created in synonym processing
        token_nodes = []  # actual tokens during tokenization phase
        ontology_nodes = []  # promote ontology names as nodes

        def add_token(d_token: dict) -> None:
            token_nodes.append(self._transform_token_type(d_token))

            edges.append(self._generate_edge(
                d_token['id'], d_token['head'], 'dependency'))

            if len(d_token['ent']):
                ent_id = f"ENT_{d_token['ent'].upper()}"
                ent_nodes.append(self._transform_ent_type(ent_id, d_token))

                edges.append(self._generate_edge(
                    d_token['id'], ent_id, 'is-type-of'))

        def add_swap_node(d_token: dict) -> None:
            swap_token_id = f"SWAP_{d_token['id']}"
            swap_nodes.append(
                self._transform_swap_type(swap_token_id, d_token))

            for token in d_token['swaps']['tokens']:
                edges.append(self._generate_edge(
                    swap_token_id, token['id'], 'composed-of'))

            for ontology_name in d_token['swaps']['ontologies']:
                ontology_id = f"OWL_{ontology_name.upper()}"
                ontology_nodes.append(self._transform_ontology_type(
                    ontology_id=ontology_id,
                    ontology_name=ontology_name))

                edges.append(self._generate_edge(
                    swap_token_id, ontology_id, 'has-provenance'))

        def iterate_token(token: dict):

            def is_plain_token() -> bool:
                return 'swaps' not in token

            if is_plain_token():
                add_token(token)
            else:
                add_swap_node(token)
                [iterate_token(x) for x in token['swaps']['tokens']]

        for i in range(len(results)):
            paragraph = results[i]

            for j in range(len(paragraph)):
                sentence = paragraph[j]

                for token in sentence:
                    iterate_token(token)

        return {
            'edges': edges,
            'nodes': {
                'entities': ent_nodes,
                'tokens': token_nodes,
                'swaps': swap_nodes,
                'ontologies': ontology_nodes
            }
        }
