import time
import board
import neopixel_spi as neopixel
import random

# Initialize constants
TOTAL_LEDS = 8*5+24+24+24+24+24  # Total number of LEDs to control

# Initialize NeoPixel object
spi_bus = board.SPI()  # Assuming default SPI bus, adjust as needed
pixels = neopixel.NeoPixel_SPI(spi_bus, TOTAL_LEDS, pixel_order=neopixel.GRB, auto_write=False)

def pick_random_color():
    # Pick a random color
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def cycle_leds():
    while True:
        # Pick a random color
        color = pick_random_color()
        print(f"Using color: {color}")

        # Turn on LEDs one at a time
        for i in range(TOTAL_LEDS):
            pixels[i] = color
            pixels.show()
            time.sleep(0.05)  # Adjust the delay to control the speed

        # Keep all LEDs on for a short duration
        time.sleep(2)

        # Turn off all LEDs
        for i in range(TOTAL_LEDS):
            pixels[i] = (0, 0, 0)
            pixels.show()
            time.sleep(0.05)  # Adjust the delay to control the speed

        # Wait before picking a new color
        time.sleep(1)

if __name__ == "__main__":
    cycle_leds()