#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# type: ignore[import]
# type: ignore[func-returns-value]
""" Compute EXCLUDE_ONE_OF Rulesets """


from typing import Dict
from pprint import pformat

from baseblock import Stopwatch
from baseblock import BaseObject

from schema_classification.dto import NormalizedSchema


class ComputerExcludeOneOf(BaseObject):
    """ Compute EXCLUDE_ONE_OF Rulesets """

    def __init__(self,
                 d_index: NormalizedSchema):
        """ Change Log

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
            d_index (dict): the in-memory schema
        """
        BaseObject.__init__(self, __name__)
        self._mapping = d_index['mapping']
        self._d_exclude_oneof = d_index['exclude_one_of']

    def process(self,
                d_input_tokens: Dict) -> Dict:
        sw = Stopwatch()

        s_mapping = set(self._d_exclude_oneof.keys())
        s_input_tokens = set(d_input_tokens.keys())
        common = s_mapping.intersection(s_input_tokens)

        mapping = set()

        for item in common:
            for value in self._d_exclude_oneof[item]:
                mapping.add(value)

        d_results = {}
        for k in mapping:
            d_results[k] = {}

        if self.isEnabledForInfo:
            self.logger.debug('\n'.join([
                "Computation Complete: Exclude One Of",
                f"\tTotal Mapping: {len(s_mapping)}",
                f"\tTotal Input Tokens: {len(s_input_tokens)}",
                f"\tTotal Candidates: {len(mapping)}",
                f"\tTotal Time: {str(sw)}"]))

        if self.isEnabledForDebug and len(d_results):
            self.logger.debug('\n'.join([
                "EXCLUDE_ONE_OF Results:",
                f"{pformat(d_results)}"]))

        return d_results
