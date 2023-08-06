#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from typing import Any
from typing import AnyStr
from typing import List
from typing import Dict
from typing import Tuple
from typing import TypedDict
from typing import NewType
from typing import Union
from typing import Optional


from enum import Enum
from typing import TypedDict


class ExplainResult(Enum):
    NO_MAPPING_FOUND = 0

    FOUND_NONAMBIGUOUS_TYPE_1 = 10
    FOUND_NONAMBIGUOUS_TYPE_2 = 11

    FILTERED_RESULT_TYPE_1 = 20

    INCLUDE_NEAR_MATCH_1 = 30

    ONLY_ONE_MATCH = 50
    FILTER_BY_WEIGHT = 51
    FILTER_BY_COVERAGE = 52
    DUPLICATE_MAPPINGS_FOUND = 53


class MappingResult(TypedDict):
    confidence: float
    explain: ExplainResult
    classification: str


class MappingResults(TypedDict):
    results: list


class Markers(TypedDict):
    marker_name: str
    marker_type: str


InputTags = NewType("InputTags", List[str])


ListOfDicts = NewType("ListOfDicts", List[Dict[str, Any]])


class ServiceEvent(TypedDict):
    text: Optional[str]
    events: ListOfDicts


class MappingResultDict(TypedDict):
    include_one_of: Dict[str, Any]
    include_all_of: Dict[str, Any]
    exclude_one_of: Dict[str, Any]
    exclude_all_of: Dict[str, Any]
    startswith: Dict[str, Any]


class ComputeOutputResultValue(TypedDict):
    weight: int
    coverage: float


ComputeOutputResult = NewType(
    "ComputeOutput", Dict[str, ComputeOutputResultValue])


# Data Flow (RawSchema -> NormalizedSchema)

RawSchema = NewType(
    # Raw Schema
    # This is the datatype when 'FileIO.read_yaml(schema_file)' is called
    # we don't explicitly declare the attributes, as most are optional
    "RawSchema",
    Dict[str, ListOfDicts])


class NormalizedSchema(TypedDict):
    # Normalized Schema
    # This is the normalized form of 'RawSchema'
    # all attributes are declared, even if most values are empty dicts
    scoring: Dict[str, float]
    include_one_of: Dict[str, List[str]]
    include_all_of: Dict[str, ListOfDicts]
    exclude_one_of: Dict[str, List[str]]
    exclude_all_of: Dict[str, List[str]]
    startswith: Dict[str, List[str]]
    mapping: RawSchema
