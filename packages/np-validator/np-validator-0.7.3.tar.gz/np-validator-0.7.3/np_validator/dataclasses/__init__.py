from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Tuple

import json
import os
from dataclasses import dataclass, field

from .. import processors, validators
from .schemas import ValidationResultSchema, ValidationStepSchema
from .utils import list_functions, resolve_function


@dataclass
class BuiltinCallable:

    """Resolved builtin callable function."""

    resolved_function: Callable[..., Tuple[Any, bool]]
    args: Dict[str, Any]


@dataclass
class Processor:

    """Processor abstraction.

    Args:
        name (str): Name of the processor to use.
        args (:obj:`dict`, optional): Additional arguments supplied to builtin.

    Attributes:
        name (str): Name of the processor.
        args (dict): Additional arguments supplied to builtin.
        builtin (BuiltinCallable): BuiltinCallable instance resolved from `name`.

    Note:
        Refer to `Supported Processors` for a list of supported `name` to use.
    """

    name: str
    args: Dict[str, Any] = field(default_factory=lambda: {})

    def __post_init__(self):
        self.builtin = load_BuiltinCallable(
            processors,
            {
                "name": self.name,
                "args": self.args,
            },
        )


@dataclass
class Validator:

    """Validator abstraction.

    Args:
        name (str): Name of the validator to use.
        args (:obj:`dict`, optional): Additional arguments supplied to builtin.

    Attributes:
        name (str): Name of the validator.
        args (dict): Additional arguments supplied to builtin.
        builtin (BuiltinCallable): BuiltinCallable instance resolved from `name`.

    Note:
        Refer to `Supported Validators` for a list of supported `name` to use.
    """

    name: str
    args: Dict[str, Any] = field(default_factory=lambda: {})

    def __post_init__(self):
        self.builtin = load_BuiltinCallable(
            validators,
            {
                "name": self.name,
                "args": self.args,
            },
        )


@dataclass
class ValidationStep:

    """Validation step abstraction.

    Attributes:
        path_suffix: Filepath suffix matched against filepaths. Determines what filepaths this step will be called on.
        processor: Processors to use on filepath before validation.
        validators: Validators to apply to a matched filepath, or processor output, if a Processor is supplied.
    """

    path_suffix: str
    processor: Optional[Processor] = None
    validators: List[Validator] = field(default_factory=lambda: [])


@dataclass
class ValidatorResult:

    value: Any
    passed: bool
    validator: Validator


@dataclass
class ValidatorError:

    message: str
    validator: Optional[Validator] = None
    processor: Optional[Processor] = None


@dataclass
class ValidationResult:

    filepath: str
    processor: Optional[Processor] = None
    results: List[ValidatorResult] = field(default_factory=lambda: [])
    errors: List[ValidatorError] = field(default_factory=lambda: [])


validation_step_schema = ValidationStepSchema()


def validate_ValidationStep_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validates that a dictionary has the shape we expect for ValidationStep."""
    return validation_step_schema.load(data)  # type: ignore[no-any-return]


def load_BuiltinCallable(mod: ModuleType, data: Dict[str, Any]) -> BuiltinCallable:
    """Loads a BuiltinCallable from a structured dictionary."""
    return BuiltinCallable(
        resolved_function=resolve_function(
            mod,
            data["name"],
        ),
        args=data["args"],
    )


def load_ValidationStep(data: Dict[str, Any]) -> ValidationStep:
    """Loads a ValidationStep from a structured dictionary."""
    validated = validate_ValidationStep_data(data)

    processor_data = validated.get("processor")

    loaded_validators = [
        Validator(**validator_data) for validator_data in validated["validators"]
    ]

    if processor_data:
        return ValidationStep(
            path_suffix=data["path_suffix"],
            processor=Processor(**processor_data),
            validators=loaded_validators,
        )
    else:
        return ValidationStep(
            path_suffix=data["path_suffix"],
            validators=loaded_validators,
        )


validation_result_schema = ValidationResultSchema()


def dump_ValidationResult(result: ValidationResult) -> Dict[str, Any]:
    return validation_result_schema.dump(result)  # type: ignore[no-any-return]


validation_results_schema = ValidationResultSchema(
    many=True,
)


def dump_ValidationResults(
    results: List[ValidationResult],
    filepath: str,
    json_args: Dict[str, Any] = {
        "indent": 4,
        "sort_keys": True,
    },
) -> None:
    """Convenience function for dumping a list of validation results.

    Args:
        results: List of validation results.
        filepath: Path to dump validation results.
        json_args: Arguments to supply to python's builtin `json.dump`.
    """
    with open(filepath, "w") as f:
        json.dump(validation_results_schema.dump(results), f, **json_args)


def _extract_path_suffix(path: str) -> str:
    fname = os.path.basename(path)
    return fname.split(".", 1)[1]


def path_to_ValidationStep(path: str) -> ValidationStep:
    return ValidationStep(
        path_suffix=_extract_path_suffix(path),
        validators=[
            Validator(
                name="meets_filesize_threshold",
                args={
                    "threshold": 1,
                },
            )
        ],
    )
