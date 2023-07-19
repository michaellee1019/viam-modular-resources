import sys
sys.path.append("..")

from typing import ClassVar, Mapping, Sequence

from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from .apis import MCP23017

import smbus
import time

MCP23017_IODIRA = 0x00
MCP23017_IPOLA  = 0x02
MCP23017_GPINTENA = 0x04
MCP23017_DEFVALA = 0x06
MCP23017_INTCONA = 0x08
MCP23017_IOCONA = 0x0A
MCP23017_GPPUA = 0x0C
MCP23017_INTFA = 0x0E
MCP23017_INTCAPA = 0x10
MCP23017_GPIOA = 0x12
MCP23017_OLATA = 0x14

MCP23017_IODIRB = 0x01
MCP23017_IPOLB = 0x03
MCP23017_GPINTENB = 0x05
MCP23017_DEFVALB = 0x07
MCP23017_INTCONB = 0x09
MCP23017_IOCONB = 0x0B
MCP23017_GPPUB = 0x0D
MCP23017_INTFB = 0x0F
MCP23017_INTCAPB = 0x11
MCP23017_GPIOB = 0x13
MCP23017_OLATB = 0x15

bus = smbus.SMBus(1)
MCP23017_ADDRESS = 0x27

mappings = {		
    'A': {'abcdefg': 0x77, 'gfedcba': 0x77},
    'a': {'abcdefg': 0x7D, 'gfedcba': 0x5F},
    'b': {'abcdefg': 0x1F, 'gfedcba': 0x7C},
    'C': {'abcdefg': 0x4E, 'gfedcba': 0x39},
    'c': {'abcdefg': 0x0D, 'gfedcba': 0x58},
    'd': {'abcdefg': 0x3D, 'gfedcba': 0x5E},
    'E': {'abcdefg': 0x4F, 'gfedcba': 0x79},
    'F': {'abcdefg': 0x47, 'gfedcba': 0x71},
    'G': {'abcdefg': 0x5E, 'gfedcba': 0x3D},
    'H': {'abcdefg': 0x37, 'gfedcba': 0x76},
    'h': {'abcdefg': 0x17, 'gfedcba': 0x74},
    'I': {'abcdefg': 0x06, 'gfedcba': 0x30},
    'J': {'abcdefg': 0x3C, 'gfedcba': 0x1E},
    'L': {'abcdefg': 0x0E, 'gfedcba': 0x38},
    'n': {'abcdefg': 0x15, 'gfedcba': 0x54},
    'O': {'abcdefg': 0x7E, 'gfedcba': 0x3F},
    'o': {'abcdefg': 0x1D, 'gfedcba': 0x5C},
    'P': {'abcdefg': 0x67, 'gfedcba': 0x73},
    'q': {'abcdefg': 0x73, 'gfedcba': 0x67},
    'r': {'abcdefg': 0x05, 'gfedcba': 0x50},
    'S': {'abcdefg': 0x5B, 'gfedcba': 0x6D},
    't': {'abcdefg': 0x0F, 'gfedcba': 0x78},
    'U': {'abcdefg': 0x3E, 'gfedcba': 0x3E},
    'u': {'abcdefg': 0x1C, 'gfedcba': 0x1C},
    'y': {'abcdefg': 0x3B, 'gfedcba': 0x6E},
    '0': {'abcdefg': 0x7E, 'gfedcba': 0xC0},
    '1': {'abcdefg': 0x30, 'gfedcba': 0xF9},
    '2': {'abcdefg': 0x6D, 'gfedcba': 0xA4},
    '3': {'abcdefg': 0x79, 'gfedcba': 0xB0},
    '4': {'abcdefg': 0x33, 'gfedcba': 0x99},
    '5': {'abcdefg': 0x5B, 'gfedcba': 0x92},
    '6': {'abcdefg': 0x5F, 'gfedcba': 0x82},
    '7': {'abcdefg': 0x70, 'gfedcba': 0xF8},
    '8': {'abcdefg': 0x7F, 'gfedcba': 0x80},
    '9': {'abcdefg': 0x7B, 'gfedcba': 0x90},
    ' ': {'abcdefg': 0x00, 'gfedcba': 0x00},
}

MODE = 'gfedcba'

#Configue the register to default value
for addr in range(22):
    if (addr == 0) or (addr == 1):
        bus.write_byte_data(MCP23017_ADDRESS, addr, 0xFF)
    else:
        bus.write_byte_data(MCP23017_ADDRESS, addr, 0x00)

    
#configue all PinA + PinB output
bus.write_byte_data(MCP23017_ADDRESS,MCP23017_IODIRA,0x00)
bus.write_byte_data(MCP23017_ADDRESS,MCP23017_IODIRB,0x00)

import sys

class EightSegmentLED(MCP23017, Reconfigurable):
    MODEL: ClassVar[Model] = Model(ModelFamily("michaellee1019", "mcp23017"), "eightsegment")
    device: str

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        output = cls(config.name)
        output.device = config.attributes.fields["device"].string_value
        return output

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> None:
        # Custom validation can be done by specifiying a validate function like this one. Validate functions
        # can raise errors that will be returned to the parent through gRPC. Validate functions can
        # also return a sequence of strings representing the implicit dependencies of the resource.
        device = config.attributes.fields["device"]
        if device is None:
            raise Exception("A device attribute is required for eightsegment component.")
        return None

    async def flash_word(self, word: str, **kwargs) -> None:
        for char in word:
            print(char)
            mapping = mappings.get(char, mappings.get(char.lower(), mappings.get(char.upper())))
            if mapping is not None:
                bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOA,mapping['gfedcba'])
                bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOB,mapping['abcdefg'])
                time.sleep(0.5)
                bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOA,0x00)
                bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOB,0x00)
                time.sleep(0.5)
            else:
                print("nope")
        pass

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.device = config.attributes.fields["device"]