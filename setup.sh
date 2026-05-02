#!/bin/bash
# Setup script for Raspberry Pi 5 WS2812B LED Testing Project

set -e  # Exit on error

echo "=========================================="
echo "Raspberry Pi 5 WS2812B LED Setup"
echo "=========================================="
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "⚠️  Warning: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Installing Python 3..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-dev python3-venv
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Update system packages
echo "→ Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install system dependencies
echo ""
echo "→ Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    build-essential

echo "✓ System dependencies installed"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "→ Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment and install Python packages
echo "→ Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Python dependencies installed"
echo ""

# Make main.py executable
chmod +x main.py
echo "✓ Made main.py executable"
echo ""

# Check if SPI is enabled
echo "→ Checking SPI status..."
if lsmod | grep -q spi_bcm2835; then
    echo "✓ SPI is enabled"
else
    echo "⚠️  SPI is not enabled"
    echo "   To enable SPI, run: sudo raspi-config"
    echo "   Navigate to: Interface Options -> SPI -> Enable"
fi
echo ""

# Display configuration info
echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Connect your WS2812B LED strip according to the wiring diagram in README.md"
echo "2. Edit config.py to match your LED count and GPIO pin"
echo "3. Activate the virtual environment: source venv/bin/activate"
echo "4. Run the test program: sudo python3 main.py"
echo ""
echo "For detailed instructions, see README.md"
echo ""
echo "⚠️  Important Safety Notes:"
echo "   - Use an external 5V power supply for >5 LEDs"
echo "   - Add a 330Ω resistor on the data line"
echo "   - Add a 1000µF capacitor across power supply"
echo "   - Always use common ground"
echo ""
echo "Happy LED testing! 🌈✨"
echo ""

# Made with Bob
