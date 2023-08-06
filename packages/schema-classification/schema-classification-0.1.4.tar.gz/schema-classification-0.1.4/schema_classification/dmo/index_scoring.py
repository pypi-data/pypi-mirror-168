#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# type: ignore[import]
# type: ignore[func-returns-value]
""" Generate an Index of 'score' Mappings """


from typing import Dict


from baseblock import Stopwatch
from baseblock import BaseObject


class IndexScoring(BaseObject):
    """ Generate an Index of 'score' Mappings """

    def __init__(self,
                 mapping: Dict):
        """ Change Log

        Created:
            10-Feb-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/176
        Updated:
            8-Jun-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/deepnlu/issues/45

        :param mapping:
        """
        BaseObject.__init__(self, __name__)
        self._mapping = mapping

    def process(self) -> Dict:
        sw = Stopwatch()
        d = {}

        for k in self._mapping:
            for mapping in self._mapping[k]:

                def score() -> float:
                    if 'score' in mapping:
                        return float(mapping['score'])
                    return 0.0

                d[k] = score()

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                "Generated Index: Scoring",
                f"\tTotal Rows: {len(d)}",
                f"\tTotal Time: {str(sw)}"]))

        return d
