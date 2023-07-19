import asyncio
import sys
sys.path.append("../mcp23017")

from viam.module.module import Module

from viam.resource.registry import Registry, ResourceCreatorRegistration, ResourceRegistration

from mcp23017.apis import MCP23017, MCP23017Client, MCP23017Service
from mcp23017.models import MCP23017, EightSegmentLED

Registry.register_subtype(ResourceRegistration(MCP23017, MCP23017Service, lambda name, channel: MCP23017Client(name, channel)))
Registry.register_resource_creator(EightSegmentLED.SUBTYPE, EightSegmentLED.MODEL, ResourceCreatorRegistration(EightSegmentLED.new, EightSegmentLED.validate_config))

async def main(address: str):
    """This function creates and starts a new module, after adding all desired resources.
    Resources must be pre-registered. For an example, see the `gizmo.__init__.py` file.

    Args:
        address (str): The address to serve the module on
    """

    module = Module(address)
    module.add_model_from_registry(MCP23017.SUBTYPE, EightSegmentLED.MODEL)
    await module.start()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Need socket path as command line argument")

    asyncio.run(main(sys.argv[1]))