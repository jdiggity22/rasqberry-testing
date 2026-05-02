# Scrolling Text Display - "THINK" in BLUE

This program scrolls the word "THINK" in BLUE across an 8x32 WS2812B LED matrix display.

## 🎯 Features

- Scrolls "THINK" in blue color across the LED matrix
- Configurable scroll speed and brightness
- Support for custom text (using available font characters)
- Smooth scrolling animation
- Can run continuously or for a specific number of loops

## 📋 Hardware Requirements

- Raspberry Pi 5
- 8x32 WS2812B LED Matrix (256 LEDs total)
- External 5V power supply (recommended: 15A or higher for full brightness)
- 300-500Ω resistor (for data line protection)
- 1000µF capacitor (for power supply smoothing)

## 🔌 LED Matrix Wiring

The program assumes a **serpentine (zigzag) wiring pattern**:

```
Row 0: LED 0 → 1 → 2 → ... → 31 (left to right)
Row 1: LED 63 ← 62 ← 61 ← ... ← 32 (right to left)
Row 2: LED 64 → 65 → 66 → ... → 95 (left to right)
Row 3: LED 127 ← 126 ← 125 ← ... ← 96 (right to left)
...and so on
```

Connect:
- LED Matrix Data IN → 330Ω resistor → GPIO 18 (Pin 12)
- LED Matrix GND → Raspberry Pi GND + Power Supply GND (common ground)
- LED Matrix 5V → External 5V Power Supply

## 🚀 Usage

### Basic Usage

Run with default settings (scrolls "THINK" continuously):

```bash
sudo python3 scroll_think.py
```

### Command-Line Options

```bash
# Scroll 5 times then stop
sudo python3 scroll_think.py -l 5

# Faster scrolling (0.03 seconds per frame)
sudo python3 scroll_think.py -s 0.03

# Slower scrolling (0.1 seconds per frame)
sudo python3 scroll_think.py -s 0.1

# Brighter display (50% brightness)
sudo python3 scroll_think.py -b 0.5

# Scroll different text
sudo python3 scroll_think.py -t "HELLO"

# Combine options
sudo python3 scroll_think.py -t "THINK" -s 0.04 -b 0.4 -l 10
```

### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `-b, --brightness` | Brightness level (0.0-1.0) | 0.3 |
| `-s, --speed` | Scroll speed (seconds per frame) | 0.05 |
| `-l, --loops` | Number of times to loop | infinite |
| `-t, --text` | Text to scroll | THINK |
| `--width` | Matrix width in pixels | 32 |
| `--height` | Matrix height in pixels | 8 |

### Supported Characters

The program includes a 5x7 pixel font for the following characters:
- **T, H, I, N, K** (for "THINK")
- **Space** (for word separation)

To add more characters, edit the `FONT` dictionary in `scroll_think.py`.

## 🎨 Color Customization

To change the color from BLUE to another color, edit the `BLUE_COLOR` constant in `scroll_think.py`:

```python
# Current (BLUE)
BLUE_COLOR = (0, 0, 255)

# Examples of other colors:
# RED
BLUE_COLOR = (255, 0, 0)

# GREEN
BLUE_COLOR = (0, 255, 0)

# CYAN
BLUE_COLOR = (0, 255, 255)

# PURPLE
BLUE_COLOR = (128, 0, 128)

# WHITE
BLUE_COLOR = (255, 255, 255)
```

## ⚡ Power Considerations

**Important:** An 8x32 matrix has 256 LEDs!

- **Maximum current**: 256 LEDs × 60mA = 15.36A at full white
- **With BLUE only**: ~5A at full brightness (only blue channel active)
- **At 30% brightness**: ~1.5A for blue text

**Recommendations:**
1. Use a 5V power supply rated for at least 5A (for blue at 30% brightness)
2. For full brightness or white colors, use a 15A+ power supply
3. Start with low brightness (0.2-0.3) and increase gradually
4. Monitor power supply temperature during operation

## 🔧 Troubleshooting

### Text doesn't appear correctly

1. **Check matrix wiring pattern**: The code assumes serpentine wiring. If your matrix uses a different pattern, modify the `xy_to_index()` method.
2. **Verify dimensions**: Ensure your matrix is actually 8x32. Use `--width` and `--height` options if different.

### Text is upside down or mirrored

Modify the `xy_to_index()` method in `scroll_think.py` to match your matrix orientation.

### Colors are wrong

Check the `pixel_order` parameter in the `LEDMatrix.__init__()` method. Try changing from `neopixel.GRB` to `neopixel.RGB`.

### LEDs flicker or are dim

1. Ensure adequate power supply
2. Add capacitor across power supply terminals
3. Check all ground connections
4. Increase brightness with `-b` option

## 📝 Examples

### Quick Demo (3 loops)
```bash
sudo python3 scroll_think.py -l 3
```

### Slow, Bright Display
```bash
sudo python3 scroll_think.py -s 0.1 -b 0.5
```

### Fast Scrolling Message
```bash
sudo python3 scroll_think.py -t "THINK" -s 0.03 -l 20
```

### Continuous Display (Press Ctrl+C to stop)
```bash
sudo python3 scroll_think.py
```

## 🛑 Stopping the Program

Press `Ctrl+C` to stop the scrolling. The program will automatically clear the display before exiting.

## 🔒 Safety Notes

1. **Always use an external power supply** - Never power 256 LEDs from the Raspberry Pi
2. **Start with low brightness** (0.2-0.3) to avoid overloading your power supply
3. **Monitor temperature** of power supply during operation
4. **Use common ground** between Raspberry Pi and power supply
5. **Add protective components** (resistor and capacitor)

## 📚 Technical Details

### Font Format

Each character is defined as a 5×8 pixel array:
- Width: 5 pixels
- Height: 8 pixels (fills the full matrix height)
- Spacing: 1 pixel between characters

### Scrolling Algorithm

1. Text starts off-screen to the right
2. Moves left one pixel per frame
3. Continues until completely off-screen to the left
4. Repeats for specified number of loops

### Frame Rate

- Default: 20 FPS (0.05 seconds per frame)
- Adjustable with `-s` option
- Faster speeds may cause flickering on some matrices

---

**Made with Bob** 🤖