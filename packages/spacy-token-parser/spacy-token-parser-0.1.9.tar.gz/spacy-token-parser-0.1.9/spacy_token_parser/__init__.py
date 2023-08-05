from .dmo import *
from .svc import *
from .dto import *

from .dto.project_types import InputTokens
from .dto.project_types import ParseResults
from .dto.project_types import DependencyGraph
from .dto.project_types import ParseInputTokensResult

from .svc.parse_input_tokens import ParseInputTokens
from .svc.create_graph_structure import CreateGraphStructure

__parse = ParseInputTokens().process
__tograph = CreateGraphStructure().process


def parse_tokens(tokens: InputTokens) -> ParseInputTokensResult:
    return __parse(tokens)


def to_graph(results: ParseResults) -> DependencyGraph:
    return __tograph(results)
