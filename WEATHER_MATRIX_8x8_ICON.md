# Weather Matrix - 8x8 Icon Display

## Overview
The weather matrix display has been modified to show weather icons in an **8x8 pixel grid on the LEFT SIDE** of the 8x32 LED matrix. This leaves the remaining 24 columns (columns 8-31) available for displaying other content like text, scrolling messages, or additional information.

## Display Layout

```
┌─────────┬──────────────────────────────────┐
│         │                                  │
│  8x8    │     24 columns available         │
│ ICON    │     for other content            │
│         │                                  │
└─────────┴──────────────────────────────────┘
  0-7        8-31 (columns)
```

## Key Changes

### 1. Icon Size
- **Previous**: Icons filled the entire 8x32 matrix (256 pixels)
- **Current**: Icons are confined to an 8x8 grid (64 pixels) on the left side

### 2. Icon Functions
All weather icon generation functions have been updated to create 8x8 patterns:
- `create_clear_day_icon()` - Compact sun with rays
- `create_clear_night_icon()` - Crescent moon with stars
- `create_clouds_icon()` - Fluffy clouds
- `create_rain_icon()` - Rain drops
- `create_thunderstorm_icon()` - Lightning bolt
- `create_snow_icon()` - Snowflakes
- `create_mist_icon()` - Fog bands
- `create_error_icon()` - Red X pattern

### 3. Display Methods

#### `display_icon(icon_key, clear_rest=True)`
Displays an 8x8 weather icon on the left side of the matrix.
- **icon_key**: The weather condition key
- **clear_rest**: If True, clears columns 8-31 (default: True)

#### `animate_icon(icon_key, duration=5.0, clear_rest=True)`
Displays an 8x8 weather icon with fade-in animation.
- **icon_key**: The weather condition key
- **duration**: Animation duration in seconds
- **clear_rest**: If True, clears columns 8-31 (default: True)

### 4. Helper Methods

#### `get_icon_bounds()`
Returns the bounds of the icon area: `(0, 8, 0, 8)`

#### `get_content_bounds()`
Returns the bounds of the available content area: `(8, 32, 0, 8)`

## Usage Examples

### Basic Usage (Same as Before)
```python
from weather_matrix import WeatherMatrix

# Initialize
display = WeatherMatrix(api_key="YOUR_API_KEY")

# Display weather (icon on left, rest cleared)
display.display_weather()
```

### Display Icon Without Clearing Rest
```python
# Display icon but keep other content on the right side
display.display_icon('clear_day', clear_rest=False)
```

### Using the Available Space
```python
# Get the content area bounds
x_start, x_end, y_start, y_end = display.get_content_bounds()

# Display weather icon on left
display.display_icon('rain', clear_rest=False)

# Now you can use columns 8-31 for other content
# Example: Set some pixels in the content area
for x in range(x_start, x_end):
    display.set_pixel(x, 4, (255, 255, 255))  # White line
display.show()
```

### Combining with Text/Scrolling
```python
# Display weather icon
display.display_icon('clouds', clear_rest=False)

# Use the right side for scrolling text or other displays
# (You would integrate with a text scrolling library here)
```

## Matrix Coordinate System

The matrix uses a serpentine (zigzag) wiring pattern:
- **Even rows (0, 2, 4, 6)**: Left to right
- **Odd rows (1, 3, 5, 7)**: Right to left

Icon area: Columns 0-7, Rows 0-7
Content area: Columns 8-31, Rows 0-7

## Benefits

1. **Efficient Use of Space**: Weather icon takes only 25% of the display
2. **Flexibility**: 75% of the display available for other content
3. **Modular Design**: Icon and content areas are independent
4. **Backward Compatible**: Existing code works with `clear_rest=True` (default)

## Notes

- The `clear_rest` parameter allows you to control whether the right side is cleared
- Set `clear_rest=False` when you want to manage the content area yourself
- The icon always appears on the left side (columns 0-7)
- All weather conditions are optimized for 8x8 display

## Example Integration

```python
#!/usr/bin/env python3
from weather_matrix import WeatherMatrix
import time

# Initialize display
display = WeatherMatrix(api_key="YOUR_API_KEY", brightness=0.3)

# Display weather icon on left
weather_data = display.get_weather_data()
icon_key = display.map_weather_to_icon(weather_data)
display.display_icon(icon_key, clear_rest=False)

# Use right side for temperature display or scrolling text
# (Add your custom content here for columns 8-31)

# Keep display running
time.sleep(60)
display.clear()
```

## Made with Bob