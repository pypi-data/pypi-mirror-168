from typing import Any, Dict, List, Optional, Tuple, Union

import json
import logging
from dataclasses import replace

import yaml
from psycopg2 import connect, extensions, extras

from . import queries
from .config import allen_config_auto_discovery
from .dataclasses import Query
from .exceptions import LimsError, NPTKError
from .local_paths import get_suffixes, local_path_to_Query, path_to_lims_meta
from .utils import fix_lims_path, is_valid_exp_id, is_windows
from .wkft import get_wkft_names, wkft_to_Query

logger = logging.getLogger(__name__)


def run_query(cursor: extensions.cursor, query: Query) -> List[str]:
    """Runs a lims query.

    Args:
        cursor: lims postgresql cursor instance
        query: Query instance to run

    Returns:
        List of filepaths to assets on lims.
    """
    cursor.execute(query.query_str)
    filtered = []
    for row in cursor.fetchall():
        for (key, value) in query.filters:
            if row[key] != value:
                break
        else:
            filtered.append(row[query.return_name])
    return filtered


def _init_cursor(db_uri: str) -> extensions.cursor:
    """Initializes a connection to the lims database."""
    logger.info("Connecting to database uri: %s..." % db_uri)
    con = connect(db_uri)
    con.set_session(readonly=True, autocommit=True)
    return con.cursor(
        cursor_factory=extras.RealDictCursor,
    )


def _resolve_query(
    exp_id: Optional[str] = None,
    wkft: Optional[str] = None,
    local_path: Optional[str] = None,
) -> Query:
    """Resolves a combination of experiment meta info to a query to be executed on lims."""
    if wkft and exp_id:
        if not is_valid_exp_id(exp_id):
            raise LimsError("Invalid experiment id: %s" % exp_id)
        query = wkft_to_Query(wkft, exp_id)
    elif local_path:
        query = local_path_to_Query(local_path, exp_id)
    else:
        raise LimsError("Invalid number of arguments supplied.")

    return query


def find_files(
    db_uri: Optional[str] = None,
    exp_id: Optional[str] = None,
    wkft: Optional[str] = None,
    local_path: Optional[str] = None,
) -> List[str]:
    """Finds all files associated with a combination of experiment meta info.

    Args:
        db_uri: lims database uri
        exp_id: lims experiment id associated with the files
        wkft: well known file type name associated with the files you want to find
        local_path: local filepath of a file you want to find on lims

    Returns:
        A list of filepaths

    Note:
        - The following combinations of meta info are supported
            - ``exp_id`` and ``wkft``
            - ``local_path``
        - A ``local_path`` can be prefixed with * but an experiment id will need to be supplied
        - If no ``db_uri`` is supplied, will attempt ``allen_config_auto_discovery``
    """
    if db_uri is None:
        logger.info("No db_uri supplied, using allen config auto discovery...")
        db_uri = allen_config_auto_discovery("lims_db_uri")
        logger.info("Resolved db_uri: %s" % db_uri)

    query = _resolve_query(exp_id=exp_id, wkft=wkft, local_path=local_path)
    logger.info("Resolved query: %s" % query)

    with _init_cursor(db_uri) as cursor:
        results = run_query(cursor, query)

    if is_windows():
        logger.info(
            "Windows detected. Fixing paths for windows. Paths before: %s" % results
        )
        fixed = [fix_lims_path(result) for result in results]
        logger.info("Paths after: %s" % fixed)
        return fixed

    return results


def get_project_name(
    project_id: Optional[str] = None,
    lims_id: Optional[str] = None,
    path: Optional[str] = None,
    db_uri: Optional[str] = None,
) -> Union[str, None]:
    if not path and not lims_id and not project_id:
        raise Exception("Insufficient arguments.")
    if not lims_id and not project_id and path:
        meta = path_to_lims_meta(path)
        if not meta:
            raise NPTKError("Failed to deserialize meta info from path=%s" % path)

        lims_id = meta._id

    if db_uri is None:
        logger.info("No db_uri supplied, using allen config auto discovery...")
        db_uri = allen_config_auto_discovery("lims_db_uri")
        logger.info("Resolved db_uri: %s" % db_uri)

    with _init_cursor(db_uri) as cursor:
        if not project_id:
            results = run_query(
                cursor,
                Query(
                    queries.ECEPHYS_SESSION_QUERY.format(lims_id),
                    filters=[],
                    return_name="project_id",
                ),
            )
            project_id = results[0]

        results = run_query(
            cursor,
            Query(
                queries.PROJECT_QUERY.format(project_id), filters=[], return_name="code"
            ),
        )
        name = results[0]

    return name


def project_name_to_data_manifestor_template(
    name: str,
    manifestor_lookup: Optional[Dict[str, str]] = None,
    raw: bool = False,
) -> Union[str, Dict[str, Any]]:
    if not manifestor_lookup:
        manifestor_lookup = allen_config_auto_discovery(
            "manifestor_lookup",
        )

    try:
        path = manifestor_lookup[name]  # type: ignore
        if raw:
            return path

        with open(path) as f:
            return yaml.safe_load(f)  # type: ignore
    except KeyError:
        raise NPTKError("Invalid name=%s" % name)


def get_data_manifestor_template(
    lims_id: Optional[str] = None,
    manifestor_lookup: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    if not manifestor_lookup:
        manifestor_lookup = allen_config_auto_discovery(
            "manifestor_lookup",
        )

    project_name = get_project_name(lims_id=lims_id)

    try:
        path = manifestor_lookup[project_name]  # type: ignore
        if path.endswith(".yml"):
            with open(path) as f:
                return yaml.safe_load(f)  # type: ignore
        elif path.endswith(".json"):
            with open(path) as f:
                return json.load(f)  # type: ignore
        else:
            raise NPTKError("Unsupported data-manifestor file format: %s" % path)
    except KeyError:
        raise NPTKError("Invalid project_name=%s" % project_name)
