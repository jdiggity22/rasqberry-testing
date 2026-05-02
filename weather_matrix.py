#!/usr/bin/env python3
"""
Weather Icon Display for Minneapolis, Minnesota - 8x32 LED Matrix
Displays current weather conditions as icons on WS2812B LED matrix
Uses OpenWeatherMap API for weather data
"""

import time
import board
import neopixel
import requests
import argparse
import sys
from typing import Tuple, Dict, List
from datetime import datetime

# Configuration for 8x32 LED Matrix
MATRIX_WIDTH = 32
MATRIX_HEIGHT = 8
TOTAL_LEDS = MATRIX_WIDTH * MATRIX_HEIGHT  # 256 LEDs
DEFAULT_LED_PIN = board.D18
DEFAULT_BRIGHTNESS = 0.3
MINNEAPOLIS_LAT = 44.9778
MINNEAPOLIS_LON = -93.2650

# Weather icon patterns for 8x32 matrix
# Each icon is defined as a function that returns colors for the entire matrix
def create_clear_day_icon():
    """Bright sun with rays"""
    icon = []
    for y in range(MATRIX_HEIGHT):
        row = []
        for x in range(MATRIX_WIDTH):
            # Center sun
            dx = x - MATRIX_WIDTH // 2
            dy = y - MATRIX_HEIGHT // 2
            dist = (dx * dx + dy * dy) ** 0.5
            
            if dist < 3:
                # Sun center - bright yellow
                row.append((255, 200, 0))
            elif dist < 4:
                # Sun edge - golden
                row.append((255, 150, 0))
            elif (abs(dx) < 1 and abs(dy) > 3) or (abs(dy) < 1 and abs(dx) > 3):
                # Sun rays (vertical and horizontal)
                row.append((255, 180, 0))
            elif abs(dx - dy) < 1 and abs(dx) > 3:
                # Diagonal rays
                row.append((255, 180, 0))
            elif abs(dx + dy) < 1 and abs(dx) > 3:
                # Other diagonal rays
                row.append((255, 180, 0))
            else:
                # Sky - light blue
                row.append((100, 150, 255))
        icon.append(row)
    return icon

def create_clear_night_icon():
    """Crescent moon with stars"""
    icon = []
    for y in range(MATRIX_HEIGHT):
        row = []
        for x in range(MATRIX_WIDTH):
            # Moon position (left side)
            dx = x - 12
            dy = y - 4
            dist = (dx * dx + dy * dy) ** 0.5
            
            # Shadow position (creates crescent)
            sdx = x - 14
            sdy = y - 4
            sdist = (sdx * sdx + sdy * sdy) ** 0.5
            
            if dist < 2.5 and sdist > 2:
                # Moon crescent - pale yellow
                row.append((200, 200, 150))
            elif (x == 20 and y == 2) or (x == 25 and y == 5) or (x == 22 and y == 6):
                # Stars - white
                row.append((200, 200, 200))
            else:
                # Night sky - dark blue
                row.append((10, 10, 50))
        icon.append(row)
    return icon

def create_clouds_icon():
    """Fluffy clouds"""
    icon = []
    for y in range(MATRIX_HEIGHT):
        row = []
        for x in range(MATRIX_WIDTH):
            # Multiple cloud puffs
            cloud1 = ((x - 10) ** 2 + (y - 3) ** 2) < 12
            cloud2 = ((x - 15) ** 2 + (y - 2) ** 2) < 10
            cloud3 = ((x - 20) ** 2 + (y - 3) ** 2) < 12
            
            if cloud1 or cloud2 or cloud3:
                # Cloud - light gray
                brightness = 200 + (x % 3) * 15
                row.append((brightness, brightness, brightness))
            else:
                # Sky - light blue
                row.append((120, 160, 200))
        icon.append(row)
    return icon

def create_rain_icon():
    """Rain drops falling"""
    icon = []
    for y in range(MATRIX_HEIGHT):
        row = []
        for x in range(MATRIX_WIDTH):
            # Dark clouds at top
            if y < 2:
                row.append((80, 80, 100))
            # Rain drops - diagonal pattern
            elif (x + y * 2) % 4 == 0:
                row.append((0, 100, 255))
            elif (x + y * 2) % 4 == 1:
                row.append((0, 120, 255))
            else:
                # Background - dark blue
                row.append((20, 40, 80))
        icon.append(row)
    return icon

