# 3D Printed Case for 8x32 LED Matrix Display

This folder contains 3D printable designs for housing your 8x32 WS2812B LED matrix with Raspberry Pi.

## 📦 What's Included

### `led_matrix_case.scad`
OpenSCAD source file with multiple components:
1. **Main Case Back** - Holds the LED matrix and provides wire management
2. **Diffuser Frame** (optional) - Holds a diffuser sheet for softer light
3. **Desktop Stand** (optional) - Angled stand for desk display
4. **Wall Mount Bracket** (optional) - For wall mounting

## 🖨️ Printing Instructions for Bambu P1S

### Recommended Settings
- **Material**: PLA or PETG
- **Layer Height**: 0.2mm
- **Infill**: 20%
- **Supports**: Yes (for wire management holes)
- **Brim/Raft**: Not needed
- **Print Time**: ~3-4 hours for main case

### Step-by-Step Process

#### 1. Generate STL Files

You have two options:

**Option A: Use OpenSCAD (Recommended)**
1. Download and install [OpenSCAD](https://openscad.org/)
2. Open `led_matrix_case.scad`
3. Uncomment the part you want to print (line 189-200)
4. Press F5 to preview, F6 to render
5. Export as STL: File → Export → Export as STL

**Option B: Use Online Converter**
1. Upload `led_matrix_case.scad` to [OpenSCAD Cloud](https://openscad.cloud/)
2. Render and download STL

#### 2. Prepare in Bambu Studio

1. Open Bambu Studio
2. Import the STL file
3. **Orientation**: Case should print with back down (flat side)
4. **Supports**: Enable for wire holes
   - Support type: Tree (auto)
   - Support density: 15%
5. **Material**: Select PLA or PETG
6. **Quality**: 0.20mm Standard

#### 3. Print Settings in Bambu Studio

```
Material: PLA Basic
Layer Height: 0.20mm
Wall Loops: 3
Top/Bottom Layers: 4
Infill: 20% (Grid pattern)
Support: Tree (Auto)
Brim: None
Speed: Normal (default)
```

#### 4. Print Order

Print in this order:
1. **Main Case Back** (required) - ~3-4 hours
2. **Desktop Stand** OR **Wall Mount** (choose one) - ~1-2 hours
3. **Diffuser Frame** (optional) - ~30 minutes

## 📐 Dimensions

### LED Matrix Case
- **External**: 266mm × 74mm × 17.5mm (W × H × D)
- **Internal cavity**: 256mm × 64mm × 15mm
- **Wall thickness**: 2.5mm
- **Weight**: ~150g (PLA)

### Desktop Stand
- **Base depth**: 40mm
- **Tilt angle**: 15°
- **Compatible with**: Main case back

### Wall Mount Bracket
- **Height**: 40mm
- **Mounting holes**: 4mm diameter (for M3/M4 screws)

## 🔧 Assembly Instructions

### What You'll Need
- Printed case parts
- 8x32 WS2812B LED Matrix
- Raspberry Pi (any model with GPIO)
- M2.5 or M3 screws (4-8 pieces, 6-10mm length)
- Optional: Acrylic or frosted plastic sheet for diffuser (256mm × 64mm)
- Optional: Double-sided tape or hot glue

### Assembly Steps

1. **Test Fit the Matrix**
   - Place LED matrix into case cavity
   - Ensure it sits flush against the front lip
   - Check that wire holes align with your connections

2. **Secure the Matrix**
   - Option A: Use mounting posts (if your matrix has holes)
   - Option B: Use small dabs of hot glue in corners
   - Option C: Use double-sided foam tape

3. **Wire Management**
   - Route power and data cables through bottom hole
   - Route Raspberry Pi connection through side hole
   - Leave some slack for strain relief

4. **Optional: Add Diffuser**
   - Cut white acrylic or frosted plastic to 256mm × 64mm
   - Place in diffuser frame
   - Attach frame to front of case with small screws or glue

5. **Attach Stand or Wall Mount**
   - For desktop: Attach stand with M3 screws
   - For wall: Attach bracket, then mount to wall with appropriate anchors

## 🎨 Customization

### Adjusting Dimensions

Edit these values in the `.scad` file (lines 7-12):

```openscad
matrix_width = 256;   // Adjust for your matrix
matrix_height = 64;   // Adjust for your matrix
matrix_depth = 10;    // PCB thickness
wall_thickness = 2.5; // Case wall thickness
```

### Changing Stand Angle

Edit line 18:
```openscad
stand_angle = 15;  // Change to desired angle (0-45°)
```

### Adding Ventilation Holes

Add this code before the final closing brace in `case_back()`:

```openscad
// Ventilation holes
for (x = [20:20:matrix_width-20]) {
    translate([wall_thickness + x, 
               wall_thickness/2, 
               back_clearance - 5])
        rotate([-90, 0, 0])
            cylinder(h=wall_thickness + 2, d=5, $fn=16);
}
```

## 🖼️ Diffuser Options

For best LED diffusion:

1. **White Acrylic** (3mm thick)
   - Best light diffusion
   - Available at hardware stores
   - Cut to size with scoring knife

2. **Frosted Plastic Sheet**
   - Cheaper alternative
   - Can use frosted report covers
   - Easier to cut

3. **Parchment Paper** (temporary)
   - Quick test option
   - Not durable
   - Tape to front of case

## 📊 Material Usage

### PLA Filament Required
- Main Case: ~120g
- Desktop Stand: ~40g
- Wall Mount: ~30g
- Diffuser Frame: ~20g
- **Total**: ~210g (one spool is plenty)

### Print Time Estimates (Bambu P1S)
- Main Case: 3-4 hours
- Desktop Stand: 1-2 hours
- Wall Mount: 1 hour
- Diffuser Frame: 30 minutes

## 🔍 Troubleshooting

### Matrix doesn't fit
- Check your matrix dimensions
- Adjust `matrix_width` and `matrix_height` in .scad file
- Re-export STL

### Supports difficult to remove
- Use tree supports instead of linear
- Reduce support density to 10-15%
- Use support interface layers

### Case warping during print
- Ensure bed is level
- Use brim if needed
- Increase bed temperature by 5°C

### Wire holes too small
- Measure your cable bundle
- Edit hole diameter in .scad file (line 56-57)
- Re-export STL

## 🎯 Design Features

- **Wire Management**: Dedicated holes for clean cable routing
- **Mounting Posts**: Optional posts for securing matrix
- **Modular Design**: Mix and match stand or wall mount
- **Diffuser Ready**: Frame holds standard acrylic sheets
- **Raspberry Pi Access**: Side hole for easy GPIO connection
- **Tilted Display**: 15° angle for optimal viewing

## 📝 License

This design is open source. Feel free to modify and share!

## 🔗 Related Files

- Main project: `../` (LED matrix control software)
- Weather display: `../weather_scroll.py`
- Scrolling text: `../scroll_think.py`

## 💡 Tips

1. **Print orientation matters**: Always print case with back (flat side) down
2. **Test fit before gluing**: Dry fit everything first
3. **Cable management**: Leave slack in wires for easy maintenance
4. **Diffuser spacing**: 5mm gap between LEDs and diffuser is optimal
5. **Color choice**: Black or dark gray PLA hides the electronics best

## 🛠️ Advanced Modifications

### Add Raspberry Pi Mount
Add a mounting plate inside the case for the Pi:
- Measure your Pi model
- Add standoffs to case back
- Use M2.5 screws to secure Pi

### Create Custom Front Panel
Design a decorative front panel:
- Export case dimensions
- Design in CAD software
- Print in different color/material

### Multi-Color Printing
Use Bambu's AMS system:
- Print case in black
- Print front accents in white
- Use pause-and-swap for logos

Made with Bob 🤖