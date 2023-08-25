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

#   Addr(BIN)      Addr(hex)
#XXX X  A2 A1 A0
#010 0  1  1  1      0x27 
#010 0  1  1  0      0x26 
#010 0  1  0  1      0x25 
#010 0  1  0  0      0x24 
#010 0  0  1  1      0x23 
#010 0  0  1  0      0x22
#010 0  0  0  1      0x21
#010 0  0  0  0      0x20

MCP23017_ADDRESS = 0x27

# def binToHexa(n):
   
#     # convert binary to int
#     num = int(n, 2)
     
#     # convert int to hexadecimal
#     hex_num = hex(num)
#     return(hex_num)

# 7-segment LED datasheet http://www.xlitx.com/Products/7-segment-led-dot-matrix/cl5611ah.html
# Consider purchasing: https://www.adafruit.com/product/5346

# alpha https://en.wikichip.org/wiki/seven-segment_display/representing_letters
# digit gfedcba https://www.electronicsforu.com/resources/7-segment-display-pinout-understanding
# digit abcdefg https://support.aimagin.com/projects/support/wiki/How_to_Drive_a_7-Segment_LED

# wiring the MCP23017:
# abcdefg mode: a -> P6 ... g->P0
# gfedcba mode: a -> P0 ... g->P6

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

# non standard first try
# numbers = {
#     "0": 0b01110111,
#     "1": 0b00010100,
#     "2": 0b10110011,
#     "3": 0b10110110,
#     "4": 0b11010100,
#     "5": 0b11100110,
#     "6": 0b11100111,
#     "7": 0b00110100,
#     "8": 0b11110111,
#     "9": 0b11110100,
# }

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
 
for line in sys.stdin:
    if 'q' == line.rstrip():
        break
    print(f'Input : {line}')
    for char in line.rstrip():
        print(char)
        mapping = mappings.get(char, mappings.get(char.lower(), mappings.get(char.upper())))
        if mapping is not None:
            #print(hex(mapping[MODE]))
            bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOA,mapping['gfedcba'])
            bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOB,mapping['abcdefg'])
            #print(bus.read_byte_data(MCP23017_ADDRESS,MCP23017_GPIOB))
            time.sleep(0.5)
            bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOA,0x00)
            bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOB,0x00)
            time.sleep(0.5)
        else:
            print("nope")

    # bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOB,int(line.strip(),16))
    
    #configue all PinA output high level
#    for v in numbers.values():
#        bus.write_byte_data(MCP23017_ADDRESS,MCP23017_GPIOB,v)
#        time.sleep(0.5)
    #then PinB read the level from PinA, print 255 means all PinA are in high level
    # print(bus.read_byte_data(MCP23017_ADDRESS,MCP23017_GPIOB))
    # time.sleep(0.5)
    