def create_thunderstorm_icon():
    """Lightning bolt with dark clouds"""
    icon = []
    lightning_pattern = [
        (16, 1), (15, 2), (16, 2), (15, 3), (14, 4), (15, 4),
        (16, 4), (17, 5), (16, 6), (17, 6)
    ]
    
    for y in range(MATRIX_HEIGHT):
        row = []
        for x in range(MATRIX_WIDTH):
            # Dark storm clouds
            if y < 3:
                row.append((40, 40, 50))
            # Lightning bolt
            elif (x, y) in lightning_pattern:
                row.append((255, 255, 0))
            else:
                # Dark stormy background
                row.append((30, 30, 40))
        icon.append(row)
    return icon

def create_snow_icon():
    """Snowflakes falling"""
    icon = []
    snowflakes = [
        (8, 2), (8, 5), (16, 1), (16, 4), (16, 6),
        (24, 2), (24, 5), (12, 3), (20, 3), (28, 4)
    ]
    
    for y in range(MATRIX_HEIGHT):
        row = []
        for x in range(MATRIX_WIDTH):
            # Light gray clouds at top
            if y < 2:
                row.append((150, 150, 160))
            # Snowflakes
            elif (x, y) in snowflakes:
                row.append((255, 255, 255))
            # Snowflake arms
            elif any((abs(x - sx) == 1 and y == sy) or (abs(y - sy) == 1 and x == sx) 
                    for sx, sy in snowflakes):
                row.append((200, 200, 220))
            else:
                # Light blue background
                row.append((180, 200, 230))
        icon.append(row)
    return icon

def create_mist_icon():
    """Foggy/misty atmosphere"""
    icon = []
    for y in range(MATRIX_HEIGHT):
        row = []
        for x in range(MATRIX_WIDTH):
            # Horizontal fog bands
            if y % 2 == 0:
                brightness = 160 + (x % 4) * 10
                row.append((brightness, brightness, brightness + 20))
            else:
                brightness = 140 + (x % 4) * 10
                row.append((brightness, brightness, brightness + 20))
        icon.append(row)
    return icon

def create_error_icon():
    """Error indicator - red X"""
    icon = []
    for y in range(MATRIX_HEIGHT):
        row = []
        for x in range(MATRIX_WIDTH):
            # Draw X pattern
            if abs(x - y * 4) < 2 or abs(x - (MATRIX_WIDTH - y * 4)) < 2:
                row.append((255, 0, 0))
            else:
                row.append((0, 0, 0))
        icon.append(row)
    return icon

# Weather icon mapping
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


