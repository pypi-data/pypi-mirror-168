import concurrent.futures
from typing import Optional

import grpc

from sila2_interop_communication_tester.grpc_stubs.BinaryTransferTest_pb2_grpc import (
    add_BinaryTransferTestServicer_to_server,
)
from sila2_interop_communication_tester.grpc_stubs.ErrorHandlingTest_pb2_grpc import (
    add_ErrorHandlingTestServicer_to_server,
)
from sila2_interop_communication_tester.grpc_stubs.MetadataConsumerTest_pb2_grpc import (
    add_MetadataConsumerTestServicer_to_server,
)
from sila2_interop_communication_tester.grpc_stubs.MetadataProvider_pb2_grpc import (
    add_MetadataProviderServicer_to_server,
)
from sila2_interop_communication_tester.grpc_stubs.ObservableCommandTest_pb2_grpc import (
    add_ObservableCommandTestServicer_to_server,
)
from sila2_interop_communication_tester.grpc_stubs.ObservablePropertyTest_pb2_grpc import (
    add_ObservablePropertyTestServicer_to_server,
)
from sila2_interop_communication_tester.grpc_stubs.SiLABinaryTransfer_pb2_grpc import (
    add_BinaryDownloadServicer_to_server,
    add_BinaryUploadServicer_to_server,
)
from sila2_interop_communication_tester.grpc_stubs.SiLAService_pb2_grpc import add_SiLAServiceServicer_to_server
from sila2_interop_communication_tester.grpc_stubs.UnobservableCommandTest_pb2_grpc import (
    add_UnobservableCommandTestServicer_to_server,
)
from sila2_interop_communication_tester.grpc_stubs.UnobservablePropertyTest_pb2_grpc import (
    add_UnobservablePropertyTestServicer_to_server,
)
from sila2_interop_communication_tester.test_server.helpers.spy import spy_servicer
from sila2_interop_communication_tester.test_server.server_implementation.binary_download import BinaryDownloadImpl
from sila2_interop_communication_tester.test_server.server_implementation.binary_transfer_test import (
    BinaryTransferTestImpl,
)
from sila2_interop_communication_tester.test_server.server_implementation.binary_upload import BinaryUploadImpl
from sila2_interop_communication_tester.test_server.server_implementation.error_handling_test import (
    ErrorHandlingTestImpl,
)
from sila2_interop_communication_tester.test_server.server_implementation.metadata_consumer_test import (
    MetadataConsumerTestImpl,
)
from sila2_interop_communication_tester.test_server.server_implementation.metadata_provider_test import (
    MetadataProviderImpl,
)
from sila2_interop_communication_tester.test_server.server_implementation.observable_command_test import (
    ObservableCommandTestImpl,
)
from sila2_interop_communication_tester.test_server.server_implementation.observable_property_test import (
    ObservablePropertyTestImpl,
)
from sila2_interop_communication_tester.test_server.server_implementation.sila_service import SiLAServiceImpl
from sila2_interop_communication_tester.test_server.server_implementation.unobservable_command_test import (
    UnobservableCommandTestImpl,
)
from sila2_interop_communication_tester.test_server.server_implementation.unobservable_property_test import (
    UnobservablePropertyTestImpl,
)


class Server:
    def __init__(self, server_address: str, cert_file: Optional[str], key_file: Optional[str]) -> None:
        self.server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=100))

        # configure address and encryption
        if cert_file is None and key_file is None:
            self.server.add_insecure_port(server_address)
        elif cert_file is not None and key_file is not None:
            with open(cert_file, "rb") as cert_fp, open(key_file, "rb") as key_fp:
                self.server.add_secure_port(
                    server_address,
                    server_credentials=grpc.ssl_server_credentials([(key_fp.read(), cert_fp.read())]),
                )
        else:
            raise ValueError("Either certificate and private key files must both be provided, or none of them")

        # binary transfer
        binary_upload_parameter_whitelist = [
            "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
            "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinariesObservably/Parameter/Binaries",
        ]
        add_BinaryUploadServicer_to_server(
            spy_servicer(BinaryUploadImpl(allowed_parameters=binary_upload_parameter_whitelist)), self.server
        )
        add_BinaryDownloadServicer_to_server(spy_servicer(BinaryDownloadImpl()), self.server)

        # add feature implementations
        add_SiLAServiceServicer_to_server(spy_servicer(SiLAServiceImpl()), self.server)
        add_UnobservablePropertyTestServicer_to_server(spy_servicer(UnobservablePropertyTestImpl()), self.server)
        add_UnobservableCommandTestServicer_to_server(spy_servicer(UnobservableCommandTestImpl()), self.server)
        add_MetadataProviderServicer_to_server(spy_servicer(MetadataProviderImpl()), self.server)
        add_MetadataConsumerTestServicer_to_server(spy_servicer(MetadataConsumerTestImpl()), self.server)
        add_ErrorHandlingTestServicer_to_server(spy_servicer(ErrorHandlingTestImpl()), self.server)
        add_ObservablePropertyTestServicer_to_server(spy_servicer(ObservablePropertyTestImpl()), self.server)
        add_ObservableCommandTestServicer_to_server(spy_servicer(ObservableCommandTestImpl()), self.server)
        add_BinaryTransferTestServicer_to_server(spy_servicer(BinaryTransferTestImpl()), self.server)

    def start(self) -> None:
        self.server.start()

    def stop(self, grace: Optional[int] = None) -> None:
        self.server.stop(grace)

    def wait_for_termination(self, timeout: Optional[int] = None) -> None:
        self.server.wait_for_termination(timeout)
