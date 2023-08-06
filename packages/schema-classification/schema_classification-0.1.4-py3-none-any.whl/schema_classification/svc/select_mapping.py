#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# type: ignore[import]
# type: ignore[func-returns-value]
""" Choose the Best Mapping """


from typing import List
from typing import Dict
from typing import Any

from baseblock import BaseObject

from schema_classification.dmo import MappingFindCandidates
from schema_classification.dmo import MappingRemoveDuplicates
from schema_classification.dmo import MappingScoreCandidates
from schema_classification.dmo import MappingSelectCandidates

from schema_classification.dto import ListOfDicts
from schema_classification.dto import NormalizedSchema
from schema_classification.dto import MappingResultDict


class SelectMapping(BaseObject):
    """ Choose the Best Mapping """

    def __init__(self,
                 results: MappingResultDict,
                 d_index: NormalizedSchema):
        """ Change Log

        Created:
            7-Feb-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/169
        Updated:
            8-Jun-2022
            craigtrim@gmail.com
            *   eliminate callback and pass d-index in pursuit of
                https://github.com/grafflr/deepnlu/issues/45

        :param results:
            relevant section of mapping ruleset
        :param scoring:
            callback to scoring method
        """
        BaseObject.__init__(self, __name__)
        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                "Initialized Service",
                f"\tTotal Results: {len(results)}"]))

        self._results = results
        self._d_index = d_index

    def process(self) -> ListOfDicts:

        find_candidates = MappingFindCandidates(self._results).process

        score_candidates = MappingScoreCandidates(
            results=self._results,
            d_index=self._d_index).process

        dedupe_candidates = MappingRemoveDuplicates(self._results).process

        select_candidates = MappingSelectCandidates(self._results).process

        d_candidates = find_candidates()  # Find Candidates
        d_candidates = score_candidates(d_candidates)  # Score Candidates
        d_candidates = dedupe_candidates(d_candidates)  # Remove Duplicates
        d_results = select_candidates(d_candidates)  # Select Results

        return d_results
