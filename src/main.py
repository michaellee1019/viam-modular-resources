import asyncio
import sys

sys.path.append("..")

from viam.module.module import Module
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.components.generic import Generic

from models import EightSegmentLED
from models import AudioOutputPlayFile
from models import Grove4ChannelSPDTRelay

Registry.register_resource_creator(Generic.SUBTYPE, EightSegmentLED.MODEL, ResourceCreatorRegistration(EightSegmentLED.new, EightSegmentLED.validate_config))
Registry.register_resource_creator(Generic.SUBTYPE, AudioOutputPlayFile.MODEL, ResourceCreatorRegistration(AudioOutputPlayFile.new, AudioOutputPlayFile.validate_config))
Registry.register_resource_creator(Generic.SUBTYPE, Grove4ChannelSPDTRelay.MODEL, ResourceCreatorRegistration(Grove4ChannelSPDTRelay.new, Grove4ChannelSPDTRelay.validate_config))

async def main():
    """This function creates and starts a new module, after adding all desired resources.
    Resources must be pre-registered. For an example, see the `gizmo.__init__.py` file.

    Args:
        address (str): The address to serve the module on
    """

    module = Module.from_args()
    module.add_model_from_registry(Generic.SUBTYPE, EightSegmentLED.MODEL)
    module.add_model_from_registry(Generic.SUBTYPE, AudioOutputPlayFile.MODEL)
    module.add_model_from_registry(Generic.SUBTYPE, Grove4ChannelSPDTRelay.MODEL)
    await module.start()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Need socket path as command line argument")

    asyncio.run(main())