class WeatherMatrix:
    """Class to handle weather display on 8x32 LED matrix"""
    
    def __init__(self, api_key: str, width=MATRIX_WIDTH, height=MATRIX_HEIGHT,
                 pin=DEFAULT_LED_PIN, brightness=DEFAULT_BRIGHTNESS):
        """
        Initialize the weather matrix display
        
        Args:
            api_key: OpenWeatherMap API key
            width: Matrix width in pixels
            height: Matrix height in pixels
            pin: GPIO pin connected to the LED data line
            brightness: LED brightness (0.0 to 1.0)
        """
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
            index = y * self.width + x
        else:
            index = y * self.width + (self.width - 1 - x)
        
        return index
    
    def set_pixel(self, x, y, color):
        """Set a single pixel color"""
        index = self.xy_to_index(x, y)
        if index is not None:
            self.pixels[index] = color
    
    def clear(self):
        """Clear all pixels"""
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
    
    def show(self):
        """Update the display"""
        self.pixels.show()
    
    def get_weather_data(self, lat: float = MINNEAPOLIS_LAT, 
                        lon: float = MINNEAPOLIS_LON) -> Dict:
        """Fetch current weather data from OpenWeatherMap API"""
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'imperial'
        }
        
        try:
            print(f"→ Fetching weather for Minneapolis, MN ({lat}, {lon})...")
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
            
            print(f"✓ Weather data retrieved successfully")
            return weather_info
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching weather data: {e}")
            return None
        except KeyError as e:
            print(f"✗ Error parsing weather data: {e}")
            return None
    
    def map_weather_to_icon(self, weather_data: Dict) -> str:
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
    
    def display_icon(self, icon_key: str):
        """Display a weather icon on the matrix"""
        if icon_key not in WEATHER_ICONS:
            print(f"⚠ Unknown icon: {icon_key}, using error pattern")
            icon_key = 'error'
        
        # Generate icon pattern
        icon_pattern = WEATHER_ICONS[icon_key]()
        
        # Display on matrix
        for y in range(self.height):
            for x in range(self.width):
                color = icon_pattern[y][x]
                self.set_pixel(x, y, color)
        
        self.show()
    
    def animate_icon(self, icon_key: str, duration: float = 5.0):
        """Display weather icon with fade-in animation"""
        if icon_key not in WEATHER_ICONS:
            icon_key = 'error'
        
        icon_pattern = WEATHER_ICONS[icon_key]()
        steps = 20
        step_duration = duration / steps
        
        # Fade in animation
        for step in range(steps + 1):
            brightness = step / steps
            for y in range(self.height):
                for x in range(self.width):
                    r, g, b = icon_pattern[y][x]
                    self.set_pixel(x, y, (
                        int(r * brightness),
                        int(g * brightness),
                        int(b * brightness)
                    ))
            self.show()
            time.sleep(step_duration)
    
    def display_weather(self, animate: bool = True, duration: float = 10.0):
        """Fetch and display current weather"""
        weather_data = self.get_weather_data()
        
        if not weather_data:
            print("✗ Failed to get weather data, showing error pattern")
            self.display_icon('error')
            time.sleep(duration)
            return
        
        # Print weather information
        print("\n" + "="*50)
        print("MINNEAPOLIS WEATHER")
        print("="*50)
        print(f"Condition: {weather_data['description'].title()}")
        print(f"Temperature: {weather_data['temp']:.1f}°F")
        print(f"Feels Like: {weather_data['feels_like']:.1f}°F")
        print(f"Humidity: {weather_data['humidity']}%")
        print(f"Wind Speed: {weather_data['wind_speed']} mph")
        print(f"Updated: {weather_data['timestamp']}")
        print("="*50 + "\n")
        
        # Map to icon and display
        icon_key = self.map_weather_to_icon(weather_data)
        print(f"→ Displaying weather icon: {icon_key}")
        
        if animate:
            self.animate_icon(icon_key, duration)
        else:
            self.display_icon(icon_key)
            time.sleep(duration)
    
    def continuous_display(self, update_interval: int = 600, animate: bool = True):
        """Continuously display weather with periodic updates"""
        print(f"\n→ Starting continuous weather display")
        print(f"  Update interval: {update_interval} seconds ({update_interval/60:.1f} minutes)")
        print("  Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.display_weather(animate=animate, duration=update_interval)
        except KeyboardInterrupt:
            print("\n\n⚠ Display stopped by user")
            self.clear()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Display Minneapolis weather on 8x32 LED matrix',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python weather_matrix.py -k YOUR_API_KEY                    # Display once
  python weather_matrix.py -k YOUR_API_KEY -c                 # Continuous display
  python weather_matrix.py -k YOUR_API_KEY -c -i 300          # Update every 5 minutes
  python weather_matrix.py -k YOUR_API_KEY -b 0.5             # Brighter display

Get a free API key at: https://openweathermap.org/api
        """
    )
    
    parser.add_argument('-k', '--api-key', required=True,
                       help='OpenWeatherMap API key (required)')
    parser.add_argument('-b', '--brightness', type=float, default=DEFAULT_BRIGHTNESS,
                       help=f'Brightness level 0.0-1.0 (default: {DEFAULT_BRIGHTNESS})')
    parser.add_argument('-c', '--continuous', action='store_true',
                       help='Continuously update weather display')
    parser.add_argument('-i', '--interval', type=int, default=600,
                       help='Update interval in seconds for continuous mode (default: 600)')
    parser.add_argument('--no-animate', action='store_true',
                       help='Disable animation effects')
    parser.add_argument('-d', '--duration', type=float, default=10.0,
                       help='Display duration in seconds for single display (default: 10.0)')
    
    args = parser.parse_args()
    
    # Validate brightness
    if not 0.0 <= args.brightness <= 1.0:
        print("Error: Brightness must be between 0.0 and 1.0")
        sys.exit(1)
    
    # Validate interval
    if args.interval < 60:
        print("Warning: Update interval less than 60 seconds may exceed API rate limits")
    
    # Initialize display
    display = WeatherMatrix(
        api_key=args.api_key,
        brightness=args.brightness
    )
    
    try:
        if args.continuous:
            display.continuous_display(
                update_interval=args.interval,
                animate=not args.no_animate
            )
        else:
            display.display_weather(
                animate=not args.no_animate,
                duration=args.duration
            )
    finally:
        display.clear()
        print("\n✓ Display cleared")


if __name__ == "__main__":
    main()

# Made with Bob