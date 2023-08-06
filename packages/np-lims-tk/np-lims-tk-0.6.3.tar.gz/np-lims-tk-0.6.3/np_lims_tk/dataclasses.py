from typing import Any, List, Optional, Tuple

from dataclasses import dataclass


@dataclass
class Query:

    """Abstraction of query to be executed on lims database."""

    query_str: str
    filters: List[Tuple[str, Any]]
    return_name: str


@dataclass
class LimsMeta:

    """Abstraction of np project metadata."""

    _id: str
    subject_id: str
    date_str: str
