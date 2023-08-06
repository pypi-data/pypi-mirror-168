from dataclasses import dataclass
import importlib.util
import sys
from typing import Any, Callable, Tuple
import grpc
import pkg_resources
from concurrent import futures

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih.collection import ServiceRoleValue
from pih.const import ServiceCommands, ServiceRoles
import pih.rpcCommandCall_pb2_grpc as pb2_grpc
import pih.rpcCommandCall_pb2 as pb2
from pih.tools import DataTools, ParameterList

@dataclass
class rpcCommand:
    host: str
    port: int
    name: str


@dataclass
class Error(BaseException):
    details: str
    code: Tuple

class RPC:

    @staticmethod
    def create_error(context, message: str = "", code: Any = None) -> Any:
        context.set_details(message)
        context.set_code(code)
        return pb2.rpcCommandResult()

    class UnaryService(pb2_grpc.UnaryServicer):

        def __init__(self, handler: Callable, *args, **kwargs):
            self.handler = handler

        def internal_handler(self, command_name: str, parameters: str, context) -> dict:
            print(f"RPC call: {command_name}")
            if command_name == "ping":
                return "pong"
            return self.handler(command_name, ParameterList(parameters), context)

        def rpcCallCommand(self, command, context):
            parameters = command.parameters
            if not DataTools.is_empty(parameters):
                parameters = DataTools.rpc_unrepresent(parameters)
            return pb2.rpcCommandResult(data=DataTools.represent(self.internal_handler(command.name, parameters, context)))

    class Service:

        @staticmethod
        def serve(service_host: str, service_name: str, service_port: int, handler: Callable, libs: Tuple = None) -> None:
            from pih.pih import PIH, PR
            PR.init()
            PIH.VISUAL.rpc_service_header(
                service_host, service_port, service_name)
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            pb2_grpc.add_UnaryServicer_to_server(
                RPC.UnaryService(handler), server)
            server.add_insecure_port(f"{service_host}:{service_port}")
            server.start()
            server.wait_for_termination()

        @staticmethod
        def serve_role(role: ServiceRoles, handler: Callable, start_handler: Callable = None) -> None:
            from pih.pih import PIH, PR
            PR.init()
            role_item: ServiceRoleValue = role.value
            service_host: str = PIH.SERVICE.get_host(role)
            service_port: int = PIH.SERVICE.get_port(role)
            PIH.VISUAL.rpc_service_header(
                service_host, service_port, role_item.description)
            all_library_installed: bool = True
            installed_libraries = {pkg.key for pkg in pkg_resources.working_set}
            for lib in role_item.libs:
                if lib not in installed_libraries:
                    all_library_installed = False
                    PR.alert(f"Library: {lib} is not presented!")
            if not all_library_installed: 
                PR.alert(f"Service starting was aborted!")
                return
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            pb2_grpc.add_UnaryServicer_to_server(
                RPC.UnaryService(handler), server)
            server.add_insecure_port(f"{service_host}:{service_port}")
            server.start()
            if start_handler is not None:
                start_handler()
            PIH.MESSAGE.COMMAND.service_started(role)
            server.wait_for_termination()

    class CommandClient():

        def __init__(self, host: str, port: int):
            self.stub = pb2_grpc.UnaryStub(grpc.insecure_channel(f"{host}:{port}"))

        def call_command(self, name: str, parameters: str = None):
            return self.stub.rpcCallCommand(pb2.rpcCommand(name=name, parameters=parameters))

    @staticmethod
    def ping(role: ServiceRoles) -> str:
        return RPC.internal_call(role, ServiceCommands.ping)

    @staticmethod
    def internal_call(role: ServiceRoles, command: ServiceCommands, parameters: Any = None) -> str:
        PIH = sys.modules["pih.pih"].PIH
        PIH.SERVICE.init()
        try:
            if role is None:
                role = PIH.SERVICE.get_role_by_command(command)
            service_host: str = PIH.SERVICE.get_host(role)
            service_port: int = PIH.SERVICE.get_port(role)
            return RPC.CommandClient(service_host, service_port).call_command(command.name, DataTools.rpc_represent(parameters)).data
        except grpc.RpcError as error:
            code: Tuple = error.code()
            details: str = f"\nService host: {service_host}\nService port: {service_port}\nCommand: {command.name}\nDetails: {error.details()}\nCode: {code}"
            PIH.error_handler(details, code, role, command)

    @staticmethod
    def call_by_role(command: ServiceCommands, parameters: Any = None) -> str:
        return RPC.internal_call(None, command, parameters)

    @staticmethod
    def call(command: rpcCommand, parameters: Any = None) -> str:
        PIH = sys.modules["pih.pih"].PIH
        try:
            return RPC.CommandClient(command.host, command.port).call_command(command.name, DataTools.rpc_represent(parameters)).data
        except grpc.RpcError as error:
            code: Tuple = error.code()
            details: str = f"Service host: {command.host}\nService port: {command.port}\nCommand: {command.name}\nDetails: {error.details()}\nCode: {code}"
            PIH.error_handler(details, code, command)
            raise Error(details, code)
