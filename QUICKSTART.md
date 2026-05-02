# Quick Start Guide

Get your WS2812B LED strip running in 5 minutes!

## 🔌 Hardware Setup

1. **Connect the LED strip:**
   ```
   LED Strip          Raspberry Pi 5
   ---------          --------------
   DIN (Data)  -----> GPIO 18 (Pin 12) [with 330Ω resistor]
   GND         -----> GND (Pin 6 or 9)
   5V          -----> External 5V Power Supply
   ```

2. **Important:** Connect power supply GND to Raspberry Pi GND (common ground)

## 💻 Software Setup

### Option 1: Automated Setup (Recommended)

```bash
cd ~/rasqberry-testing
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

## 🎮 Run Your First Test

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run the test program
sudo python3 main.py
```

You should see your LEDs light up with various patterns!

## ⚙️ Customize Settings

Edit `config.py` to change:
- Number of LEDs: `LED_COUNT = 8`
- Brightness: `BRIGHTNESS = 0.5`
- GPIO pin: `LED_PIN = board.D18`

## 🎨 Run Specific Tests

```bash
# Rainbow pattern only
sudo python3 main.py --test rainbow

# Test with 16 LEDs at 30% brightness
sudo python3 main.py -n 16 -b 0.3

# Color test only
sudo python3 main.py --test colors
```

## 🐛 Troubleshooting

**LEDs don't light up?**
- Check all connections
- Verify you're using `sudo`
- Check LED strip direction (DIN vs DOUT)
- Verify power supply is connected

**Wrong colors?**
- Try changing `PIXEL_ORDER` in config.py from "GRB" to "RGB"

**Need more help?**
- See full README.md for detailed troubleshooting
- Check wiring diagram in README.md

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed information
- Modify test patterns in `main.py`
- Create your own LED animations!

---

**Happy LED Testing! 🌈✨**