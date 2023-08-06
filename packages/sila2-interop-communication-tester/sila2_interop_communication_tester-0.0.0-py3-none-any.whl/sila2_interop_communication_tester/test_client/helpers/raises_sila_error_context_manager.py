"""Defines context managers to assert that SiLA Errors are raised"""
import binascii
from base64 import standard_b64decode
from types import TracebackType
from typing import Callable, Generic, Literal, Optional, Type, TypeVar

import google.protobuf.message
import grpc
from pytest import fail

from sila2_interop_communication_tester.grpc_stubs.SiLAFramework_pb2 import (
    DefinedExecutionError,
    FrameworkError,
    SiLAError,
    UndefinedExecutionError,
    ValidationError,
)

_SiLAErrorType = TypeVar(
    "_SiLAErrorType", ValidationError, FrameworkError, DefinedExecutionError, UndefinedExecutionError
)
_SiLAErrorTypeName = Literal["validationError", "frameworkError", "definedExecutionError", "undefinedExecutionError"]
_FrameworkErrorType = Literal[
    "COMMAND_EXECUTION_NOT_ACCEPTED",
    "INVALID_COMMAND_EXECUTION_UUID",
    "COMMAND_EXECUTION_NOT_FINISHED",
    "INVALID_METADATA",
    "NO_METADATA_ALLOWED",
]


class SiLAErrorOption(Generic[_SiLAErrorType]):
    def __init__(self):
        self.error: Optional[_SiLAErrorType] = None


class RaisesContext(Generic[_SiLAErrorType]):
    # adapted from pytest.raises
    def __init__(
        self, error_type: _SiLAErrorTypeName, check_func: Optional[Callable[[_SiLAErrorType], None]] = None
    ) -> None:
        self.error_type = error_type
        self.sila_error_option: SiLAErrorOption[_SiLAErrorType] = SiLAErrorOption()
        self.check_func: Optional[Callable[[_SiLAErrorType], None]] = check_func

    def __enter__(self) -> SiLAErrorOption[_SiLAErrorType]:
        return self.sila_error_option

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        __tracebackhide__ = True

        if exc_type is None:
            fail("Expected a gRPC error, but no exception was caught")

        if not issubclass(exc_type, grpc.RpcError):
            return False

        assert isinstance(exc_val, grpc.RpcError), "Caught a non-gRPC error (probably an internal error in test suite)"
        assert isinstance(exc_val, grpc.Call), "Caught a non-gRPC error (probably an internal error in test suite)"
        assert (
            exc_val.code() == grpc.StatusCode.ABORTED
        ), f"Caught gRPC error with wrong status code (expected {grpc.StatusCode.ABORTED}, got {exc_val.code()})"

        try:
            sila_error = SiLAError.FromString(standard_b64decode(exc_val.details()))
        except binascii.Error:
            fail("Failed to decode error details as Base64")
            return
        except google.protobuf.message.DecodeError:
            fail("Failed to decode error details as SiLAFramework.SiLAError Protobuf message")
            return

        assert sila_error.HasField(
            self.error_type
        ), f"Caught SiLA Error of wrong type (expected '{self.error_type}', got '{sila_error.WhichOneof('error')}')"

        specific_error: _SiLAErrorType = getattr(sila_error, self.error_type)

        assert (
            len(specific_error.message) > 10
        ), "Error message was less than 10 characters long (SiLA Errors must include information about the error)"

        if self.check_func is not None:
            self.check_func(specific_error)

        self.sila_error_option.error = specific_error
        return True


def raises_defined_execution_error(error_identifier: str) -> RaisesContext[DefinedExecutionError]:
    def check_func(error: DefinedExecutionError) -> None:
        assert error.errorIdentifier == error_identifier, (
            f"Caught DefinedExecutionError with wrong errorIdentifier "
            f"(expected '{error_identifier}', got '{error.errorIdentifier}')"
        )

    return RaisesContext("definedExecutionError", check_func)


def raises_undefined_execution_error() -> RaisesContext[UndefinedExecutionError]:
    return RaisesContext("undefinedExecutionError")


def raises_validation_error(parameter_identifier: str) -> RaisesContext[ValidationError]:
    def check_func(error: ValidationError) -> None:
        assert (
            error.parameter == parameter_identifier
        ), f"Caught ValidationError for wrong parameter (expected '{parameter_identifier}', got '{error.parameter}')"

    return RaisesContext("validationError", check_func)


def __raises_framework_error(error_type: _FrameworkErrorType) -> RaisesContext[FrameworkError]:
    error_type = getattr(FrameworkError.ErrorType, error_type)

    def check_func(error: FrameworkError) -> None:
        assert (
            error.errorType == error_type
        ), f"Caught FrameworkError with wrong errorType (expected '{error_type}', got '{error.errorType}')"

    return RaisesContext("frameworkError", check_func)


def raises_command_execution_not_accepted_error():
    return __raises_framework_error("COMMAND_EXECUTION_NOT_ACCEPTED")


def raises_invalid_command_execution_uuid_error():
    return __raises_framework_error("INVALID_COMMAND_EXECUTION_UUID")


def raises_command_execution_not_finished_error():
    return __raises_framework_error("COMMAND_EXECUTION_NOT_FINISHED")


def raises_invalid_metadata_error():
    return __raises_framework_error("INVALID_METADATA")


def raises_no_metadata_allowed_error():
    return __raises_framework_error("NO_METADATA_ALLOWED")
