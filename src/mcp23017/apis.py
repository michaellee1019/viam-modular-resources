import abc
from typing import Final, List, Mapping, Optional, Sequence

from grpclib.client import Channel
from grpclib.server import Stream

from viam.components.component_base import ComponentBase
from viam.components.generic.client import do_command
from viam.errors import ResourceNotFoundError
from viam.resource.rpc_service_base import ResourceRPCServiceBase
from viam.resource.types import RESOURCE_TYPE_COMPONENT, Subtype
from viam.utils import ValueTypes

from .proto.gen.mcp23017_grpc import MCP23017ServiceBase, MCP23017ServiceStub
from .proto.gen.mcp23017_pb2 import (
    FlashWordRequest,
    FlashWordResponse,
)

class MCP23017(ComponentBase):
    SUBTYPE: Final = Subtype("michaellee1019", RESOURCE_TYPE_COMPONENT, "mcp23017")

    @abc.abstractmethod
    async def flash_word(self, word: str, **kwargs) -> None:
        ...

class MCP23017Service(MCP23017ServiceBase, ResourceRPCServiceBase):
    RESOURCE_TYPE = MCP23017

    async def FlashWord(self, stream: Stream[FlashWordRequest, FlashWordResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        name = request.name
        try:
            resource = self.get_resource(name)
        except ResourceNotFoundError as e:
            raise e.grpc_error
        resp = await resource.flash_word(request.name)
        response = FlashWordResponse()
        await stream.send_message(response)

class MCP23017Client(MCP23017):
    def __init__(self, channel: Channel):
        self.channel = channel
        self.client = MCP23017ServiceStub(channel)
        super().__init__()

    async def flash_word(self) -> None:
        resp: FlashWordResponse = await self.client.FlashWord(FlashWordRequest())
        return None

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
    ) -> Mapping[str, ValueTypes]:
        return await do_command(self.channel, self.name, command, timeout=timeout)