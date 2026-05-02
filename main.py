#!/usr/bin/env python3
"""
WS2812B LED Test Program for Raspberry Pi 5
Tests various LED patterns and colors to verify proper operation
"""

import time
import board
import neopixel
import argparse
import sys
from typing import Tuple

# Configuration
DEFAULT_LED_COUNT = 8
DEFAULT_LED_PIN = board.D18  # GPIO 18 (PWM0)
DEFAULT_BRIGHTNESS = 0.5
DEFAULT_AUTO_WRITE = False
DEFAULT_PIXEL_ORDER = neopixel.GRB


class LEDTester:
    """Class to handle WS2812B LED testing operations"""
    
    def __init__(self, num_pixels: int = DEFAULT_LED_COUNT, 
                 pin=DEFAULT_LED_PIN, 
                 brightness: float = DEFAULT_BRIGHTNESS,
                 auto_write: bool = DEFAULT_AUTO_WRITE,
                 pixel_order=DEFAULT_PIXEL_ORDER):
        """
        Initialize the LED tester
        
        Args:
            num_pixels: Number of LEDs in the strip
            pin: GPIO pin connected to the LED data line
            brightness: LED brightness (0.0 to 1.0)
            auto_write: Whether to automatically update LEDs
            pixel_order: Pixel color order (GRB, RGB, etc.)
        """
        try:
            self.pixels = neopixel.NeoPixel(
                pin, 
                num_pixels, 
                brightness=brightness,
                auto_write=auto_write,
                pixel_order=pixel_order
            )
            self.num_pixels = num_pixels
            print(f"✓ Initialized {num_pixels} LEDs on pin {pin}")
            print(f"  Brightness: {brightness}, Auto-write: {auto_write}")
        except Exception as e:
            print(f"✗ Error initializing LEDs: {e}")
            sys.exit(1)
    
    def clear(self):
        """Turn off all LEDs"""
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
    
    def set_color(self, color: Tuple[int, int, int]):
        """Set all LEDs to a specific color"""
        self.pixels.fill(color)
        self.pixels.show()
    
    def test_individual_leds(self, color: Tuple[int, int, int] = (255, 0, 0), delay: float = 0.1):
        """
        Test each LED individually
        
        Args:
            color: RGB color tuple
            delay: Delay between LEDs in seconds
        """
        print(f"\n→ Testing individual LEDs with color {color}...")
        self.clear()
        
        for i in range(self.num_pixels):
            self.pixels[i] = color
            self.pixels.show()
            print(f"  LED {i+1}/{self.num_pixels} ON", end='\r')
            time.sleep(delay)
            self.pixels[i] = (0, 0, 0)
            self.pixels.show()
        
        print(f"  ✓ All {self.num_pixels} LEDs tested individually")
    
    def test_colors(self, delay: float = 1.0):
        """
        Test primary colors (Red, Green, Blue, White)
        
        Args:
            delay: Delay between colors in seconds
        """
        print("\n→ Testing primary colors...")
        colors = {
            'Red': (255, 0, 0),
            'Green': (0, 255, 0),
            'Blue': (0, 0, 255),
            'White': (255, 255, 255),
            'Yellow': (255, 255, 0),
            'Cyan': (0, 255, 255),
            'Magenta': (255, 0, 255)
        }
        
        for name, color in colors.items():
            print(f"  {name}: {color}")
            self.set_color(color)
            time.sleep(delay)
        
        self.clear()
        print("  ✓ Color test complete")
    
    def test_rainbow(self, iterations: int = 2, delay: float = 0.01):
        """
        Display a rainbow pattern
        
        Args:
            iterations: Number of times to cycle through rainbow
            delay: Delay between updates in seconds
        """
        print(f"\n→ Testing rainbow pattern ({iterations} iterations)...")
        
        def wheel(pos):
            """Generate rainbow colors across 0-255 positions"""
            if pos < 85:
                return (pos * 3, 255 - pos * 3, 0)
            elif pos < 170:
                pos -= 85
                return (255 - pos * 3, 0, pos * 3)
            else:
                pos -= 170
                return (0, pos * 3, 255 - pos * 3)
        
        for j in range(256 * iterations):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(delay)
        
        self.clear()
        print("  ✓ Rainbow test complete")
    
    def test_chase(self, color: Tuple[int, int, int] = (255, 255, 255), 
                   iterations: int = 3, delay: float = 0.1):
        """
        Chase pattern along the strip
        
        Args:
            color: RGB color tuple
            iterations: Number of complete chases
            delay: Delay between steps in seconds
        """
        print(f"\n→ Testing chase pattern with color {color}...")
        
        for _ in range(iterations):
            for i in range(self.num_pixels):
                self.clear()
                self.pixels[i] = color
                self.pixels.show()
                time.sleep(delay)
        
        self.clear()
        print("  ✓ Chase test complete")
    
    def test_brightness_levels(self, color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Test different brightness levels
        
        Args:
            color: RGB color tuple to test
        """
        print(f"\n→ Testing brightness levels with color {color}...")
        levels = [0.1, 0.25, 0.5, 0.75, 1.0]
        
        for level in levels:
            print(f"  Brightness: {level}")
            self.pixels.brightness = level
            self.set_color(color)
            time.sleep(1)
        
        self.pixels.brightness = DEFAULT_BRIGHTNESS
        self.clear()
        print("  ✓ Brightness test complete")
    
    def run_all_tests(self):
        """Run all test patterns"""
        print("\n" + "="*50)
        print("WS2812B LED Strip Test Suite")
        print("="*50)
        
        try:
            # Test 1: Individual LEDs
            self.test_individual_leds(color=(255, 0, 0), delay=0.1)
            time.sleep(0.5)
            
            # Test 2: Primary colors
            self.test_colors(delay=1.0)
            time.sleep(0.5)
            
            # Test 3: Rainbow
            self.test_rainbow(iterations=2, delay=0.01)
            time.sleep(0.5)
            
            # Test 4: Chase pattern
            self.test_chase(color=(0, 255, 0), iterations=3, delay=0.1)
            time.sleep(0.5)
            
            # Test 5: Brightness levels
            self.test_brightness_levels(color=(255, 255, 255))
            
            print("\n" + "="*50)
            print("✓ All tests completed successfully!")
            print("="*50)
            
        except KeyboardInterrupt:
            print("\n\n⚠ Tests interrupted by user")
            self.clear()
        except Exception as e:
            print(f"\n✗ Error during testing: {e}")
            self.clear()
            raise


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Test WS2812B LED strip on Raspberry Pi 5',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run all tests with default settings
  python main.py -n 16              # Test 16 LEDs
  python main.py -b 0.3             # Set brightness to 30%
  python main.py --test colors      # Run only color test
  python main.py --test rainbow     # Run only rainbow test
        """
    )
    
    parser.add_argument('-n', '--num-leds', type=int, default=DEFAULT_LED_COUNT,
                        help=f'Number of LEDs (default: {DEFAULT_LED_COUNT})')
    parser.add_argument('-b', '--brightness', type=float, default=DEFAULT_BRIGHTNESS,
                        help=f'Brightness level 0.0-1.0 (default: {DEFAULT_BRIGHTNESS})')
    parser.add_argument('--test', choices=['individual', 'colors', 'rainbow', 'chase', 'brightness', 'all'],
                        default='all', help='Specific test to run (default: all)')
    
    args = parser.parse_args()
    
    # Validate brightness
    if not 0.0 <= args.brightness <= 1.0:
        print("Error: Brightness must be between 0.0 and 1.0")
        sys.exit(1)
    
    # Initialize tester
    tester = LEDTester(
        num_pixels=args.num_leds,
        brightness=args.brightness
    )
    
    try:
        # Run requested test
        if args.test == 'all':
            tester.run_all_tests()
        elif args.test == 'individual':
            tester.test_individual_leds()
        elif args.test == 'colors':
            tester.test_colors()
        elif args.test == 'rainbow':
            tester.test_rainbow()
        elif args.test == 'chase':
            tester.test_chase()
        elif args.test == 'brightness':
            tester.test_brightness_levels()
        
    finally:
        # Always clear LEDs on exit
        tester.clear()
        print("\n✓ LEDs cleared")


if __name__ == "__main__":
    main()

# Made with Bob
