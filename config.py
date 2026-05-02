"""
Configuration file for WS2812B LED strip settings
Modify these values to match your hardware setup
"""

import board

# ============================================================================
# LED STRIP CONFIGURATION
# ============================================================================

# Number of LEDs in your strip
LED_COUNT = 8

# GPIO pin connected to the LED strip data line
# Common options for Raspberry Pi 5:
# - board.D18 (GPIO 18, PWM0) - Recommended for best performance
# - board.D10 (GPIO 10, SPI MOSI) - For SPI mode
# - board.D12 (GPIO 12, PWM0)
# - board.D21 (GPIO 21, PWM1)
LED_PIN = board.D18

# LED brightness (0.0 to 1.0)
# Start with lower values to avoid excessive power draw
BRIGHTNESS = 0.5

# Pixel color order
# Common values: GRB, RGB, GRBW, RGBW
# WS2812B typically uses GRB
PIXEL_ORDER = "GRB"

# Auto-write mode
# If True, changes are immediately sent to LEDs
# If False, you must call pixels.show() to update
AUTO_WRITE = False

# ============================================================================
# POWER CONFIGURATION
# ============================================================================

# Maximum current per LED in milliamps (typically 60mA at full white)
MAX_CURRENT_PER_LED = 60

# Power supply voltage (typically 5V for WS2812B)
POWER_SUPPLY_VOLTAGE = 5.0

# Calculate estimated maximum current draw
ESTIMATED_MAX_CURRENT = (LED_COUNT * MAX_CURRENT_PER_LED) / 1000  # in Amps

# ============================================================================
# TEST CONFIGURATION
# ============================================================================

# Default delay between test steps (seconds)
TEST_DELAY = 0.1

# Number of rainbow iterations
RAINBOW_ITERATIONS = 2

# Number of chase pattern iterations
CHASE_ITERATIONS = 3

# Colors for testing (R, G, B)
TEST_COLORS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'white': (255, 255, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'orange': (255, 165, 0),
    'purple': (128, 0, 128),
}

# ============================================================================
# HARDWARE NOTES
# ============================================================================

"""
Raspberry Pi 5 WS2812B Connection:
- LED Data Pin -> GPIO 18 (Pin 12)
- LED 5V -> External 5V power supply positive
- LED GND -> Raspberry Pi GND + Power supply GND (common ground)

IMPORTANT:
1. WS2812B strips can draw significant current. Use an external power supply
   for more than a few LEDs.
2. Add a 300-500 ohm resistor between GPIO and LED data line for signal protection.
3. Add a 1000µF capacitor across the power supply to prevent voltage spikes.
4. Keep data wire short (< 1 meter) or use a level shifter for longer runs.
5. Ensure common ground between Raspberry Pi and power supply.

Power Calculation:
- Estimated max current for {LED_COUNT} LEDs: {ESTIMATED_MAX_CURRENT:.2f}A
- Recommended power supply: {ESTIMATED_MAX_CURRENT * 1.2:.2f}A or higher
"""

# ============================================================================
# ADVANCED CONFIGURATION
# ============================================================================

# SPI Configuration (if using SPI mode instead of PWM)
USE_SPI = False
SPI_BUS = None  # Will use default SPI bus if None

# Frequency for PWM (Hz) - typically 800000 for WS2812B
# Note: This is usually handled automatically by the library
LED_FREQ_HZ = 800000

# DMA channel (for rpi_ws281x library)
# -1 means auto-select
DMA_CHANNEL = 10

# GPIO PWM channel
PWM_CHANNEL = 0

# Invert signal (usually False for WS2812B)
INVERT_SIGNAL = False

# Made with Bob
