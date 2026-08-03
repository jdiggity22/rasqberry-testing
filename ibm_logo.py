#!/usr/bin/env python3
"""
IBM 8-Bar Logo Scroller for 8x32 WS2812B LED Matrix
Scrolls the IBM logo in classic IBM blue across the display.

The IBM 8-bar logo is rendered as 8 horizontal bars (one per LED row).
Each letter (I, B, M) is 8 columns wide with a 2-column gap between letters.
"""

import time
import board
import neopixel
import argparse
import sys

# Configuration
MATRIX_WIDTH = 32
MATRIX_HEIGHT = 8
TOTAL_LEDS = MATRIX_WIDTH * MATRIX_HEIGHT  # 256 LEDs
DEFAULT_LED_PIN = board.D10  # GPIO 10 (SPI MOSI)
DEFAULT_BRIGHTNESS = 0.225
DEFAULT_SCROLL_SPEED = 0.0665  # Seconds between scroll steps
BLACK_COLOR = (0, 0, 0)
IBM_BLUE = (0, 98, 255)  # IBM brand blue

# IBM 8-bar logo — each letter is 8 columns wide, 8 rows tall.
# Each inner list is one ROW (top to bottom), each value is one COLUMN (left to right).
# 1 = bar pixel on, 0 = gap pixel off.
#
# The 8-bar pattern means every row is a bar; the IBM shape is expressed
# by which columns are illuminated in each row.
#
#   I  — solid 6-wide column block (serifs top/bottom, stem in middle)
#   B  — left spine always on; bumps on top half and bottom half
#   M  — outer columns always on; inner diagonal V
#
# Each letter: 8 cols wide. Gap between letters: 2 cols of black (implicit via spacing).

IBM_LOGO = {
    # I: serif top (full width), stem (centre 2), serif bottom (full width)
    'I': [
        [1, 1, 1, 1, 1, 1, 1, 1],  # row 0 — top serif (full bar)
        [1, 1, 1, 1, 1, 1, 1, 1],  # row 1 — top serif (full bar)
        [0, 0, 0, 1, 1, 0, 0, 0],  # row 2 — stem
        [0, 0, 0, 1, 1, 0, 0, 0],  # row 3 — stem
        [0, 0, 0, 1, 1, 0, 0, 0],  # row 4 — stem
        [0, 0, 0, 1, 1, 0, 0, 0],  # row 5 — stem
        [1, 1, 1, 1, 1, 1, 1, 1],  # row 6 — bottom serif (full bar)
        [1, 1, 1, 1, 1, 1, 1, 1],  # row 7 — bottom serif (full bar)
    ],
    # B: left spine (cols 0-1) always; right bumps on rows 0-1, 3-4, 6-7
    #    middle rows taper inward (cols 0-1 only or partial)
    'B': [
        [1, 1, 1, 1, 1, 1, 1, 0],  # row 0 — top of upper bump
        [1, 1, 1, 1, 1, 1, 1, 1],  # row 1 — widest top
        [1, 1, 0, 0, 0, 1, 1, 0],  # row 2 — upper taper
        [1, 1, 1, 1, 1, 1, 1, 1],  # row 3 — mid bar (widest mid)
        [1, 1, 1, 1, 1, 1, 1, 1],  # row 4 — mid bar
        [1, 1, 0, 0, 0, 1, 1, 0],  # row 5 — lower taper
        [1, 1, 1, 1, 1, 1, 1, 1],  # row 6 — widest bottom
        [1, 1, 1, 1, 1, 1, 1, 0],  # row 7 — base of lower bump
    ],
    # M: outer columns always on; inner V peaks at centre
    'M': [
        [1, 1, 0, 0, 0, 0, 1, 1],  # row 0 — outer cols only
        [1, 1, 1, 0, 0, 1, 1, 1],  # row 1 — slight inward step
        [1, 1, 1, 1, 1, 1, 1, 1],  # row 2 — full bar (V peak reaches here)
        [1, 1, 0, 1, 1, 0, 1, 1],  # row 3 — V descends
        [1, 1, 0, 0, 0, 0, 1, 1],  # row 4 — outer cols + narrow centre gap
        [1, 1, 0, 0, 0, 0, 1, 1],  # row 5 — outer cols only
        [1, 1, 0, 0, 0, 0, 1, 1],  # row 6 — outer cols only
        [1, 1, 0, 0, 0, 0, 1, 1],  # row 7 — outer cols only
    ],
}

# Full logo sprite: I + gap + B + gap + M
# 8 cols per letter, 2 cols gap = 8+2+8+2+8 = 28 columns wide
LOGO_LETTER_WIDTH = 8
LOGO_GAP_WIDTH = 2
LOGO_WIDTH = LOGO_LETTER_WIDTH * 3 + LOGO_GAP_WIDTH * 2  # 28


def build_logo_sprite():
    """
    Build the full IBM logo as a 2D pixel array [row][col].
    Returns a list of 8 rows, each LOGO_WIDTH columns wide.
    """
    sprite = [[0] * LOGO_WIDTH for _ in range(MATRIX_HEIGHT)]
    letters = ['I', 'B', 'M']

    for letter_num, letter in enumerate(letters):
        x_start = letter_num * (LOGO_LETTER_WIDTH + LOGO_GAP_WIDTH)
        for row_idx in range(MATRIX_HEIGHT):
            for col_idx in range(LOGO_LETTER_WIDTH):
                sprite[row_idx][x_start + col_idx] = IBM_LOGO[letter][row_idx][col_idx]

    return sprite


