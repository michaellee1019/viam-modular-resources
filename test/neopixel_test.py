"""CircuitPython Essentials NeoPixel example"""
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 64)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

pixels.fill(YELLOW)