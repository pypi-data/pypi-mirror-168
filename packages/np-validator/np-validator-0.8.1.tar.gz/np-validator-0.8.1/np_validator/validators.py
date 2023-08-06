from typing import Any, Dict, List, Optional, Tuple, Union

import logging
import operator
import os
import sys

import numpy as np

logger = logging.getLogger(__name__)

from .comparators import above_minimum, rate, within_tolerance
from .sync_dataset import Dataset, get_sync_line_data


def meets_filesize_threshold(
    value: str,
    threshold: Union[float, int],
    operator_name: str = "ge",
) -> Tuple[int, bool]:
    """Validates whether or not a filepath meets a given filesize threshold.

    Args:
        value: Filepath to validate.
        threshold: minimum filesize threshold in bytes
        operator_name: name of which python ``operator`` to use

    Returns:
        A tuple of length 2 wherein, the first element is the filesize of
        the `value` and the second element is a boolean whether or not the
        `threshold` for this value was met.
    """
    op = getattr(operator, operator_name)
    filesize = os.path.getsize(value)
    return (
        filesize,
        op(filesize, threshold),
    )


def has_dict_key(value: Dict[str, Any], path: List[str]) -> Tuple[Any, bool]:
    """Validates whether or not a dictionary has a key at given paths.

    A single element path will grab from the top level keys. Multiple path elements are used to index into nested dictionaries.

    Args:
        value: dictionary to validate
        path: keys to validate

    Returns:
        value: the value of the key if it exists or None
        has_key: whether or not the key was found
    """
    try:
        for key in path:
            value = value[key]
        return (
            value,
            True,
        )
    except KeyError:
        return (
            None,
            False,
        )


def meets_value_threshold(
    value: Union[Dict[str, Any], Dataset],
    path: List[str],
    threshold: Union[float, int],
    tolerance: Optional[Union[float, int]] = None,
) -> Tuple[Any, bool]:
    """Ensures that a value of a dict or Dataset instance at `path` meets a `threshold`.

    Args:
        value: Target dict or Dataset.
        path: Keys to index into target.
        threshold: Threshold to compare the indexed value to.
        tolerance: Tolerance of the threshold.

    Returns:
        The indexed value.
        Whether or not the indexed value meets the given `threshold`.

    Raises:
        Exception: Dataset supplied as `value` and length path > 1.
        TypeError: Value is an unsupported datatype.

    Note:
        To index into nested dict-like objects, use a `path` with length greater than 1.

        Dataset targets only support a `path` of length 1.

        meant to mirror ``get_data_subtype`` for ``synchronization_data`` in ``NP_pipeline_validation``, an earlier implementation this tool is based off of
    """
    if isinstance(value, Dataset):
        if len(path) > 1:
            raise Exception(
                "Dataset doesnt support nested indexing, \
                path length cannot be greater than 1."
            )
        _, value = get_sync_line_data(value, path[0])
    elif isinstance(value, dict):
        value, exists = has_dict_key(value, path)
        if not exists:
            raise Exception("Failed to find value at path: %s" % path)
    else:
        raise TypeError("Unsupported value: %s" % value)

    if tolerance is None:
        try:
            # this is the way the legacy code worked, dont want new bugs
            actual_value = len(value)  # type: ignore[arg-type]
        except TypeError as E:
            actual_value = value  # type: ignore[assignment]
    else:
        actual_value = rate(value)

    if tolerance is None:
        validation_bool = above_minimum(actual_value, threshold)
    else:
        validation_bool = within_tolerance(actual_value, tolerance, threshold)

    return actual_value, validation_bool


def meets_wheel_rotation_threshold(
    value: dict,  # type: ignore
    threshold: int,
) -> Tuple[int, bool]:
    """Validates the number of wheel rotations from behavior output.

    Args:
        value: Behavior pickle data from a session.
        threshold: Minimum number of calculated wheel rotations.

    Returns:
        number_of_rotations: Calculated number of wheel rotations.
        passes: Passes ``threshold``.
    """
    dx = value["items"]["behavior"]["encoders"][0]["dx"]
    num_rotations = np.sum(dx) / 360.0  # wheel rotations
    return num_rotations, num_rotations >= threshold


def meets_lick_threshold(
    value: dict,  # type: ignore
    threshold: int,
) -> Tuple[int, bool]:
    """Validates the number of licks from behavior output.

    Args:
        value: Behavior pickle data from a session.
        threshold: Minimum number of calculated licks.

    Returns:
        Calculated number of licks.
        Passes ``threshold``.
    """
    licks = value["items"]["behavior"]["lick_sensors"][0]["lick_events"]
    return len(licks), len(licks) >= threshold
