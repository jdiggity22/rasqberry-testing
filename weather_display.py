#!/usr/bin/env python3
"""
Weather Icon Display for Minneapolis, Minnesota
Displays current weather conditions as icons on WS2812B LED strip
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

# Configuration
DEFAULT_LED_COUNT = 8
DEFAULT_LED_PIN = board.D10  # GPIO 10 (SPI MOSI)
DEFAULT_BRIGHTNESS = 0.5
DEFAULT_PIXEL_ORDER = neopixel.GRB
MINNEAPOLIS_LAT = 44.9778
MINNEAPOLIS_LON = -93.2650

# Weather icon patterns for 8 LEDs
# Each pattern is a list of (R, G, B) tuples
WEATHER_ICONS = {
    'clear_day': [
        (255, 200, 0),   # Bright yellow sun
        (255, 180, 0),
        (255, 160, 0),
        (255, 140, 0),
        (255, 160, 0),
        (255, 180, 0),
        (255, 200, 0),
        (255, 220, 0),
    ],
    'clear_night': [
        (200, 200, 255),  # Pale blue moon
        (180, 180, 240),
        (160, 160, 220),
        (140, 140, 200),
        (120, 120, 180),
        (100, 100, 160),
        (80, 80, 140),
        (60, 60, 120),
    ],
    'clouds': [
        (180, 180, 180),  # Gray clouds
        (200, 200, 200),
        (220, 220, 220),
        (240, 240, 240),
        (220, 220, 220),
        (200, 200, 200),
        (180, 180, 180),
        (160, 160, 160),
    ],
    'rain': [
        (0, 100, 200),    # Blue rain
        (0, 120, 220),
        (0, 140, 240),
        (0, 160, 255),
        (0, 140, 240),
        (0, 120, 220),
        (0, 100, 200),
        (0, 80, 180),
    ],
    'thunderstorm': [
        (255, 255, 0),    # Yellow lightning
        (200, 200, 0),
        (150, 150, 0),
        (100, 100, 100),  # Dark clouds
        (80, 80, 80),
        (255, 255, 0),    # Lightning
        (200, 200, 0),
        (100, 100, 100),
    ],
    'snow': [
        (255, 255, 255),  # White snow
        (240, 240, 255),
        (220, 220, 255),
        (200, 200, 255),
        (220, 220, 255),
        (240, 240, 255),
        (255, 255, 255),
        (240, 240, 240),
    ],
    'mist': [
        (200, 200, 220),  # Light gray mist
        (180, 180, 200),
        (160, 160, 180),
        (140, 140, 160),
        (160, 160, 180),
        (180, 180, 200),
        (200, 200, 220),
        (180, 180, 200),
    ],
    'error': [
        (255, 0, 0),      # Red error indicator
        (0, 0, 0),
        (255, 0, 0),
        (0, 0, 0),
        (255, 0, 0),
        (0, 0, 0),
        (255, 0, 0),
        (0, 0, 0),
    ],
}


class WeatherDisplay:
    """Class to handle weather display on LED strip"""
    
    def __init__(self, api_key: str, num_pixels: int = DEFAULT_LED_COUNT,
                 pin=DEFAULT_LED_PIN, brightness: float = DEFAULT_BRIGHTNESS,
                 pixel_order=DEFAULT_PIXEL_ORDER):
        """
        Initialize the weather display
        
        Args:
            api_key: OpenWeatherMap API key
            num_pixels: Number of LEDs in the strip
            pin: GPIO pin connected to the LED data line
            brightness: LED brightness (0.0 to 1.0)
            pixel_order: Pixel color order (GRB, RGB, etc.)
        """
        self.api_key = api_key
        self.num_pixels = num_pixels
        
        try:
            self.pixels = neopixel.NeoPixel(
                pin,
                num_pixels,
                brightness=brightness,
                auto_write=False,
                pixel_order=pixel_order
            )
            print(f"✓ Initialized {num_pixels} LEDs on pin {pin}")
        except Exception as e:
            print(f"✗ Error initializing LEDs: {e}")
            sys.exit(1)
    
    def clear(self):
        """Turn off all LEDs"""
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
    
    def get_weather_data(self, lat: float = MINNEAPOLIS_LAT, 
                        lon: float = MINNEAPOLIS_LON) -> Dict:
        """
        Fetch current weather data from OpenWeatherMap API
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary with weather data
        """
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'imperial'  # Fahrenheit
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
        """
        Map weather condition to icon pattern
        
        Args:
            weather_data: Weather data dictionary
            
        Returns:
            Icon key for WEATHER_ICONS
        """
        if not weather_data:
            return 'error'
        
        condition = weather_data['condition']
        icon_code = weather_data.get('icon_code', '')
        is_day = 'd' in icon_code  # OpenWeatherMap uses 'd' for day, 'n' for night
        
        # Map conditions to icons
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
            return 'clouds'  # Default to clouds for unknown conditions
    
    def display_icon(self, icon_key: str, duration: float = 5.0):
        """
        Display a weather icon pattern on the LEDs
        
        Args:
            icon_key: Key from WEATHER_ICONS dictionary
            duration: How long to display the icon (seconds)
        """
        if icon_key not in WEATHER_ICONS:
            print(f"⚠ Unknown icon: {icon_key}, using error pattern")
            icon_key = 'error'
        
        pattern = WEATHER_ICONS[icon_key]
        
        # Set each LED to the pattern color
        for i in range(min(self.num_pixels, len(pattern))):
            self.pixels[i] = pattern[i]
        
        self.pixels.show()
        time.sleep(duration)
    
    def animate_icon(self, icon_key: str, duration: float = 5.0):
        """
        Display weather icon with animation effect
        
        Args:
            icon_key: Key from WEATHER_ICONS dictionary
            duration: Total animation duration (seconds)
        """
        if icon_key not in WEATHER_ICONS:
            icon_key = 'error'
        
        pattern = WEATHER_ICONS[icon_key]
        steps = 20
        step_duration = duration / steps
        
        # Fade in animation
        for step in range(steps):
            brightness = step / steps
            for i in range(min(self.num_pixels, len(pattern))):
                r, g, b = pattern[i]
                self.pixels[i] = (
                    int(r * brightness),
                    int(g * brightness),
                    int(b * brightness)
                )
            self.pixels.show()
            time.sleep(step_duration)
    
    def display_weather(self, animate: bool = True, duration: float = 10.0):
        """
        Fetch and display current weather
        
        Args:
            animate: Whether to animate the display
            duration: How long to display the weather (seconds)
        """
        # Get weather data
        weather_data = self.get_weather_data()
        
        if not weather_data:
            print("✗ Failed to get weather data, showing error pattern")
            self.display_icon('error', duration)
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
            self.display_icon(icon_key, duration)
    
    def continuous_display(self, update_interval: int = 600, animate: bool = True):
        """
        Continuously display weather with periodic updates
        
        Args:
            update_interval: Seconds between weather updates (default: 10 minutes)
            animate: Whether to animate transitions
        """
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
        description='Display Minneapolis weather on WS2812B LED strip',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python weather_display.py -k YOUR_API_KEY                    # Display once
  python weather_display.py -k YOUR_API_KEY -c                 # Continuous display
  python weather_display.py -k YOUR_API_KEY -c -i 300          # Update every 5 minutes
  python weather_display.py -k YOUR_API_KEY -n 16 -b 0.3       # 16 LEDs, 30% brightness

Get a free API key at: https://openweathermap.org/api
        """
    )
    
    parser.add_argument('-k', '--api-key', required=True,
                       help='OpenWeatherMap API key (required)')
    parser.add_argument('-n', '--num-leds', type=int, default=DEFAULT_LED_COUNT,
                       help=f'Number of LEDs (default: {DEFAULT_LED_COUNT})')
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
    display = WeatherDisplay(
        api_key=args.api_key,
        num_pixels=args.num_leds,
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
        # Always clear LEDs on exit
        display.clear()
        print("\n✓ LEDs cleared")


if __name__ == "__main__":
    main()

# Made with Bob