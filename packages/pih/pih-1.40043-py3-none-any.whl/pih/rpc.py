from ast import Call
from dataclasses import dataclass
from typing import Any, Callable, Tuple
import grpc

from concurrent import futures
from pih.collection import ServiceRoleItem
from pih.const import ServiceCommandNames, ServiceRoles

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

    command_map: dict = None
    error_handler: Callable = None
    get_host_handler: Callable = None
    get_port_handler: Callable = None

    @staticmethod
    def init(error_handler: Callable, get_host_handler: Callable, get_port_handler: Callable) -> None:
        RPC.error_handler = error_handler
        RPC.get_host_handler = get_host_handler
        RPC.get_port_handler = get_port_handler
        RPC.command_map = {}
        for role in ServiceRoles:
            for role_command in role.value.commands:
                RPC.command_map[role_command.name] = role

    @staticmethod
    def create_error(context, message: str = "", code: Any = None) -> Any:
        context.set_details(message)
        context.set_code(code)
        return pb2.rpcCommandResult()

    @staticmethod
    def get_service_role_by_command_name(value: ServiceCommandNames) -> ServiceRoles:
        return RPC.command_map[value.name]

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
        def serve_role(role: ServiceRoles, handler: Callable) -> None:
            from pih.pih import PIH, PR
            PR.init()
            role_item: ServiceRoleItem = role.value
            service_host: str = RPC.get_host_handler(role)
            service_port: int = RPC.get_port_handler(role)
            PIH.VISUAL.rpc_service_header(
                service_host, service_port, role_item.name)
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            pb2_grpc.add_UnaryServicer_to_server(
                RPC.UnaryService(handler), server)
            server.add_insecure_port(f"{service_host}:{service_port}")
            server.start()
            server.wait_for_termination()

    class CommandClient():

        def __init__(self, host: str, port: int):
            self.stub = pb2_grpc.UnaryStub(grpc.insecure_channel(f"{host}:{port}"))

        def call_command(self, name: str, parameters: str = None):
            return self.stub.rpcCallCommand(pb2.rpcCommand(name=name, parameters=parameters))

    @staticmethod
    def call_by_role(command: ServiceCommandNames, parameters: Any = None) -> str:
        try:
            role: ServiceRoles = RPC.get_service_role_by_command_name(command)
            service_host: str = RPC.get_host_handler(role)
            service_port: int = RPC.get_port_handler(role)
            return RPC.CommandClient(service_host, service_port).call_command(command.name, DataTools.rpc_represent(parameters)).data
        except grpc.RpcError as error:
            code: Tuple = error.code()
            details: str = f"\nService host: {service_host}\nService port: {service_port}\nCommand: {command.name}\nDetails: {error.details()}\nCode: {code}"
            if RPC.error_handler is not None:
                RPC.error_handler(details, code, command)

    @staticmethod
    def call(command: rpcCommand, parameters: Any = None) -> str:
        try:
            return RPC.CommandClient(command.host, command.port).call_command(command.name, DataTools.rpc_represent(parameters)).data
        except grpc.RpcError as error:
            code: Tuple = error.code()
            details: str = f"Service host: {command.host}\nService port: {command.port}\nCommand: {command.name}\nDetails: {error.details()}\nCode: {code}"
            if RPC.error_handler is not None:
                RPC.error_handler(details, code, command)
            raise Error(details, code)
