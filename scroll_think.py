#!/usr/bin/env python3
"""
Scrolling Text Display for 8x32 WS2812B LED Matrix
Scrolls text in blue color with 8-pixel high letters
"""

import time
import board
import neopixel
import argparse
import sys

# Configuration for 8x32 LED Matrix
MATRIX_WIDTH = 32
MATRIX_HEIGHT = 8
TOTAL_LEDS = MATRIX_WIDTH * MATRIX_HEIGHT  # 256 LEDs
DEFAULT_LED_PIN = board.D10  # GPIO 10 (SPI MOSI)
DEFAULT_BRIGHTNESS = 0.3
DEFAULT_SCROLL_SPEED = 0.05  # Seconds between scroll steps
BLACK_COLOR = (0, 0, 0)
BLUE_COLOR = (0, 0, 255)

# 8x6 Font for letters (each letter is 6 pixels wide, 8 pixels tall)
# 1 = pixel on, 0 = pixel off
FONT_8x6 = {
    'T': [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
    ],
    'H': [
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
    ],
    'I': [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
    ],
    'N': [
        [1, 1, 0, 0, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1, 1],
        [1, 1, 0, 1, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
    ],
    'K': [
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 1, 1, 0],
        [1, 1, 1, 1, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 0, 0],
        [1, 1, 0, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
    ],
    ' ': [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ],
}


class LEDMatrix:
    """Class to handle 8x32 LED matrix operations"""
    
    def __init__(self, width=MATRIX_WIDTH, height=MATRIX_HEIGHT, 
                 pin=DEFAULT_LED_PIN, brightness=DEFAULT_BRIGHTNESS):
        """
        Initialize the LED matrix
        
        Args:
            width: Matrix width in pixels
            height: Matrix height in pixels
            pin: GPIO pin connected to the LED data line
            brightness: LED brightness (0.0 to 1.0)
        """
        self.width = width
        self.height = height
        self.num_pixels = width * height
        
        try:
            self.pixels = neopixel.NeoPixel(
                pin,
                self.num_pixels,
                brightness=brightness,
                auto_write=False,
                pixel_order=neopixel.GRB
            )
            print(f"✓ Initialized {width}x{height} LED matrix ({self.num_pixels} LEDs)")
            print(f"  Pin: {pin}, Brightness: {brightness}")
        except Exception as e:
            print(f"✗ Error initializing LED matrix: {e}")
            sys.exit(1)
    
    def xy_to_index(self, x, y):
        """
        Convert x,y coordinates to LED strip index
        Column-major zigzag wiring pattern (confirmed by hardware test)
        - Even columns (0, 2, 4...): Data flows TOP to BOTTOM
        - Odd columns  (1, 3, 5...): Data flows BOTTOM to TOP

        Args:
            x: X coordinate (0 to width-1, left to right)
            y: Y coordinate (0 to height-1, top to bottom)

        Returns:
            LED index in the strip
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None

        # Column-major zigzag pattern
        if x % 2 == 0:
            # Even columns: top to bottom
            index = x * self.height + y
        else:
            # Odd columns: bottom to top
            index = x * self.height + (self.height - 1 - y)

        return index
    
    def set_pixel(self, x, y, color):
        """
        Set a single pixel color
        
        Args:
            x: X coordinate
            y: Y coordinate
            color: RGB tuple
        """
        index = self.xy_to_index(x, y)
        if index is not None:
            self.pixels[index] = color
    
    def clear(self):
        """Clear all pixels"""
        self.pixels.fill(BLACK_COLOR)
        self.pixels.show()
    
    def show(self):
        """Update the display"""
        self.pixels.show()
    
    def render_text_at_position(self, text, x_offset, color=BLUE_COLOR):
        """
        Render text at a specific x position in blue color.
        
        Args:
            text: Text to render
            x_offset: X position offset for scrolling
            color: RGB color tuple (default: blue)
        """
        self.clear()
        
        text = text.upper()
        current_x = x_offset
        
        for char in text:
            if char in FONT_8x6:
                letter = FONT_8x6[char]
                
                for row_idx, row in enumerate(letter):
                    for col_idx, pixel in enumerate(row):
                        x_pos = current_x + col_idx
                        y_pos = row_idx
                        
                        if pixel == 1 and 0 <= x_pos < self.width and 0 <= y_pos < self.height:
                            self.set_pixel(x_pos, y_pos, color)
                
                current_x += 7  # 6 pixels wide + 1 pixel spacing
        
        self.show()


def scroll_text(matrix, text, scroll_speed=DEFAULT_SCROLL_SPEED, loops=None, color=BLUE_COLOR):
    """
    Scroll text across the display in blue color.
    
    Args:
        matrix: LEDMatrix instance
        text: Text to scroll
        scroll_speed: Delay between scroll steps in seconds
        loops: Number of times to loop (None = infinite)
        color: RGB color tuple (default: blue)
    """
    text = text.upper()
    text_width = len(text) * 7  # Each char is 6 pixels + 1 spacing
    
    loop_count = 0
    try:
        while True:
            # Scroll from right edge to completely off left edge
            for x_offset in range(matrix.width, -text_width - 1, -1):
                matrix.render_text_at_position(text, x_offset, color)
                time.sleep(scroll_speed)
            
            loop_count += 1
            if loops is not None and loop_count >= loops:
                break
    
    except KeyboardInterrupt:
        print("\n⚠ Scrolling interrupted by user")
        matrix.clear()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Scroll text in BLUE across 8x32 LED matrix with 8-pixel high letters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scroll_think.py                    # Scroll "THINK" continuously
  python scroll_think.py -l 3               # Scroll 3 times then stop
  python scroll_think.py -s 0.1             # Faster scrolling
  python scroll_think.py -t "HELLO"         # Scroll different text
  python scroll_think.py -b 0.5             # Brighter display
        """
    )
    
    parser.add_argument('-b', '--brightness', type=float, default=DEFAULT_BRIGHTNESS,
                        help=f'Brightness level 0.0-1.0 (default: {DEFAULT_BRIGHTNESS})')
    parser.add_argument('-s', '--speed', type=float, default=DEFAULT_SCROLL_SPEED,
                        help=f'Scroll speed in seconds per step (default: {DEFAULT_SCROLL_SPEED})')
    parser.add_argument('-l', '--loops', type=int, default=None,
                        help='Number of times to loop (default: infinite until Ctrl+C)')
    parser.add_argument('-t', '--text', type=str, default='THINK',
                        help='Text to scroll (default: THINK)')
    parser.add_argument('--width', type=int, default=MATRIX_WIDTH,
                        help=f'Matrix width (default: {MATRIX_WIDTH})')
    parser.add_argument('--height', type=int, default=MATRIX_HEIGHT,
                        help=f'Matrix height (default: {MATRIX_HEIGHT})')
    parser.add_argument('--test-fill', action='store_true',
                        help='Fill all LEDs solid blue for 5 seconds (wiring/pin diagnostic)')

    args = parser.parse_args()

    # Validate brightness
    if not 0.0 <= args.brightness <= 1.0:
        print("Error: Brightness must be between 0.0 and 1.0")
        sys.exit(1)

    # Initialize matrix
    matrix = LEDMatrix(
        width=args.width,
        height=args.height,
        brightness=args.brightness
    )

    # Diagnostic: fill all LEDs solid blue then exit
    if args.test_fill:
        print("→ Lighting LEDs 0-7 one at a time (0.5s each) — watch which physical LEDs light up")
        for i in range(8):
            matrix.pixels.fill(BLACK_COLOR)
            matrix.pixels[i] = BLUE_COLOR
            matrix.pixels.show()
            print(f"  LED index {i}")
            time.sleep(0.5)
        matrix.clear()
        print("✓ Done — note which direction the first 8 LEDs ran (left→right, top→bottom, etc.)")
        return

    # Validate text contains only supported characters
    supported_chars = set(FONT_8x6.keys())
    text_chars = set(args.text.upper())
    unsupported = text_chars - supported_chars
    if unsupported:
        print(f"Warning: Unsupported characters will be skipped: {unsupported}")

    print(f"\n{'='*50}")
    print(f"Scrolling '{args.text}' in BLUE")
    print(f"Speed: {args.speed}s per step")
    print(f"Loops: {args.loops or 'infinite'}")
    print(f"{'='*50}\n")
    print("Press Ctrl+C to stop\n")

    try:
        scroll_text(matrix, args.text, args.speed, args.loops, BLUE_COLOR)
        print("\n✓ Scrolling complete")
    finally:
        matrix.clear()
        print("✓ Display cleared")


if __name__ == "__main__":
    main()

# Made with Bob