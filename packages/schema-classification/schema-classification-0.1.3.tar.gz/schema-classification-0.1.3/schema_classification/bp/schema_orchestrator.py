#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore[import]
# type: ignore[func-returns-value]
""" Portendo performs Predictive Classification of deepNLU parsed ASTs """


import os
from pprint import pformat

from typing import List

from baseblock import FileIO
from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject

from schema_classification.svc import ReadMapping
from schema_classification.svc import PredictMapping
from schema_classification.svc import SelectMapping
from schema_classification.dmo import InputTokensTransform
from schema_classification.dto import ServiceEvent


class SchemaOrchestrator(BaseObject):
    """ Portendo performs Predictive Classification of deepNLU parsed ASTs

    This Orchestration sequence requires a pre-written schema for classification
    Pre-written schemas are more complex and are capable of nuanced classification
    """

    def __init__(self,
                 schema_file: str):
        """Initialize Portendo API

        Created:
            7-Feb-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/169
        Updated:
            8-Jun-2022
            craigtrim@gmail.com
            *   make absolute_path a required parameter in pursuit of
                https://github.com/grafflr/deepnlu/issues/44
            *   read classifications from memory (not python files)
                https://github.com/grafflr/deepnlu/issues/45
        Updated:
            13-Jul-2022
            craigtrim@gmail.com
            *   renamed from 'portendo' in pursuit of
                https://github.com/grafflr/deepnlu/issues/48
        Updated:
            26-Jul-2022
            craigtrim@gmail.com
            *   remove 'schema-name' and 'absolute-path' as parameters, and instead
                pass the full absolute path of a schema file, in pursuit of
                https://bast-ai.atlassian.net/browse/COR-12
            *   document the schema-file to schema-name mapping convention
                https://bast-ai.atlassian.net/browse/COR-13

        Args:
            schema_file (str): the absolute path to a local schema file containing classification rules
        """
        BaseObject.__init__(self, __name__)
        if self.isEnabledForDebug:
            Enforcer.is_str(schema_file)
            FileIO.exists_or_error(schema_file)

        self._schema_name = os.path.basename(
            schema_file).split('-')[0].strip()  # COR-13

        self._d_index = ReadMapping(schema_file).index()

    def _run(self,
             input_tokens: List[str]) -> ServiceEvent:

        d_tokens = InputTokensTransform(input_tokens).process()
        input_tokens = [x for x in d_tokens]

        svcresult = {
            'transform': d_tokens,
            'input': input_tokens
        }

        mapping_result_dict = PredictMapping(
            d_index=self._d_index,
            ontology_name=self._schema_name).process(svcresult)

        mapping = SelectMapping(
            results=mapping_result_dict,
            d_index=self._d_index).process()

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                "Mapping Completed",
                f"\tInput:\n{pformat(input_tokens)}",
                f"\tOutput:\n{pformat(mapping)}"]))

        if not len(mapping):
            return {
                'result': None,
                'tokens': d_tokens
            }

        return {
            'result': mapping,
            'tokens': d_tokens
        }

    def run(self,
            input_tokens: list) -> ServiceEvent:
        """ Run the Schema Orchestrator on Input Tokens

        Args:
            input_tokens (list): a flat list of tokens extracted from text
            Sample Input:
                ['network_topology', 'user', 'customer']

        Returns:
            tuple: the service result
        """

        sw = Stopwatch()

        svcresult = self._run(input_tokens)

        self.logger.info('\n'.join([
            "Portendo Schema Orchestrator Completed",
            f"\tTotal Time: {str(sw)}",
            f"\tResult:\n{pformat(svcresult)}"]))

        return svcresult
