#!/usr/bin/env python3
"""
Weather Scrolling Display for 8x32 WS2812B LED Matrix
Displays 8x8 weather icon followed by scrolling temperature and condition text
"""

import time
import board
import neopixel
import requests
import argparse
import sys
from datetime import datetime

# Configuration for 8x32 LED Matrix
MATRIX_WIDTH = 32
MATRIX_HEIGHT = 8
ICON_SIZE = 8
TOTAL_LEDS = MATRIX_WIDTH * MATRIX_HEIGHT
DEFAULT_LED_PIN = board.D18
DEFAULT_BRIGHTNESS = 0.3
DEFAULT_SCROLL_SPEED = 0.05
MINNEAPOLIS_LAT = 44.9778
MINNEAPOLIS_LON = -93.2650

# Colors
BLACK_COLOR = (0, 0, 0)
BLUE_COLOR = (0, 100, 255)
TEMP_COLOR = (255, 100, 0)  # Orange for temperature

# 8x6 Font for numbers and letters
FONT_8x6 = {
    '0': [
        [0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 0],
    ],
    '1': [
        [0, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1],
    ],
    '2': [
        [0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1],
    ],
    '3': [
        [0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 1, 1],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 0],
    ],
    '4': [
        [0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 0],
        [1, 1, 0, 1, 1, 0],
        [1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 1, 0],
    ],
    '5': [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 0],
    ],
    '6': [
        [0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 0],
    ],
    '7': [
        [1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
    ],
    '8': [
        [0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 0],
    ],
    '9': [
        [0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 0],
    ],
    'F': [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
    ],
    'C': [
        [0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 0],
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
    '-': [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ],
    '.': [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
    ],
    'O': [
        [0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [0, 1, 1, 1, 1, 0],
    ],
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
    'E': [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1],
    ],
    'M': [
        [1, 1, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
    ],
    'P': [
        [1, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
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
    'W': [
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
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
    'D': [
        [1, 1, 1, 1, 0, 0],
        [1, 1, 0, 1, 1, 0],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 1, 1, 0],
        [1, 1, 1, 1, 0, 0],
    ],
    '%': [
        [1, 1, 0, 0, 0, 1],
        [1, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [1, 1, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0],
    ],
}

# Import weather icon functions from weather_matrix
from weather_matrix import (
    create_clear_day_icon, create_clear_night_icon, create_clouds_icon,
    create_rain_icon, create_thunderstorm_icon, create_snow_icon,
    create_mist_icon, create_error_icon
)

WEATHER_ICONS = {
    'clear_day': create_clear_day_icon,
    'clear_night': create_clear_night_icon,
    'clouds': create_clouds_icon,
    'rain': create_rain_icon,
    'thunderstorm': create_thunderstorm_icon,
    'snow': create_snow_icon,
    'mist': create_mist_icon,
    'error': create_error_icon,
}


class WeatherScrollDisplay:
    """Class to handle weather scrolling display on 8x32 LED matrix"""
    
    def __init__(self, api_key, width=MATRIX_WIDTH, height=MATRIX_HEIGHT,
                 pin=DEFAULT_LED_PIN, brightness=DEFAULT_BRIGHTNESS):
        """Initialize the weather scroll display"""
        self.api_key = api_key
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
        """Convert x,y coordinates to LED strip index (column-major zigzag)"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        
        if x % 2 == 0:
            index = x * self.height + y
        else:
            index = x * self.height + (self.height - 1 - y)
        
        return index
    
    def set_pixel(self, x, y, color):
        """Set a single pixel color"""
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
    
    def render_icon_at_position(self, icon_pattern, x_offset):
        """Render 8x8 weather icon at specific x position"""
        for y in range(ICON_SIZE):
            for x in range(ICON_SIZE):
                x_pos = x_offset + x
                if 0 <= x_pos < self.width:
                    color = icon_pattern[y][x]
                    self.set_pixel(x_pos, y, color)
    
    def render_text_at_position(self, text, x_offset, color=BLUE_COLOR):
        """Render text at specific x position"""
        current_x = x_offset
        
        for char in text.upper():
            if char in FONT_8x6:
                letter = FONT_8x6[char]
                
                for row_idx, row in enumerate(letter):
                    for col_idx, pixel in enumerate(row):
                        x_pos = current_x + col_idx
                        
                        if pixel == 1 and 0 <= x_pos < self.width:
                            self.set_pixel(x_pos, row_idx, color)
                
                current_x += 7  # 6 pixels + 1 spacing
        
        return current_x
    
    def get_weather_data(self, lat=MINNEAPOLIS_LAT, lon=MINNEAPOLIS_LON):
        """Fetch weather data from OpenWeatherMap API"""
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'imperial'
        }
        
        try:
            print(f"→ Fetching weather data...")
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            weather_info = {
                'condition': data['weather'][0]['main'].lower(),
                'description': data['weather'][0]['description'],
                'temp': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'icon_code': data['weather'][0]['icon'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"✓ Weather: {weather_info['description']}, {weather_info['temp']:.0f}°F")
            return weather_info
            
        except Exception as e:
            print(f"✗ Error fetching weather data: {e}")
            return None
    
    def map_weather_to_icon(self, weather_data):
        """Map weather condition to icon key"""
        if not weather_data:
            return 'error'
        
        condition = weather_data['condition']
        icon_code = weather_data.get('icon_code', '')
        is_day = 'd' in icon_code
        
        if condition == 'clear':
            return 'clear_day' if is_day else 'clear_night'
        elif condition == 'clouds':
            return 'clouds'
        elif condition == 'rain' or condition == 'drizzle':
            return 'rain'
        elif condition == 'thunderstorm':
            return 'thunderstorm'
        elif condition == 'snow':
            return 'snow'
        elif condition in ['mist', 'fog', 'haze', 'smoke']:
            return 'mist'
        else:
            return 'clouds'
    
    def scroll_weather(self, scroll_speed=DEFAULT_SCROLL_SPEED, loops=None):
        """Scroll weather icon and comprehensive data across the display"""
        weather_data = self.get_weather_data()
        
        if not weather_data:
            print("✗ Failed to get weather data")
            return
        
        # Get icon
        icon_key = self.map_weather_to_icon(weather_data)
        icon_pattern = WEATHER_ICONS[icon_key]()
        
        # Format comprehensive weather text
        temp = int(weather_data['temp'])
        feels = int(weather_data['feels_like'])
        humidity = int(weather_data['humidity'])
        wind = int(weather_data['wind_speed'])
        
        # Build weather string with all data
        weather_text = (
            f" {temp}F "
            f" FEELS {feels}F "
            f" HUMID {humidity}% "
            f" WIND {wind}MPH "
        )
        
        # Calculate total width: icon (8) + text
        text_width = len(weather_text) * 7
        total_width = ICON_SIZE + text_width
        
        loop_count = 0
        try:
            while True:
                # Scroll from right edge to completely off left edge
                for x_offset in range(self.width, -total_width - 1, -1):
                    self.clear()
                    
                    # Render icon
                    self.render_icon_at_position(icon_pattern, x_offset)
                    
                    # Render weather text after icon
                    text_x = x_offset + ICON_SIZE
                    self.render_text_at_position(weather_text, text_x, BLUE_COLOR)
                    
                    self.show()
                    time.sleep(scroll_speed)
                
                loop_count += 1
                if loops is not None and loop_count >= loops:
                    break
        
        except KeyboardInterrupt:
            print("\n⚠ Scrolling interrupted by user")
            self.clear()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Scroll weather icon and data across 8x32 LED matrix',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python weather_scroll.py -k YOUR_API_KEY              # Scroll continuously
  python weather_scroll.py -k YOUR_API_KEY -l 3         # Scroll 3 times
  python weather_scroll.py -k YOUR_API_KEY -s 0.08      # Slower scrolling
  python weather_scroll.py -k YOUR_API_KEY -b 0.5       # Brighter display

Get a free API key at: https://openweathermap.org/api
        """
    )
    
    parser.add_argument('-k', '--api-key', required=True,
                       help='OpenWeatherMap API key (required)')
    parser.add_argument('-b', '--brightness', type=float, default=DEFAULT_BRIGHTNESS,
                       help=f'Brightness level 0.0-1.0 (default: {DEFAULT_BRIGHTNESS})')
    parser.add_argument('-s', '--speed', type=float, default=DEFAULT_SCROLL_SPEED,
                       help=f'Scroll speed in seconds per step (default: {DEFAULT_SCROLL_SPEED})')
    parser.add_argument('-l', '--loops', type=int, default=None,
                       help='Number of times to loop (default: infinite)')
    
    args = parser.parse_args()
    
    # Validate brightness
    if not 0.0 <= args.brightness <= 1.0:
        print("Error: Brightness must be between 0.0 and 1.0")
        sys.exit(1)
    
    # Initialize display
    display = WeatherScrollDisplay(
        api_key=args.api_key,
        brightness=args.brightness
    )
    
    print(f"\n{'='*50}")
    print("WEATHER SCROLLING DISPLAY")
    print(f"Speed: {args.speed}s per step")
    print(f"Loops: {args.loops or 'infinite'}")
    print(f"{'='*50}\n")
    print("Press Ctrl+C to stop\n")
    
    try:
        display.scroll_weather(args.speed, args.loops)
        print("\n✓ Scrolling complete")
    finally:
        display.clear()
        print("✓ Display cleared")


if __name__ == "__main__":
    main()

# Made with Bob