#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Build an in-memory Index over a Dictionary of Classifications """


import os

from baseblock import FileIO
from baseblock import Enforcer
from baseblock import BaseObject

from schema_classification.dmo import IndexScoring
from schema_classification.dmo import IndexExcludeAllOf
from schema_classification.dmo import IndexExcludeOneOf
from schema_classification.dmo import IndexIncludeAllOf
from schema_classification.dmo import IndexIncludeOneOf
from schema_classification.dmo import IndexStartsWith


class ReadMapping(BaseObject):
    """ Build an in-memory Index over a Dictionary of Classifications """

    def __init__(self,
                 schema_file: str):
        """ Initialize Manifest Indicer

        Created:
            7-Feb-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/167
        Updated:
            8-Jun-2022
            craigtrim@gmail.com
            *   read schema in-memory
                https://github.com/grafflr/deepnlu/issues/45
        Updated:
            26-Jul-2022
            craigtrim@gmail.com
            *   remove 'schema-name' and 'absolute-path' as parameters, and instead
                pass the full absolute path of a schema file, in pursuit of
                https://bast-ai.atlassian.net/browse/COR-12

        Args:
            schema_file (str): the absolute path to a local schema file containing classification rules
        """
        BaseObject.__init__(self, __name__)
        d_schema = FileIO.read_yaml(schema_file)
        self._d_index = self._create_index(d_schema)

    # def _read_file(self,
    #                schema_name: str,
    #                absolute_path: str) -> dict:

    #     def get_file_name() -> str:
    #         if "yml" not in schema_name:
    #             return f"{schema_name}.yml"
    #         return schema_name

    #     input_file = os.path.normpath(os.path.join(
    #         absolute_path, get_file_name()))

    #     FileIO.exists_or_error(input_file)
    #     return FileIO.read_yaml(input_file)

    def _create_index(self,
                      d_schema: dict):

        return {
            'scoring': IndexScoring(d_schema).process(),
            'include_one_of': IndexIncludeOneOf(d_schema).process(),
            'include_all_of': IndexIncludeAllOf(d_schema).process(),
            'exclude_one_of': IndexExcludeOneOf(d_schema).process(),
            'exclude_all_of': IndexExcludeAllOf(d_schema).process(),
            'startswith': IndexStartsWith(d_schema).process(),
            'mapping': d_schema,
        }

    def index(self) -> dict:
        return self._d_index
