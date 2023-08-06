from .bp import *
from .svc import *
from .dmo import *
from .dto import *


def classify(absolute_path: str,
             input_tokens: list) -> dict:
    """ Run the Schema Orchestrator

    Args:
        absolute_path (str): absolute path to the location of the classification rules
        input_tokens (list): a flat list of tokens extracted from text
            Sample Input:
                ['network_topology', 'user', 'customer']
    """
    run = SchemaOrchestrator(
        schema_file=absolute_path).run

    svcresult = run(input_tokens)

    return svcresult
