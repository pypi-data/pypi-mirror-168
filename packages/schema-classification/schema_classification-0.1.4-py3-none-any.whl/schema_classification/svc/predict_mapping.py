#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore[import]
# type: ignore[func-returns-value]
"""Predict a Mapping"""


from pprint import pformat

from baseblock import Stopwatch
from baseblock import BaseObject
from baseblock import Enforcer

from schema_classification.dto import NormalizedSchema
from schema_classification.dto import MappingResultDict

from schema_classification.dto import ExplainResult
from schema_classification.dto import MappingResult
from schema_classification.dto import MappingResults
from schema_classification.dmo import ComputerIncludeOneOf
from schema_classification.dmo import ComputerIncludeRecursive
from schema_classification.dmo import ComputerIncludeAllOf
from schema_classification.dmo import ComputerExcludeOneOf
from schema_classification.dmo import ComputerExcludeAllOf
from schema_classification.dmo import ConfidenceExcludeAllOf
from schema_classification.dmo import ConfidenceIncludeAllOf
from schema_classification.dmo import ComputerStartsWith


class PredictMapping(BaseObject):
    """Predict a Mapping"""

    def __init__(self,
                 ontology_name: str,
                 d_index: NormalizedSchema):
        """ Initialize Service

        Created:
            7-Feb-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/169
        Updated:
            8-Jun-2022
            craigtrim@gmail.com
            *   read schema in-memory
                https://github.com/grafflr/deepnlu/issues/45

        Args:
            ontology_name (str):
            d_index (dict): the indexed schema
        """
        BaseObject.__init__(self, __name__)
        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                "Initialized Service",
                f"\tOntology Name: {ontology_name}"]))

        self._include_one_of = ComputerIncludeOneOf(d_index).process
        self._include_all_of = ComputerIncludeAllOf(d_index).process
        self._exclude_one_of = ComputerExcludeOneOf(d_index).process
        self._exclude_all_of = ComputerExcludeAllOf(d_index).process
        self._startswith = ComputerStartsWith(d_index).process

    def _process(self,
                 d_tokens: dict) -> MappingResultDict:
        mapping_results = []

        sw = Stopwatch()

        d_transform = d_tokens['transform']  # has token:canon mapping
        d_input = d_tokens['input']  # just text tokens

        m_include_oneof = self._include_one_of(d_transform)
        m_include_allof = self._include_all_of(d_transform)
        m_exclude_oneof = self._exclude_one_of(d_transform)
        m_exclude_allof = self._exclude_all_of(d_transform)
        m_startswith = self._startswith(d_input)

        # m_include_r1 = self._include_r1(d_input_tokens)
        # m_include_r2 = self._include_r2(d_input_tokens)
        # m_include_r2 = {k: m_include_r2[k] for k in m_include_r2
        #                 if k not in m_include_r1}

        if self.isEnabledForDebug:
            Enforcer.is_dict(m_include_oneof)
            Enforcer.is_dict(m_include_allof)
            Enforcer.is_dict(m_exclude_oneof)
            Enforcer.is_dict(m_exclude_allof)
            Enforcer.is_dict(m_startswith)

        return {
            'include_one_of': m_include_oneof,
            # 'include_r1': m_include_r1,
            # 'include_r2': m_include_r2,
            'include_all_of': m_include_allof,
            'exclude_one_of': m_exclude_oneof,
            'exclude_all_of': m_exclude_allof,
            'startswith': m_startswith,
        }

    def process(self,
                d_tokens: dict) -> MappingResultDict:
        sw = Stopwatch()

        results = self._process(d_tokens)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Mapping Prediction Completed",
                f"\tTotal Time: {str(sw)}",
                f"\tTotal Results: {len(results)}"]))

        if self.isEnabledForDebug and len(results):
            self.logger.debug('\n'.join([
                "Mapping Prediction Results",
                f"{pformat(results)}"]))

        return results
