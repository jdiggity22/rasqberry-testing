# Weather Display for Minneapolis, Minnesota

Display current weather conditions as colorful icons on your WS2812B LEDs! This project includes two programs:

- **weather_display.py** - For 1D LED strips (8 LEDs in a row)
- **weather_matrix.py** - For 2D LED matrices (8x32 matrix, 256 LEDs) ⭐ **RECOMMENDED**

Both programs fetch real-time weather data from OpenWeatherMap and show beautiful weather icons.

## 🌤️ Features

- **Real-time Weather Data**: Fetches current conditions for Minneapolis, MN
- **Beautiful Weather Icons**: 8 different weather patterns with appropriate colors
- **Day/Night Detection**: Different icons for clear day vs. clear night
- **Smooth Animations**: Optional fade-in effects for weather transitions
- **Continuous Mode**: Auto-updates weather at configurable intervals
- **Detailed Weather Info**: Displays temperature, humidity, wind speed, and more

## 🎨 Weather Icons

### For 8x32 Matrix (weather_matrix.py) - Full Screen Icons

The matrix version displays beautiful full-screen weather icons:

| Weather Condition | Visual Description |
|------------------|-------------------|
| **Clear (Day)** | Bright yellow sun with rays spreading across the display |
| **Clear (Night)** | Crescent moon with twinkling stars on dark blue sky |
| **Clouds** | Fluffy white/gray clouds floating across light blue sky |
| **Rain** | Dark clouds at top with blue raindrops falling diagonally |
| **Thunderstorm** | Dark storm clouds with bright yellow lightning bolt |
| **Snow** | Gray clouds with white snowflakes falling gently |
| **Mist/Fog** | Horizontal bands of gray creating foggy atmosphere |
| **Error** | Red X pattern indicating connection error |

### For LED Strip (weather_display.py) - Color Patterns

The strip version displays color gradients for 8 LEDs:

| Weather Condition | LED Color Pattern | Description |
|------------------|-------------------|-------------|
| **Clear (Day)** | Yellow/Gold | Bright sun colors |
| **Clear (Night)** | Pale Blue | Moonlight colors |
| **Clouds** | Gray/White | Cloudy sky gradient |
| **Rain** | Blue | Raindrop blue shades |
| **Thunderstorm** | Yellow/Gray | Lightning flashes with dark clouds |
| **Snow** | White/Light Blue | Snowflake whites |
| **Mist/Fog** | Light Gray | Misty atmosphere |
| **Error** | Red Flashing | Connection error indicator |

## 📋 Requirements

### Hardware
- Raspberry Pi 5
- WS2812B LED strip (8 or more LEDs)
- External 5V power supply (for >5 LEDs)
- Internet connection for weather API

### Software
- Python 3.7+
- OpenWeatherMap API key (free tier available)

## 🔑 Getting an API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your API key
5. Free tier includes:
   - 1,000 API calls per day
   - Current weather data
   - 3-hour forecast data

## 🚀 Quick Start (For 8x32 Matrix)

### Basic Usage

Display weather once for 10 seconds:

```bash
sudo python3 weather_matrix.py -k YOUR_API_KEY
```

### Continuous Display Mode

Update weather every 10 minutes:

```bash
sudo python3 weather_matrix.py -k YOUR_API_KEY -c
```

Update every 5 minutes:

```bash
sudo python3 weather_matrix.py -k YOUR_API_KEY -c -i 300
```

## 🚀 Installation

### 1. Install Dependencies

```bash
# Activate your virtual environment
source venv/bin/activate

# Install/update requirements
pip install -r requirements.txt
```

The `requirements.txt` now includes the `requests` library needed for API calls.

### 2. Verify Hardware Setup

Make sure your LED strip is properly connected:
- Data pin to GPIO 18 (default)
- Power and ground properly connected
- See main README.md for wiring details

## 🎮 Usage

### For 8x32 Matrix (weather_matrix.py) ⭐ RECOMMENDED

**Basic Usage:**
```bash
# Display once for 10 seconds
sudo python3 weather_matrix.py -k YOUR_API_KEY

# Continuous display, update every 10 minutes
sudo python3 weather_matrix.py -k YOUR_API_KEY -c

# Update every 5 minutes with 50% brightness
sudo python3 weather_matrix.py -k YOUR_API_KEY -c -i 300 -b 0.5
```

### For LED Strip (weather_display.py)

**Basic Usage:**
```bash
# Display once for 10 seconds (8 LEDs)
sudo python3 weather_display.py -k YOUR_API_KEY

# Continuous display with 16 LEDs
sudo python3 weather_display.py -k YOUR_API_KEY -c -n 16

# Custom brightness for nighttime
sudo python3 weather_display.py -k YOUR_API_KEY -c -b 0.2
```

