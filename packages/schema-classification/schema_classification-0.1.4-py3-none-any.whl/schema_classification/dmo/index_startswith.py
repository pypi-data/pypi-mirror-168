#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# type: ignore[import]
# type: ignore[func-returns-value]
""" Generate an Index of 'startswith' Mappings"""


from typing import Dict

from collections import defaultdict

from baseblock import Stopwatch
from baseblock import BaseObject


class IndexStartsWith(BaseObject):
    """ Generate an Index of 'startswith' Mappings"""

    def __init__(self,
                 mapping: Dict):
        """ Change Log

        Created:
            5-Apr-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/264
        Updated:
            8-Jun-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/deepnlu/issues/45

        :param mapping
        """
        BaseObject.__init__(self, __name__)
        self._mapping = mapping

    def process(self) -> Dict:
        sw = Stopwatch()
        d = defaultdict(list)

        for k in self._mapping:
            for mapping in self._mapping[k]:
                if 'startswith' in mapping:
                    for marker_name in mapping['startswith']:
                        d[str(marker_name)].append(str(k))

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                "Generated Index: StartsWith",
                f"\tTotal Rows: {len(d)}",
                f"\tTotal Time: {str(sw)}"]))

        return dict(d)
