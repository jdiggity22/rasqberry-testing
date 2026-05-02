# Raspberry Pi 5 WS2812B LED Testing Project

A comprehensive Python project for testing and controlling WS2812B (NeoPixel) LED strips and matrices on Raspberry Pi 5.

## 🎯 Features

- **Multiple Test Patterns**: Individual LED testing, color cycling, rainbow effects, chase patterns, and brightness testing
- **Scrolling Text Display**: NEW! Scroll text across 8x32 LED matrix (see `scroll_think.py`)
- **Configurable Settings**: Easy-to-modify configuration file for LED count, GPIO pins, and brightness
- **Command-Line Interface**: Run specific tests or all tests with customizable parameters
- **Well-Documented Code**: Clear comments and type hints throughout
- **Safe Defaults**: Conservative brightness and power settings to protect hardware

## 📂 Programs Included

1. **main.py** - LED strip testing program with various patterns
2. **scroll_think.py** - Scrolling text display for 8x32 LED matrix (scrolls "THINK" in BLUE)

## 📋 Hardware Requirements

- Raspberry Pi 5
- WS2812B LED strip (NeoPixel compatible)
- External 5V power supply (recommended for >5 LEDs)
- 300-500Ω resistor (for data line protection)
- 1000µF capacitor (for power supply smoothing)
- Jumper wires

## 🔌 Wiring Diagram

```
Raspberry Pi 5          WS2812B LED Strip
┌─────────────┐         ┌──────────────┐
│             │         │              │
│  GPIO 18 ───┼────[R]──┤ DIN (Data)   │
│  (Pin 12)   │  330Ω   │              │
│             │         │              │
│  GND ───────┼─────────┤ GND          │
│             │    │    │              │
└─────────────┘    │    └──────────────┘
                   │
              ┌────┴────┐
              │ 5V PSU  │
              │  [C]    │  [C] = 1000µF capacitor
              │  ├──────┤ 5V+ to LED strip
              │  └──────┤ GND (common ground)
              └─────────┘
```

**Important Notes:**
- Always use a common ground between Raspberry Pi and power supply
- For strips with >5 LEDs, use an external 5V power supply
- Add a resistor between GPIO and LED data line
- Add a capacitor across the power supply terminals

## 🚀 Installation

### 1. System Prerequisites

Update your Raspberry Pi 5 system:

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

Install required system packages:

```bash
sudo apt-get install -y python3-pip python3-dev python3-venv git
```

### 2. Enable SPI (Optional, for SPI mode)

If you plan to use SPI mode instead of PWM:

```bash
sudo raspi-config
# Navigate to: Interface Options -> SPI -> Enable
```

### 3. Clone or Download Project

```bash
cd ~
git clone <your-repo-url> rasqberry-testing
cd rasqberry-testing
```

Or if you already have the files:

```bash
cd ~/rasqberry-testing
```

### 4. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Configure Your Setup

Edit `config.py` to match your hardware:

```bash
nano config.py
```

Key settings to modify:
- `LED_COUNT`: Number of LEDs in your strip
- `LED_PIN`: GPIO pin connected to data line (default: GPIO 18)
- `BRIGHTNESS`: Initial brightness (0.0 to 1.0)

## 🎮 Usage

### Basic Usage

Run all tests with default settings:

```bash
sudo python3 main.py
```

**Note:** `sudo` is required for GPIO access on Raspberry Pi.

### Command-Line Options

```bash
# Test with 16 LEDs
sudo python3 main.py -n 16

# Set brightness to 30%
sudo python3 main.py -b 0.3

# Run only the rainbow test
sudo python3 main.py --test rainbow

# Combine options
sudo python3 main.py -n 24 -b 0.5 --test colors
```

### Available Tests

- `individual` - Test each LED one at a time
- `colors` - Cycle through primary colors
- `rainbow` - Display rainbow animation
- `chase` - Chase pattern along the strip
- `brightness` - Test different brightness levels
- `all` - Run all tests (default)

