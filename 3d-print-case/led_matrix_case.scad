// 8x32 WS2812B LED Matrix Case for Raspberry Pi
// Designed for Bambu P1S 3D Printer
// Made with Bob

// ===== CONFIGURATION =====

// LED Matrix dimensions (adjust to your actual matrix)
matrix_width = 256;  // 32 pixels * 8mm per pixel
matrix_height = 64;  // 8 pixels * 8mm per pixel
matrix_depth = 10;   // Thickness of LED matrix PCB

// Case parameters
wall_thickness = 2.5;
front_lip = 3;       // Lip to hold matrix in place
back_clearance = 15; // Space behind matrix for wiring
mounting_hole_dia = 3.5;  // M3 screw holes
corner_radius = 4;

// Diffuser parameters
diffuser_thickness = 2;
diffuser_gap = 5;    // Gap between LEDs and diffuser

// Stand parameters
stand_angle = 15;    // Tilt angle in degrees
stand_depth = 40;

// ===== MODULES =====

module rounded_box(width, height, depth, radius) {
    hull() {
        for (x = [radius, width - radius]) {
            for (y = [radius, height - radius]) {
                translate([x, y, 0])
                    cylinder(h=depth, r=radius, $fn=32);
            }
        }
    }
}

module case_back() {
    difference() {
        // Main case body
        rounded_box(
            matrix_width + 2*wall_thickness,
            matrix_height + 2*wall_thickness,
            back_clearance + wall_thickness,
            corner_radius
        );
        
        // Matrix cavity
        translate([wall_thickness, wall_thickness, wall_thickness])
            cube([matrix_width, matrix_height, back_clearance + 1]);
        
        // Front opening (with lip)
        translate([wall_thickness + front_lip, 
                   wall_thickness + front_lip, 
                   -1])
            cube([matrix_width - 2*front_lip, 
                  matrix_height - 2*front_lip, 
                  wall_thickness + 2]);
        
        // Wire management holes
        // Bottom center for power/data
        translate([matrix_width/2 + wall_thickness, 
                   wall_thickness/2, 
                   back_clearance/2])
            rotate([-90, 0, 0])
                cylinder(h=wall_thickness + 2, d=15, $fn=32);
        
        // Side hole for Raspberry Pi connection
        translate([wall_thickness/2, 
                   matrix_height/2 + wall_thickness, 
                   back_clearance/2])
            rotate([0, 90, 0])
                cylinder(h=wall_thickness + 2, d=20, $fn=32);
    }
    
    // Mounting posts for matrix (optional - use if matrix has mounting holes)
    post_inset = 5;
    post_height = 3;
    post_dia = 5;
    
    for (x = [post_inset, matrix_width - post_inset]) {
        for (y = [post_inset, matrix_height - post_inset]) {
            translate([wall_thickness + x, 
                       wall_thickness + y, 
                       wall_thickness]) {
                difference() {
                    cylinder(h=post_height, d=post_dia, $fn=32);
                    translate([0, 0, -1])
                        cylinder(h=post_height + 2, d=2.5, $fn=16);
                }
            }
        }
    }
}

module diffuser_frame() {
    difference() {
        // Outer frame
        rounded_box(
            matrix_width + 2*wall_thickness,
            matrix_height + 2*wall_thickness,
            diffuser_thickness,
            corner_radius
        );
        
        // Inner cutout for diffuser material
        translate([wall_thickness, wall_thickness, -1])
            cube([matrix_width, matrix_height, diffuser_thickness + 2]);
    }
}

module stand() {
    stand_width = matrix_width + 2*wall_thickness;
    stand_height = stand_depth * sin(stand_angle);
    stand_base = stand_depth * cos(stand_angle);
    
    difference() {
        union() {
            // Angled support
            hull() {
                cube([stand_width, wall_thickness, 0.1]);
                translate([0, stand_base, stand_height])
                    cube([stand_width, wall_thickness, 0.1]);
            }
            
            // Base
            cube([stand_width, stand_base + wall_thickness, wall_thickness]);
            
            // Back support
            translate([0, stand_base, 0])
                cube([stand_width, wall_thickness, stand_height + wall_thickness]);
        }
        
        // Mounting holes for case
        mount_spacing = 20;
        for (x = [mount_spacing, stand_width - mount_spacing]) {
            translate([x, stand_base + wall_thickness/2, stand_height])
                rotate([-90, 0, 0])
                    cylinder(h=wall_thickness + 2, d=mounting_hole_dia, $fn=16);
        }
    }
}

module wall_mount_bracket() {
    bracket_width = matrix_width + 2*wall_thickness;
    bracket_height = 40;
    
    difference() {
        union() {
            // Main plate
            cube([bracket_width, wall_thickness, bracket_height]);
            
            // Mounting tabs
            for (x = [10, bracket_width - 10]) {
                translate([x - 5, 0, bracket_height - 15])
                    cube([10, wall_thickness + 5, 10]);
            }
        }
        
        // Wall mounting holes
        for (x = [10, bracket_width - 10]) {
            translate([x, -1, bracket_height - 10])
                rotate([-90, 0, 0])
                    cylinder(h=wall_thickness + 7, d=4, $fn=16);
        }
        
        // Case mounting holes
        mount_spacing = 20;
        for (x = [mount_spacing, bracket_width - mount_spacing]) {
            translate([x, wall_thickness/2, 10])
                rotate([-90, 0, 0])
                    cylinder(h=wall_thickness + 2, d=mounting_hole_dia, $fn=16);
        }
    }
}

// ===== RENDER SELECTION =====

// Uncomment the part you want to print:

// Main case back (print this first)
case_back();

// Diffuser frame (optional - holds acrylic or paper diffuser)
//translate([0, matrix_height + 2*wall_thickness + 10, 0])
//    diffuser_frame();

// Desktop stand (optional)
//translate([0, -(stand_depth * cos(stand_angle) + 10), 0])
//    stand();

// Wall mount bracket (optional)
//translate([matrix_width + 2*wall_thickness + 10, 0, 0])
//    wall_mount_bracket();

// ===== PRINT NOTES =====
// 1. Print case_back with supports for wire holes
// 2. Use 0.2mm layer height, 20% infill
// 3. PLA or PETG recommended
// 4. Print time: ~3-4 hours for case_back
// 5. For diffuser: use white acrylic sheet or frosted plastic