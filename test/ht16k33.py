# Import all board pins and bus interface.
import board
import busio

# Import the HT16K33 LED matrix module.
from adafruit_ht16k33 import segments

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

alpha = segments.Seg14x4(i2c=i2c, address=[0x70], auto_write=True, chars_per_display=4)
alpha.marquee("MICHAEL@VIAM.COM    ")