#!/usr/bin/env python3
"""
Scrolling Text Display for 8x32 WS2812B LED Matrix
Scrolls the word "THINK" in BLUE across the display
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
BLUE_COLOR = (0, 0, 255)
BLACK_COLOR = (0, 0, 0)

# 5x7 Font for letters (each letter is 5 pixels wide, 7 pixels tall)
# 1 = pixel on, 0 = pixel off
FONT = {
    'T': [
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ],
    'H': [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
    ],
    'I': [
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
    ],
    'N': [
        [1, 0, 0, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
    ],
    'K': [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0],
        [1, 0, 1, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1],
    ],
    ' ': [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
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
        Assumes serpentine (zigzag) wiring pattern
        
        Args:
            x: X coordinate (0 to width-1)
            y: Y coordinate (0 to height-1)
            
        Returns:
            LED index in the strip
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        
        # Serpentine pattern: even rows go left-to-right, odd rows go right-to-left
        if y % 2 == 0:
            # Even row: left to right
            index = y * self.width + x
        else:
            # Odd row: right to left
            index = y * self.width + (self.width - 1 - x)
        
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
    
    def render_text(self, text, x_offset, color=BLUE_COLOR):
        """
        Render text on the matrix at given x offset
        
        Args:
            text: Text to render
            x_offset: Horizontal offset for scrolling
            color: RGB color tuple
        """
        self.clear()
        
        current_x = x_offset
        
        for char in text.upper():
            if char in FONT:
                letter = FONT[char]
                
                # Draw each column of the letter
                for col_idx, column in enumerate(zip(*letter)):
                    x_pos = current_x + col_idx
                    
                    # Only draw if within visible area
                    if 0 <= x_pos < self.width:
                        for y_pos, pixel in enumerate(column):
                            if pixel == 1:
                                # Center vertically (7 pixel font in 8 pixel height)
                                y_centered = y_pos
                                if y_centered < self.height:
                                    self.set_pixel(x_pos, y_centered, color)
                
                # Move to next letter position (5 pixels wide + 1 pixel spacing)
                current_x += 6
        
        self.show()


def scroll_text(matrix, text, color=BLUE_COLOR, speed=0.05, loops=None):
    """
    Scroll text across the matrix
    
    Args:
        matrix: LEDMatrix instance
        text: Text to scroll
        color: RGB color tuple
        speed: Delay between frames (seconds)
        loops: Number of times to loop (None = infinite)
    """
    # Calculate text width (each letter is 5 pixels + 1 spacing)
    text_width = len(text) * 6
    
    # Start position (off-screen right)
    start_x = matrix.width
    # End position (completely off-screen left)
    end_x = -text_width
    
    loop_count = 0
    
    try:
        while True:
            # Scroll from right to left
            for x in range(start_x, end_x - 1, -1):
                matrix.render_text(text, x, color)
                time.sleep(speed)
            
            loop_count += 1
            
            # Check if we should stop
            if loops is not None and loop_count >= loops:
                break
            
            print(f"  Loop {loop_count} complete", end='\r')
    
    except KeyboardInterrupt:
        print("\n⚠ Scrolling interrupted by user")
        matrix.clear()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Scroll "THINK" in BLUE across 8x32 LED matrix',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scroll_think.py                    # Scroll continuously
  python scroll_think.py -l 5               # Scroll 5 times
  python scroll_think.py -s 0.03            # Faster scrolling
  python scroll_think.py -b 0.5             # Brighter display
  python scroll_think.py -t "HELLO"         # Scroll different text
        """
    )
    
    parser.add_argument('-b', '--brightness', type=float, default=DEFAULT_BRIGHTNESS,
                        help=f'Brightness level 0.0-1.0 (default: {DEFAULT_BRIGHTNESS})')
    parser.add_argument('-s', '--speed', type=float, default=0.05,
                        help='Scroll speed in seconds per frame (default: 0.05)')
    parser.add_argument('-l', '--loops', type=int, default=None,
                        help='Number of times to loop (default: infinite)')
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
    print(f"Scrolling '{args.text}' in BLUE")
    print(f"Speed: {args.speed}s/frame, Loops: {args.loops or 'infinite'}")
    print(f"{'='*50}\n")
    print("Press Ctrl+C to stop\n")
    
    try:
        scroll_text(matrix, args.text, BLUE_COLOR, args.speed, args.loops)
        print("\n✓ Scrolling complete")
    finally:
        matrix.clear()
        print("✓ Display cleared")


if __name__ == "__main__":
    main()

# Made with Bob