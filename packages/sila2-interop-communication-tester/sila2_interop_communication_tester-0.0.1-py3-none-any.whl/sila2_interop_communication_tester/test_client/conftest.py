"""Pytest configuration file"""
import grpc
import pytest

# is set in __main__.py
CHANNEL: grpc.Channel = grpc.insecure_channel("127.0.0.1:50052")


@pytest.fixture(scope="session")
def channel() -> grpc.Channel:
    return CHANNEL  # noqa: F821
