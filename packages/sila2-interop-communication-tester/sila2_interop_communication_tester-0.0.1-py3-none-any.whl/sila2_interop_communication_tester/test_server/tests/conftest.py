import pytest

from sila2_interop_communication_tester.test_server.helpers.spy import ServerCall

# is set in __main__.py
RPC_CALL_ARGS: dict[str, list[ServerCall]]


@pytest.fixture(scope="session")
def server_calls() -> dict[str, list[ServerCall]]:
    return RPC_CALL_ARGS  # noqa: F821
