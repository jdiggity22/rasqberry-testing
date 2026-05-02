#!/usr/bin/env python3
"""
Static Text Display for 8x32 WS2812B LED Matrix
Displays the word "THINK" in rainbow colors without scrolling
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
DEFAULT_LED_PIN = board.D18
DEFAULT_BRIGHTNESS = 0.3
BLACK_COLOR = (0, 0, 0)
RAINBOW_COLORS = [
    (255, 0, 0),
    (255, 127, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 0, 255),
    (75, 0, 130),
    (148, 0, 211),
]

# 5x5 Font for letters (each letter is 5 pixels wide, 5 pixels tall)
# 1 = pixel on, 0 = pixel off
FONT = {
    'T': [
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ],
    'H': [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
    ],
    'I': [
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
    ],
    'N': [
        [1, 0, 0, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 1, 1],
        [1, 0, 0, 0, 1],
    ],
    'K': [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1],
    ],
    ' ': [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
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
        Assumes column-major zigzag wiring pattern (typical for pre-made matrix panels)
        - Even columns (0, 2, 4...): Data flows DOWN (top to bottom)
        - Odd columns (1, 3, 5...): Data flows UP (bottom to top)
        
        Args:
            x: X coordinate (0 to width-1)
            y: Y coordinate (0 to height-1)
            
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
    
    def render_static_rainbow_text(self, text):
        """
        Render centered static text using rainbow colors.
        
        Args:
            text: Text to render
        """
        self.clear()
        
        text = text.upper()
        text_width = len(text) * 6 - 1
        x_offset = max(0, (self.width - text_width) // 2)
        y_offset = max(0, (self.height - 5) // 2)
        
        current_x = x_offset
        
        for char_index, char in enumerate(text):
            if char in FONT:
                letter = FONT[char]
                
                for row_idx, row in enumerate(letter):
                    for col_idx, pixel in enumerate(row):
                        x_pos = current_x + col_idx
                        y_pos = y_offset + row_idx
                        
                        if pixel == 1 and 0 <= x_pos < self.width and 0 <= y_pos < self.height:
                            color = RAINBOW_COLORS[(char_index + col_idx + row_idx) % len(RAINBOW_COLORS)]
                            self.set_pixel(x_pos, y_pos, color)
                
                current_x += 6
        
        self.show()


def display_static_text(matrix, text, hold_time=None):
    """
    Display static text without scrolling.
    
    Args:
        matrix: LEDMatrix instance
        text: Text to display
        hold_time: Optional display duration in seconds (None = until Ctrl+C)
    """
    try:
        matrix.render_static_rainbow_text(text)
        
        if hold_time is None:
            while True:
                time.sleep(1)
        else:
            time.sleep(hold_time)
    
    except KeyboardInterrupt:
        print("\n⚠ Display interrupted by user")
        matrix.clear()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Display "THINK" statically in rainbow colors on 8x32 LED matrix',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scroll_think.py                    # Display continuously
  python scroll_think.py -d 10              # Show for 10 seconds
  python scroll_think.py -b 0.5             # Brighter display
  python scroll_think.py -t "THINK"         # Display different text
        """
    )
    
    parser.add_argument('-b', '--brightness', type=float, default=DEFAULT_BRIGHTNESS,
                        help=f'Brightness level 0.0-1.0 (default: {DEFAULT_BRIGHTNESS})')
    parser.add_argument('-d', '--duration', type=float, default=None,
                        help='Display duration in seconds (default: infinite until Ctrl+C)')
    parser.add_argument('-t', '--text', type=str, default='THINK',
                        help='Text to scroll (default: THINK)')
    parser.add_argument('--width', type=int, default=MATRIX_WIDTH,
                        help=f'Matrix width (default: {MATRIX_WIDTH})')
    parser.add_argument('--height', type=int, default=MATRIX_HEIGHT,
                        help=f'Matrix height (default: {MATRIX_HEIGHT})')
    
    args = parser.parse_args()
    
    # Validate brightness
    if not 0.0 <= args.brightness <= 1.0:
        print("Error: Brightness must be between 0.0 and 1.0")
        sys.exit(1)
    
    # Validate text contains only supported characters
    supported_chars = set(FONT.keys())
    text_chars = set(args.text.upper())
    unsupported = text_chars - supported_chars
    if unsupported:
        print(f"Warning: Unsupported characters will be skipped: {unsupported}")
    
    # Initialize matrix
    matrix = LEDMatrix(
        width=args.width,
        height=args.height,
        brightness=args.brightness
    )
    
    print(f"\n{'='*50}")
    print(f"Displaying '{args.text}' statically in rainbow colors")
    print(f"Duration: {args.duration or 'infinite'}")
    print(f"{'='*50}\n")
    print("Press Ctrl+C to stop\n")
    
    try:
        display_static_text(matrix, args.text, args.duration)
        print("\n✓ Display complete")
    finally:
        matrix.clear()
        print("✓ Display cleared")


if __name__ == "__main__":
    main()

# Made with Bob