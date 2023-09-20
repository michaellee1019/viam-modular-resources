"""CircuitPython Essentials NeoPixel example"""
import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer
import random
import time
import sys
from PIL import Image

pixels = neopixel.NeoPixel(board.D18, 64)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

pixel_framebuf = PixelFramebuffer(
    pixels,
    8,
    8,
    reverse_x=True,
)

# Make a black background in RGBA Mode
image = Image.new("RGBA", (8, 8))

# Open the icon
icon = Image.open("blinka_16x16.png")

# Alpha blend the icon onto the background
image.alpha_composite(icon)

# Convert the image to RGB and display it
pixel_framebuf.image(image.convert("RGB"))
pixel_framebuf.display()

# pixel_framebuf.hline(0, 0, 5, 0x110000)
# pixel_framebuf.vline(0, 0, 5, 0xFF0000)
# pixel_framebuf.display()

# pixel_framebuf.fill(0x111111)
# pixel_framebuf.text(str(sys.argv[1]), 1, 0, 0x0000FF)
# pixel_framebuf.display()

# while True:
#     r = random.randint(0, 255)
#     g = random.randint(0, 255)
#     b = random.randint(0, 255)
#     rgb = r<<16 | g<<8 | b
#     # color = "#{0:02x}{1:02x}{2:02x}".format(r,g,b)
#     # print(color)
#     pixel_framebuf.fill(rgb)
#     pixel_framebuf.display()
#     time.sleep(.1)