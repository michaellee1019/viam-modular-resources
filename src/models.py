import json
import sys

from typing import ClassVar, Mapping, Sequence, Optional

from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.utils import ValueTypes
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.components.generic import Generic
from google.protobuf import json_format

import smbus
import time
import pygame

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

import sys

class EightSegmentLED(Generic):
    MODEL: ClassVar[Model] = Model(ModelFamily("michaellee1019", "mcp23017"), "eight_segment")
    device: str
    bus = None

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        result = {key: False for key in command.keys()}
        for (name, args) in command.items():
            if name == 'flash_word':
                if 'word' in args:
                    results = await self.flash_word(args['word'])
                    result[name] = 'flashed: ' + results
                else:
                    result[name] = 'missing word key'
        return result

    async def flash_word(self, word: str) -> str:
        for char in word:
            mapping = mappings.get(char, mappings.get(char.lower(), mappings.get(char.upper())))
            if mapping is not None:
                self.bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOA,mapping['gfedcba'])
                self.bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOB,mapping['abcdefg'])
                time.sleep(0.5)
                self.bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOA,0x00)
                self.bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOB,0x00)
                time.sleep(0.5)
        return word

    @classmethod
    def new(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        self.bus = smbus.SMBus(1)

        #Configue the register to default value
        for addr in range(22):
            if (addr == 0) or (addr == 1):
                self.bus.write_byte_data(MCP23017_ADDRESS, addr, 0xFF)
            else:
                self.bus.write_byte_data(MCP23017_ADDRESS, addr, 0x00)

        #configue all PinA + PinB output
        self.bus.write_byte_data(MCP23017_ADDRESS,MCP23017_IODIRA,0x00)
        self.bus.write_byte_data(MCP23017_ADDRESS,MCP23017_IODIRB,0x00)

        output = self(config.name)
        output.device = config.attributes.fields["device"].string_value
        return output

    @classmethod
    def validate_config(self, config: ComponentConfig) -> None:
        # Custom validation can be done by specifiying a validate function like this one. Validate functions
        # can raise errors that will be returned to the parent through gRPC. Validate functions can
        # also return a sequence of strings representing the implicit dependencies of the resource.
        device = config.attributes.fields["device"]
        if device is None:
            raise Exception("A device attribute is required for eight_segment component.")
        return None

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
                if 'filename' in args:
                    results = await self.play_file(args['filename'])
                    result[name] = 'played: ' + results
                else:
                    result[name] = 'missing filename key'
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

CMD_CHANNEL_CTRL=0x10
CMD_SAVE_I2C_ADDR=0x11
CMD_READ_I2C_ADDR=0x12
CMD_READ_FIRMWARE_VER=0x13

class Grove4ChannelSPDTRelay(Generic):
    MODEL: ClassVar[Model] = Model(ModelFamily("michaellee1019", "grove"), "4_channel_spdt_relay")
    bus = None

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        result = {key: False for key in command.keys()}
        for (name, args) in command.items():
            if name == 'pulse_one':
                if all(arg in args for arg in ("address","bit","pulse_seconds")):
                    results = await self.pulse_one(args['address'], args['bit'], args['pulse_seconds'])
                    result[name] = 'pulsed: ' + results
                else:
                    result[name] = 'missing address, bit, or pulse_seconds parameters'
        return result

    async def pulse_one(self, address: str, bit: str, pulse_seconds: str) -> str:
        hex_address = int(address, 16)
        hex_bit = int(bit, 16)
        self.bus.write_byte_data(hex_address,CMD_CHANNEL_CTRL,hex_bit)
        time.sleep(float(pulse_seconds))
        self.bus.write_byte_data(hex_address,CMD_CHANNEL_CTRL,0x00)
        return "{0} {1}".format(hex(hex_address), hex(hex_bit))

    @classmethod
    def new(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        self.bus = smbus.SMBus(1)
        output = self(config.name)
        return output

    @classmethod
    def validate_config(self, config: ComponentConfig) -> None:
        # Custom validation can be done by specifiying a validate function like this one. Validate functions
        # can raise errors that will be returned to the parent through gRPC. Validate functions can
        # also return a sequence of strings representing the implicit dependencies of the resource.
        return None

# Import all board pins and bus interface.
import board
import busio

# Import the HT16K33 LED matrix module.
from adafruit_ht16k33 import segments

class Ht16k33_Seg14x4(Generic):
    MODEL: ClassVar[Model] = Model(ModelFamily("michaellee1019", "ht16k33"), "seg_14_x_4")
    i2c = None
    segs = None

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        result = {key: False for key in command.keys()}
        for (name, args) in command.items():
            if name == 'marquee':
                if 'text' in args:
                    #TODO: NoneType is not converted to None
                    await self.marquee(args['text'], args.get('delay'), args.get('loop'),)
                    result[name] = True
                else:
                    result[name] = 'missing text parameter'
            if name == 'print':
                if 'value' in args:
                    #TODO: NoneType is not converted to None
                    self.print(args['value'], args.get('decimal'))
                    result[name] = True
                else:
                    result[name] = 'missing value parameter'
        return result

    
    async def marquee(self, text: str, delay: float, loop: bool) -> None:
        # TODO fix async issues and allow loop
        self.segs.marquee(text, loop = False) #delay=delay, loop=loop)

    def print(self, value, decimal: int = 0) -> None: #value: str | float
        self.segs.print(value, decimal = decimal)

    @classmethod
    def new(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        self.i2c = busio.I2C(board.SCL, board.SDA)
        
        addresses = config.attributes.fields["address"].list_value
        hex_addresses=[]
        for address in addresses:
            hex_addresses.append(int(address,16))
        
        self.segs = segments.Seg14x4(i2c=self.i2c, address=hex_addresses, auto_write=True, chars_per_display=4)

        output = self(config.name)
        return output

    @classmethod
    def validate_config(self, config: ComponentConfig) -> None:
        address = config.attributes.fields["address"].list_value
        if address is None:
            raise Exception('A address attribute is required for seg_14_x_4 component. Must be a string array of 1 or more addresses in hexidecimal format such as "0x00".')
        
        # TODO: assert len()>1, parse addresses here
        
        return None