## 📝 Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-k, --api-key` | OpenWeatherMap API key (required) | - |
| `-n, --num-leds` | Number of LEDs in strip | 8 |
| `-b, --brightness` | Brightness level (0.0-1.0) | 0.5 |
| `-c, --continuous` | Enable continuous update mode | False |
| `-i, --interval` | Update interval in seconds | 600 |
| `-d, --duration` | Display duration for single mode | 10.0 |
| `--no-animate` | Disable animation effects | False |

## 📊 Example Output

```
✓ Initialized 8 LEDs on pin board.D18
→ Fetching weather for Minneapolis, MN (44.9778, -93.265)...
✓ Weather data retrieved successfully

==================================================
MINNEAPOLIS WEATHER
==================================================
Condition: Partly Cloudy
Temperature: 72.5°F
Feels Like: 71.8°F
Humidity: 65%
Wind Speed: 8.5 mph
Updated: 2026-05-01 20:24:30
==================================================

→ Displaying weather icon: clouds
```

## 🔄 Continuous Mode

In continuous mode, the program:
1. Fetches current weather data
2. Displays the appropriate weather icon
3. Waits for the specified interval
4. Repeats indefinitely

**Recommended intervals:**
- **5 minutes (300s)**: Frequent updates, uses ~288 API calls/day
- **10 minutes (600s)**: Good balance, uses ~144 API calls/day
- **15 minutes (900s)**: Conservative, uses ~96 API calls/day

**Note:** Free tier allows 1,000 calls/day, so even 1-minute intervals would work, but weather doesn't change that frequently!

## 🎭 Animation Effects

By default, weather icons fade in smoothly over the display duration. This creates a pleasant visual effect when weather changes.

To disable animations (instant display):
```bash
sudo python3 weather_display.py -k YOUR_API_KEY --no-animate
```

## 🛠️ Customization

### Changing Location

Edit the coordinates in `weather_display.py`:

```python
# Default is Minneapolis, MN
MINNEAPOLIS_LAT = 44.9778
MINNEAPOLIS_LON = -93.2650
```

Or modify the `get_weather_data()` call to accept different coordinates.

### Custom Weather Icons

Edit the `WEATHER_ICONS` dictionary in `weather_display.py` to create your own color patterns:

```python
WEATHER_ICONS = {
    'clear_day': [
        (255, 200, 0),   # LED 0: Bright yellow
        (255, 180, 0),   # LED 1: Golden yellow
        # ... customize all 8 LEDs
    ],
}
```

### Adding More LEDs

The program works with any number of LEDs. For strips longer than 8 LEDs, the pattern repeats or you can extend the icon patterns:

```bash
sudo python3 weather_display.py -k YOUR_API_KEY -n 16
```

## 🐛 Troubleshooting

### API Key Issues

**Error: "Invalid API key"**
- Verify your API key is correct
- Check if key is activated (can take a few minutes after signup)
- Ensure no extra spaces in the key

### Network Issues

**Error: "Error fetching weather data"**
- Check internet connection
- Verify firewall isn't blocking API requests
- Try accessing https://api.openweathermap.org in a browser

### LED Issues

**LEDs don't light up:**
- Verify hardware connections (see main README.md)
- Check that you're running with `sudo`
- Test with `main.py` first to verify LED hardware works

### Rate Limiting

**Error: "429 Too Many Requests"**
- You've exceeded API rate limits
- Increase update interval (`-i` parameter)
- Free tier: 1,000 calls/day, 60 calls/minute

## 🔒 Security Notes

1. **Protect Your API Key**: Don't commit API keys to version control
2. **Use Environment Variables**: Consider storing key in environment:
   ```bash
   export WEATHER_API_KEY="your_key_here"
   python3 weather_display.py -k $WEATHER_API_KEY
   ```
3. **Rate Limiting**: Respect API rate limits to avoid account suspension

## 💡 Tips

1. **Start with single display mode** to test before running continuously
2. **Use lower brightness at night** to avoid disturbing sleep
3. **Set reasonable update intervals** - weather doesn't change every minute!
4. **Monitor API usage** in your OpenWeatherMap dashboard
5. **Test without LEDs first** by commenting out LED code to verify API works

## 🔗 Related Files

- `main.py` - LED strip testing program
- `scroll_think.py` - Scrolling text display
- `config.py` - LED configuration settings
- `requirements.txt` - Python dependencies

## 📚 API Documentation

- [OpenWeatherMap Current Weather API](https://openweathermap.org/current)
- [API Response Format](https://openweathermap.org/current#current_JSON)
- [Weather Condition Codes](https://openweathermap.org/weather-conditions)

## 🎯 Future Enhancements

Possible improvements:
- Support for weather forecasts
- Temperature-based color gradients
- Severe weather alerts
- Multiple location support
- Web interface for configuration
- Historical weather tracking

## 📧 Support

For issues:
- **Hardware problems**: See main README.md troubleshooting
- **API issues**: Check OpenWeatherMap documentation
- **LED patterns**: Modify WEATHER_ICONS dictionary

---

**Enjoy your weather display! 🌈⛈️☀️**

Made with Bob