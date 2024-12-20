import json

from typing import ClassVar, Mapping, Optional

from typing_extensions import Self

import smbus

from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.utils import ValueTypes
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.components.generic import Generic
from google.protobuf import json_format
from viam import logging

LOGGER = logging.getLogger(__name__)

import time
import pygame

class AudioOutputPlayFile(Generic):
    MODEL: ClassVar[Model] = Model(ModelFamily("michaellee1019", "audio_output"), "play_file")
    files: dict

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        result = {key: False for key in command.keys()}
        for (name, args) in command.items():
            if name == 'play':
                if 'sound' in args:
                    results = await self.play_file(args['sound'])
                    result[name] = 'played: ' + results
                else:
                    result[name] = 'missing sound key'
        return result

    async def play_file(self, filename: str) -> str:
        file_path = self.files.get(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        return filename

    @classmethod
    def new(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        output = self(config.name)

        output.files = json.loads(json_format.MessageToJson(config.attributes.fields["files"]))
        print("---")
        print(output.files)
        return output

    @classmethod
    def validate_config(self, config: ComponentConfig) -> None:
        # Custom validation can be done by specifiying a validate function like this one. Validate functions
        # can raise errors that will be returned to the parent through gRPC. Validate functions can
        # also return a sequence of strings representing the implicit dependencies of the resource.
        files = config.attributes.fields["files"].struct_value
        if files is None:
            raise Exception("A files attribute is required for playfile component.")
        return None