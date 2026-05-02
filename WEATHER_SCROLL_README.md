# Weather Scrolling Display

Scrolls weather icon and temperature data across an 8x32 WS2812B LED matrix display for Minneapolis, Minnesota.

## 🎯 Features

- **8x8 Weather Icon** - Full-color weather condition icon
- **8-Pixel High Temperature** - Large, readable temperature display in orange
- **Smooth Scrolling** - Icon and text scroll together from right to left
- **Real-Time Weather** - Fetches current conditions from OpenWeatherMap API
- **Configurable** - Adjustable scroll speed, brightness, and loop count

## 📋 Display Format

The display shows:
1. **Weather Icon** (8x8 pixels) - Sun, moon, clouds, rain, snow, etc.
2. **Temperature** (8-pixel high text) - Current temperature in Fahrenheit

Example: `[☀️ ICON] 72F` scrolls across the display

## 🌤️ Weather Icons

The program displays different 8x8 icons based on conditions:
- **Clear Day** - Bright sun with rays
- **Clear Night** - Crescent moon with stars
- **Clouds** - Fluffy gray clouds
- **Rain** - Blue raindrops falling
- **Thunderstorm** - Lightning bolt with dark clouds
- **Snow** - White snowflakes
- **Mist/Fog** - Gray fog bands

## 📋 Hardware Requirements

- Raspberry Pi 5
- 8x32 WS2812B LED Matrix (256 LEDs total)
- External 5V power supply (recommended: 15A or higher)
- 300-500Ω resistor (for data line protection)
- 1000µF capacitor (for power supply smoothing)

## 🔌 LED Matrix Wiring

The program uses **column-major zigzag** wiring pattern (typical for pre-made panels):

```
Column 0: LED 0 → 1 → 2 → ... → 7 (top to bottom)
Column 1: LED 15 ← 14 ← 13 ← ... ← 8 (bottom to top)
Column 2: LED 16 → 17 → 18 → ... → 23 (top to bottom)
...and so on
```

Connect:
- LED Matrix Data IN → 330Ω resistor → GPIO 18 (Pin 12)
- LED Matrix GND → Raspberry Pi GND + Power Supply GND (common ground)
- LED Matrix 5V → External 5V Power Supply

## 🚀 Usage

### Get API Key

1. Sign up for a free account at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your API key from the dashboard
3. Free tier allows 60 calls/minute, 1,000,000 calls/month

### Basic Usage (Continuous Scrolling)

```bash
python weather_scroll.py -k YOUR_API_KEY
```

This will continuously scroll the weather icon and temperature until you press Ctrl+C.

### Scroll a Specific Number of Times

```bash
python weather_scroll.py -k YOUR_API_KEY -l 3
```

Scrolls the weather data 3 times then stops.

### Adjust Scroll Speed

```bash
# Slower scrolling (0.08 seconds per step)
python weather_scroll.py -k YOUR_API_KEY -s 0.08

# Faster scrolling (0.03 seconds per step)
python weather_scroll.py -k YOUR_API_KEY -s 0.03
```

### Adjust Brightness

```bash
# Dimmer (30% brightness)
python weather_scroll.py -k YOUR_API_KEY -b 0.3

# Brighter (70% brightness)
python weather_scroll.py -k YOUR_API_KEY -b 0.7
```

### Combined Options

```bash
# Scroll 5 times at 50% brightness with slower speed
python weather_scroll.py -k YOUR_API_KEY -l 5 -b 0.5 -s 0.08
```

## 📝 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-k, --api-key` | OpenWeatherMap API key | Required |
| `-s, --speed` | Scroll speed (seconds per step) | 0.05 |
| `-l, --loops` | Number of times to loop | Infinite |
| `-b, --brightness` | LED brightness (0.0-1.0) | 0.3 |

## 🎨 Display Details

### Weather Icon
- **Size**: 8x8 pixels
- **Position**: Scrolls from right to left
- **Colors**: Full RGB colors matching weather conditions

### Temperature Text
- **Font Size**: 8 pixels high × 6 pixels wide per character
- **Color**: Orange (255, 100, 0)
- **Format**: `##F` (e.g., "72F", "-5F")
- **Spacing**: 1 pixel between characters

### Scrolling Behavior
- Starts from right edge of display
- Icon appears first, followed by temperature
- Scrolls completely off the left edge
- Loops continuously or for specified count

## 🔧 Technical Details

### Weather Data Source
- **API**: OpenWeatherMap Current Weather API
- **Location**: Minneapolis, MN (44.9778, -93.2650)
- **Units**: Imperial (Fahrenheit)
- **Update**: Fetches fresh data at start of each loop

### Font Support
The 8x6 font includes:
- **Numbers**: 0-9
- **Letters**: F, C, O (for temperature units)
- **Symbols**: Space, dash, period

### Color Scheme
- **Weather Icons**: Condition-specific colors
- **Temperature**: Orange (255, 100, 0)
- **Background**: Black (0, 0, 0)

## 📊 Example Output

```
✓ Initialized 32x8 LED matrix (256 LEDs)
→ Fetching weather data...
✓ Weather: clear sky, 72°F

==================================================
WEATHER SCROLLING DISPLAY
Speed: 0.05s per step
Loops: infinite
==================================================

Press Ctrl+C to stop
```

## 🔄 Integration with Other Programs

This program combines features from:
- `weather_matrix.py` - Weather icons and API integration
- `scroll_think.py` - Scrolling text functionality

You can modify it to:
- Add more weather details (humidity, wind speed)
- Change text color based on temperature
- Display multiple weather metrics
- Add time/date information

## 🐛 Troubleshooting

### Weather data not fetching
- Check your API key is valid
- Ensure internet connection is working
- Verify API rate limits haven't been exceeded

### Display looks wrong
- Confirm your matrix uses column-major zigzag wiring
- Check power supply is adequate
- Verify GPIO pin connection (default: GPIO 18)

### Scrolling too fast/slow
- Adjust with `-s` parameter
- Try values between 0.02 (fast) and 0.1 (slow)

## 📄 License

Made with Bob

## 🔗 Related Programs

- `weather_matrix.py` - Static weather icon display
- `scroll_think.py` - Scrolling text display
- `weather_display.py` - Simple weather display for LED strip