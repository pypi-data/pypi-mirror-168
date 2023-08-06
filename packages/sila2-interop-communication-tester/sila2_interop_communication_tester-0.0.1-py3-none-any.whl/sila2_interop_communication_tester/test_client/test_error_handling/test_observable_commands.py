import uuid

from sila2_interop_communication_tester.grpc_stubs import ErrorHandlingTest_pb2, SiLAFramework_pb2
from sila2_interop_communication_tester.helpers.utils import string_is_uuid
from sila2_interop_communication_tester.test_client.helpers import (
    raises_defined_execution_error,
    raises_invalid_command_execution_uuid_error,
    raises_undefined_execution_error,
)
from sila2_interop_communication_tester.test_client.helpers.utils import collect_from_stream


def test_raise_defined_execution_error_observably_returns_valid_uuid_string(errorhandlingtest_stub):
    exec_confirmation = errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably(
        ErrorHandlingTest_pb2.RaiseDefinedExecutionErrorObservably_Parameters()
    )

    assert string_is_uuid(exec_confirmation.commandExecutionUUID.value)


def test_raise_undefined_execution_error_observably_returns_valid_uuid_string(errorhandlingtest_stub):
    exec_confirmation = errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably(
        ErrorHandlingTest_pb2.RaiseUndefinedExecutionErrorObservably_Parameters()
    )

    assert string_is_uuid(exec_confirmation.commandExecutionUUID.value)


def test_raise_defined_execution_error_observably_works(errorhandlingtest_stub):
    exec_confirmation = errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably(
        ErrorHandlingTest_pb2.RaiseDefinedExecutionErrorObservably_Parameters()
    )

    with raises_defined_execution_error(
        "org.silastandard/test/ErrorHandlingTest/v1/DefinedExecutionError/TestError"
    ) as error:
        errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably_Result(exec_confirmation.commandExecutionUUID)
    assert error.error.message == "SiLA2_test_error_message"


def test_raise_undefined_execution_error_observably_works(errorhandlingtest_stub):
    exec_confirmation = errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably(
        ErrorHandlingTest_pb2.RaiseUndefinedExecutionErrorObservably_Parameters()
    )

    with raises_undefined_execution_error() as error:
        errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably_Result(exec_confirmation.commandExecutionUUID)
    assert error.error.message == "SiLA2_test_error_message"


def test_raise_defined_execution_error_observably_info_rejects_invalid_uuid(errorhandlingtest_stub):
    info_stream = errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably_Info(
        SiLAFramework_pb2.CommandExecutionUUID(value=str(uuid.uuid4()))
    )
    with raises_invalid_command_execution_uuid_error():
        next(info_stream)


def test_raise_defined_execution_error_observably_result_rejects_invalid_uuid(errorhandlingtest_stub):
    with raises_invalid_command_execution_uuid_error():
        errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably_Result(
            SiLAFramework_pb2.CommandExecutionUUID(value=str(uuid.uuid4()))
        )


def test_raise_undefined_execution_error_observably_info_rejects_invalid_uuid(errorhandlingtest_stub):
    info_stream = errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably_Info(
        SiLAFramework_pb2.CommandExecutionUUID(value=str(uuid.uuid4()))
    )
    with raises_invalid_command_execution_uuid_error():
        next(info_stream)


def test_raise_undefined_execution_error_observably_result_rejects_invalid_uuid(errorhandlingtest_stub):
    with raises_invalid_command_execution_uuid_error():
        errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably_Result(
            SiLAFramework_pb2.CommandExecutionUUID(value=str(uuid.uuid4()))
        )


def test_raise_defined_execution_error_observably_info_reports_finished_with_error(errorhandlingtest_stub):
    exec_confirmation = errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably(
        ErrorHandlingTest_pb2.RaiseDefinedExecutionErrorObservably_Parameters()
    )
    info_stream = errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably_Info(
        exec_confirmation.commandExecutionUUID
    )
    exec_infos = collect_from_stream(info_stream, timeout=1)

    assert exec_infos, "Server did not send execution info for RaiseDefinedExecutionErrorObservably"
    assert exec_infos[-1].commandStatus == SiLAFramework_pb2.ExecutionInfo.CommandStatus.finishedWithError


def test_raise_undefined_execution_error_observably_info_reports_finished_with_error(errorhandlingtest_stub):
    exec_confirmation = errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably(
        ErrorHandlingTest_pb2.RaiseUndefinedExecutionErrorObservably_Parameters()
    )
    info_stream = errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably_Info(
        exec_confirmation.commandExecutionUUID
    )
    exec_infos = collect_from_stream(info_stream, timeout=1)

    assert exec_infos, "Server did not send execution info for RaiseUndefinedExecutionErrorObservably"
    assert exec_infos[-1].commandStatus == SiLAFramework_pb2.ExecutionInfo.CommandStatus.finishedWithError


def test_raise_defined_execution_error_observably_info_rejects_invalid_uuids(errorhandlingtest_stub):
    stream = errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably_Info(
        SiLAFramework_pb2.CommandExecutionUUID(value="abcdefg")
    )
    with raises_invalid_command_execution_uuid_error():
        next(stream)


def test_raise_undefined_execution_error_observably_info_rejects_invalid_uuids(errorhandlingtest_stub):
    stream = errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably_Info(
        SiLAFramework_pb2.CommandExecutionUUID(value="abcdefg")
    )
    with raises_invalid_command_execution_uuid_error():
        next(stream)


def test_raise_defined_execution_error_observably_result_rejects_invalid_uuids(errorhandlingtest_stub):
    with raises_invalid_command_execution_uuid_error():
        errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably_Result(
            SiLAFramework_pb2.CommandExecutionUUID(value="abcdefg")
        )


def test_raise_undefined_execution_error_observably_result_rejects_invalid_uuids(errorhandlingtest_stub):
    with raises_invalid_command_execution_uuid_error():
        errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably_Result(
            SiLAFramework_pb2.CommandExecutionUUID(value="abcdefg")
        )