class LEDMatrix:
    """8x32 LED matrix with column-major zigzag wiring"""

    def __init__(self, width=MATRIX_WIDTH, height=MATRIX_HEIGHT,
                 pin=DEFAULT_LED_PIN, brightness=DEFAULT_BRIGHTNESS):
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
        except Exception as e:
            print(f"✗ Error initializing LED matrix: {e}")
            sys.exit(1)

    def xy_to_index(self, x, y):
        """
        Column-major zigzag wiring (confirmed by hardware test):
        - Even columns: top to bottom
        - Odd columns:  bottom to top
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        if x % 2 == 0:
            return x * self.height + y
        else:
            return x * self.height + (self.height - 1 - y)

    def set_pixel(self, x, y, color):
        index = self.xy_to_index(x, y)
        if index is not None:
            self.pixels[index] = color

    def clear(self):
        self.pixels.fill(BLACK_COLOR)
        self.pixels.show()

    def clear_buffer(self):
        self.pixels.fill(BLACK_COLOR)

    def show(self):
        self.pixels.show()

    def render_sprite_at(self, sprite, x_offset, color=IBM_BLUE):
        """
        Render a 2D sprite [[row][col]] at the given x_offset.

        Args:
            sprite:   list of rows, each row a list of 0/1 values
            x_offset: leftmost column of the sprite on the matrix
            color:    RGB tuple for lit pixels
        """
        self.clear_buffer()
        for row_idx, row in enumerate(sprite):
            for col_idx, pixel in enumerate(row):
                x_pos = x_offset + col_idx
                if pixel == 1 and 0 <= x_pos < self.width:
                    self.set_pixel(x_pos, row_idx, color)
        self.show()


def scroll_logo(matrix, sprite, scroll_speed=DEFAULT_SCROLL_SPEED, loops=None, color=IBM_BLUE):
    """
    Scroll the IBM logo sprite across the matrix.

    Args:
        matrix:       LEDMatrix instance
        sprite:       2D pixel array from build_logo_sprite()
        scroll_speed: seconds between scroll steps
        loops:        number of passes (None = infinite)
    """
    sprite_width = len(sprite[0])
    loop_count = 0

    try:
        while True:
            for x_offset in range(matrix.width, -sprite_width - 1, -1):
                matrix.render_sprite_at(sprite, x_offset, color)
                time.sleep(scroll_speed)

            loop_count += 1
            if loops is not None and loop_count >= loops:
                break

    except KeyboardInterrupt:
        print("\n⚠ Scrolling interrupted by user")
        matrix.clear()


def main():
    parser = argparse.ArgumentParser(
        description='Scroll the IBM 8-bar logo across an 8x32 WS2812B LED matrix',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ibm_logo.py                  # Scroll IBM logo continuously
  python ibm_logo.py -l 3             # Scroll 3 times then stop
  python ibm_logo.py -s 0.03          # Faster scroll
  python ibm_logo.py -b 0.4           # Brighter
  python ibm_logo.py --static         # Show logo static at centre for 5s
        """
    )

    parser.add_argument('-b', '--brightness', type=float, default=DEFAULT_BRIGHTNESS,
                        help=f'Brightness 0.0-1.0 (default: {DEFAULT_BRIGHTNESS})')
    parser.add_argument('-s', '--speed', type=float, default=DEFAULT_SCROLL_SPEED,
                        help=f'Scroll speed seconds/step (default: {DEFAULT_SCROLL_SPEED})')
    parser.add_argument('-l', '--loops', type=int, default=None,
                        help='Number of scroll passes (default: infinite)')
    parser.add_argument('--static', action='store_true',
                        help='Display the logo statically centred on screen for 10 seconds')

    args = parser.parse_args()

    if not 0.0 <= args.brightness <= 1.0:
        print("Error: Brightness must be between 0.0 and 1.0")
        sys.exit(1)

    matrix = LEDMatrix(brightness=args.brightness)
    sprite = build_logo_sprite()

    if args.static:
        # Centre the 28-wide logo on the 32-wide matrix
        x_offset = (matrix.width - LOGO_WIDTH) // 2  # = 2
        print(f"→ Displaying IBM logo statically for 10 seconds (x_offset={x_offset})...")
        matrix.render_sprite_at(sprite, x_offset)
        time.sleep(10)
        matrix.clear()
        print("✓ Done")
        return

    print(f"\n{'='*50}")
    print("IBM 8-Bar Logo Scroller")
    print(f"Speed: {args.speed}s/step  Brightness: {args.brightness}")
    print(f"Loops: {args.loops or 'infinite'}")
    print(f"{'='*50}\n")
    print("Press Ctrl+C to stop\n")

    try:
        scroll_logo(matrix, sprite, args.speed, args.loops)
        print("\n✓ Scroll complete")
    finally:
        matrix.clear()
        print("✓ Display cleared")


if __name__ == "__main__":
    main()

# Made with Bob