### Help

```bash
python3 main.py --help
```

## 🎬 Scrolling Text Display (NEW!)

To scroll "THINK" in BLUE across an 8x32 LED matrix:

```bash
# Basic usage (scrolls continuously)
sudo python3 scroll_think.py

# Scroll 5 times then stop
sudo python3 scroll_think.py -l 5

# Adjust speed and brightness
sudo python3 scroll_think.py -s 0.03 -b 0.4

# Custom text
sudo python3 scroll_think.py -t "HELLO"
```

**See [SCROLL_THINK_README.md](SCROLL_THINK_README.md) for complete documentation.**

## 📁 Project Structure

```
rasqberry-testing/
├── main.py                  # Main test program with LED patterns
├── scroll_think.py          # Scrolling text display for 8x32 matrix
├── config.py                # Configuration file for LED settings
├── remoteexec.py            # Remote execution script
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── SCROLL_THINK_README.md   # Scrolling text documentation
```

## 🔧 Configuration Options

### config.py Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `LED_COUNT` | Number of LEDs | 8 |
| `LED_PIN` | GPIO pin for data | board.D18 |
| `BRIGHTNESS` | LED brightness (0.0-1.0) | 0.5 |
| `PIXEL_ORDER` | Color order (GRB/RGB) | "GRB" |
| `AUTO_WRITE` | Auto-update LEDs | False |

### Power Calculations

The configuration file automatically calculates estimated power requirements:

- **Per LED**: ~60mA at full white
- **Total Current**: LED_COUNT × 60mA
- **Recommended PSU**: Total current × 1.2 (20% safety margin)

Example for 8 LEDs:
- Max current: 8 × 60mA = 480mA (0.48A)
- Recommended PSU: 0.58A or higher (use 1A supply)

## 🐛 Troubleshooting

### LEDs Don't Light Up

1. **Check wiring**: Verify all connections, especially ground
2. **Check power**: Ensure external power supply is connected and adequate
3. **Check GPIO pin**: Verify you're using the correct pin (default: GPIO 18)
4. **Run with sudo**: GPIO access requires root privileges
5. **Check LED strip**: Verify data direction (DIN vs DOUT)

### LEDs Flicker or Show Wrong Colors

1. **Add resistor**: Place 330Ω resistor on data line
2. **Add capacitor**: Place 1000µF capacitor across power supply
3. **Shorten wires**: Keep data wire under 1 meter
4. **Check pixel order**: Try changing `PIXEL_ORDER` in config.py (GRB vs RGB)
5. **Check power supply**: Ensure adequate current capacity

### Import Errors

```bash
# Reinstall dependencies
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Permission Denied

```bash
# Always use sudo for GPIO access
sudo python3 main.py
```

### SPI Not Available

```bash
# Enable SPI interface
sudo raspi-config
# Interface Options -> SPI -> Enable
sudo reboot
```

## 📚 Additional Resources

- [Adafruit NeoPixel Guide](https://learn.adafruit.com/adafruit-neopixel-uberguide)
- [WS2812B Datasheet](https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf)
- [Raspberry Pi GPIO Pinout](https://pinout.xyz/)
- [CircuitPython on Raspberry Pi](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux)

## 🔒 Safety Notes

1. **Never connect LED strip 5V directly to Raspberry Pi 5V pin** - Use external power supply
2. **Always use common ground** between Raspberry Pi and power supply
3. **Start with low brightness** to avoid excessive current draw
4. **Add protective components** (resistor and capacitor) as shown in wiring diagram
5. **Monitor temperature** of power supply and Raspberry Pi during operation

## 📝 License

This project is provided as-is for educational and testing purposes.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📧 Support

For issues specific to:
- **Hardware wiring**: Check the wiring diagram above
- **Software errors**: Review the troubleshooting section
- **Library issues**: Consult Adafruit CircuitPython documentation

---

**Happy LED Testing! 🌈✨**