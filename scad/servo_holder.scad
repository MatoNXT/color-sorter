echo(version=version());

// -------------------------------------------------------------------------------------------------------------------
/*
initial parameters
change these to create your brick
*/
nubs_cnt_x = 4; // INT > count of nubs in X
nubs_cnt_y = 4; // INT > count of nubs in Y
nubs_on_top = true; // BOOLEAN > if nubs should be rendered or not [true, false]
nubs_diameter_mod = 0; // FLOAT > increases the nub-diameter for 3D-Printing reasons (i.e. 0.2)

brick_height = 11; // INT > height of brick in lego-units (1=plate, 3=normal height) [1,2,3,4,5,6]

text_on_top = ""; // STRING > text (if wanted, elswhere empty) - if text on top set nubs_on_top = false (otherwise no text)!
text_on_front = ""; // STRING > text on the front side (if wanted, elsewhere empty)
text_on_back = ""; // STRING > text on the front side (if wanted, elsewhere empty)
text_size_top = 7; // INT > text-size (12 suits best for top text and count of nubs in y = 2) on the top
text_size_front = 7; // INT > text-size (12 suits best for top text and count of nubs in y = 2) on the front
text_size_back = 7; // INT > text-size (12 suits best for top text and count of nubs in y = 2) on the back
text_extrusion_factor = 1.0; // FLOAT > factor for text-extrusion (X * lego-unit - Info: height of nubs is 1 lego-unit)
text_language = "de"; // STRING > which language for the text (use two letter code) [i.e. "de", "fr", etc.]
text_offset_y = 1.5; // FLOAT > text offset in text-up/down-direction
keyring_diameter = 0; // FLOAT > want a keyring-hole ? sets diameter of keyring (bigger than 0)
strong_brick = true; // BOOLEAN > walls at every (true) or every second (false) pipe in the inner of brick [true,false]

//Circle resolution
// $fa the minimum angle for a fragment. see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$fs
$fa = $preview ? 12 : 1;
// $fs the minimum size of a fragment. see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$fs
$fs = $preview ? 2 : 0.4;
// -------------------------------------------------------------------------------------------------------------------

/*
calling module with parameters
*/
difference(){
    union(){
        //translate([8,-8,0])brick(3, 6, nubs_on_top, 3, text_on_top, text_size_top, text_on_front, text_size_front,text_on_back, text_size_back, text_language, text_offset_y, nubs_diameter_mod, keyring_diameter, strong_brick);
        translate([0,0,0])brick(8, 4, nubs_on_top, 3, text_on_top, text_size_top, text_on_front, text_size_front,text_on_back, text_size_back, text_language, text_offset_y, nubs_diameter_mod, keyring_diameter, strong_brick);
        translate([0,0,9.6])brick(6, 4, nubs_on_top, 3, text_on_top, text_size_top, text_on_front, text_size_front,text_on_back, text_size_back, text_language, text_offset_y, nubs_diameter_mod, keyring_diameter, strong_brick);
        translate([0,0,9.6+9.6])brick(4, 4, nubs_on_top, 5, text_on_top, text_size_top, text_on_front, text_size_front,text_on_back, text_size_back, text_language, text_offset_y, nubs_diameter_mod, keyring_diameter, strong_brick);
        translate([0,0,0])cube([16.2,31.8,9.6*(brick_height/3)]);
    }

    translate([1.2,4,-1])
        union(){
            translate([1.2,.5,0])cube([12.5,23,15*(brick_height/3)]);
            translate([-1.2,-4,9.872*(brick_height/3)])cube([16,31.8,2]);
            #translate([-1.3,-4,1*((brick_height-7)/3)-0.4])cube([15,31.8,9*(brick_height/3)]);
        }
    //difference() {
    //    translate([-0.2,-0.2,0])cube([13.3,24.4,15]);
    //    cube([13,24,15]);
    //}
}
translate([8,0,0])brick(1, 1, nubs_on_top, 3, text_on_top, text_size_top, text_on_front, text_size_front,text_on_back, text_size_back, text_language, text_offset_y, nubs_diameter_mod, keyring_diameter, strong_brick);
translate([8,8*3,0])brick(1, 1, nubs_on_top, 3, text_on_top, text_size_top, text_on_front, text_size_front,text_on_back, text_size_back, text_language, text_offset_y, nubs_diameter_mod, keyring_diameter, strong_brick);

translate([8,7.4*-1,0])brick(2, 1, nubs_on_top, 3, text_on_top, text_size_top, text_on_front, text_size_front,text_on_back, text_size_back, text_language, text_offset_y, nubs_diameter_mod, keyring_diameter, strong_brick);
translate([8,7.8*4,0])brick(2, 1, nubs_on_top, 3, text_on_top, text_size_top, text_on_front, text_size_front,text_on_back, text_size_back, text_language, text_offset_y, nubs_diameter_mod, keyring_diameter, strong_brick);

translate([0,7.4*-1,9.6])brick(3, 1, nubs_on_top, 3, text_on_top, text_size_top, text_on_front, text_size_front,text_on_back, text_size_back, text_language, text_offset_y, nubs_diameter_mod, keyring_diameter, strong_brick);
translate([0,7.8*4,9.6])brick(3, 1, nubs_on_top, 3, text_on_top, text_size_top, text_on_front, text_size_front,text_on_back, text_size_back, text_language, text_offset_y, nubs_diameter_mod, keyring_diameter, strong_brick);



/*
module brick

- count of nubs in X // nubs_cnt_x = 10;
- count of nubs in Y // nubs_cnt_y = 1;
- boolean, if nubs should be rendered or not // nubs_on_top = false; // [true, false]
- height of brick in lego-units (1=plate, 3=normal height) // brick_height = 1; // [1,2,3,4,5,6]
- text (if wanted) on top surface - leave empty for no text // text_on_brick = "hello world";
- text-size (12 suits best top - 2 nubs in y) // text_size = 12;
- text-position (top or front) // text_position = "top" ["top", "front"]
- text_language (for accents etc.) // (use two letter code) // [i.e. "de", "fr", etc.]
- text offset in text-up/down-direction // text_offset_y = 0
- keyring-diameter // keyring_diameter = 1
- strong_brick // Boolean to add so much wall under the brick
*/
module brick(nubs_cnt_x, nubs_cnt_y, nubs_on_top, brick_height, text_on_top, text_size_top, text_on_front, text_size_front, text_on_back, text_size_back, text_language, text_offset_y, nubs_diameter_mod, keyring_diameter, strong_brick) {

    lego_unit = 1.6;

    grid_base = 8;
    grid_offset = 0.2;
    nubs_height = lego_unit; // 1.6
    nubs_diameter = 3 * lego_unit+nubs_diameter_mod; // 4.8
    nubs_radius = nubs_diameter / 2;
    brick_wall = 1.2;
    brick_wall_top = 1;
    cylinder_diameter_outer = 6.51;
    cylinder_diameter_inner = 3 * lego_unit; // 4.8
    brick_baseheight = 6 * lego_unit; //9.6

    brick_height_crt = brick_baseheight / 3 * brick_height;
    brick_x_crt = (nubs_cnt_x * grid_base) - grid_offset;
    brick_y_crt = (nubs_cnt_y * grid_base) - grid_offset;
    nubs_offset_outer = (grid_base - grid_offset) / 2;

    difference() { // for keyring-hole to get through whole brick
        color("red") {
            difference() {
                translate([0,0,0]) cube([brick_x_crt,brick_y_crt,brick_height_crt]);
                union() {
                    translate([brick_wall,brick_wall,0])
                        cube([brick_x_crt - (2*brick_wall),
                            brick_y_crt - (2*brick_wall),
                            brick_height_crt - brick_wall_top]);
                }
            }

            if (nubs_on_top) {
                for (x=[0:1:nubs_cnt_x - 1]) {
                    for (y=[0:1:nubs_cnt_y - 1]) {
                        translate([nubs_offset_outer + (x*grid_base),
                                    nubs_offset_outer + (y*grid_base),
                                    brick_height_crt]) {
                                        cylinder(h=nubs_height,r=nubs_radius);
                                    }
                    }
                }
            }

            if (nubs_cnt_x > 1 && nubs_cnt_y == 1) {
                cylinder_diameter_outer = 2 * lego_unit;
                y = nubs_cnt_y / 2;
                for (x=[1:1:nubs_cnt_x - 1]) {
                    translate([x*grid_base - grid_offset/2,y*grid_base - grid_offset/2,0]) {
                        cylinder(h=brick_height_crt-brick_wall, r=cylinder_diameter_outer/2);
                    }
                    if (x%2 == 0) {
                        translate([(x*grid_base - grid_offset/2) - brick_wall_top / 2,0,0]) {
                            cube([brick_wall_top,brick_y_crt,brick_height_crt]);
                        }
                    }
                }
            }
            else if (nubs_cnt_x == 1 && nubs_cnt_y > 1) {
                cylinder_diameter_outer = 2 * lego_unit;
                x = nubs_cnt_x / 2;
                for (y=[1:1:nubs_cnt_y - 1]) {
                    translate([x*grid_base - grid_offset/2,y*grid_base - grid_offset/2,0]) {
                        cylinder(h=brick_height_crt-brick_wall, r=cylinder_diameter_outer/2);
                    }
                    if (y%2 == 0) {
                        translate([0,(y*grid_base - grid_offset/2) - brick_wall_top / 2,0]) {
                            cube([brick_x_crt,brick_wall_top,brick_height_crt]);
                        }
                    }
                }
            }
            else {
                difference() {
                    for (x=[1:1:nubs_cnt_x - 1]) {
                        if ((strong_brick) || (x%2 == 0)) {
                            translate([x*grid_base - brick_wall/2, 0, 0]) {
                                union(){
                                    cube([brick_wall_top, brick_y_crt, brick_height_crt]);
//                                    translate([-(x*grid_base - brick_wall/2),x*grid_base - brick_wall/2,0])
//                                        cube([brick_y_crt, brick_wall_top, brick_height_crt]);
                                };
                            }
                        }
                        for (y=[1:1:nubs_cnt_y - 1]) {
                            translate([x*grid_base - grid_offset/2,y*grid_base - grid_offset/2,0]) {
                                difference() {
                                    cylinder(h=brick_height_crt-brick_wall, r=cylinder_diameter_outer/2);
                                    cylinder(h=brick_height_crt-brick_wall, r=cylinder_diameter_inner/2);
                                }
                            }
                        }
                    }
                    for (x=[1:1:nubs_cnt_x - 1]) {
                        translate([x*grid_base - brick_wall/2, 0, 0]) {
                            for (y=[1:1:nubs_cnt_y - 1]) {
                                translate([brick_wall_top/2,y*grid_base - grid_offset/2,0]) {
                                    cylinder(h=brick_height_crt-brick_wall, r=cylinder_diameter_inner/2);
                                }
                            }
                        }
                    }
                }
            }
        }
        if(keyring_diameter > 0) {
            translate([brick_x_crt*0.85,brick_y_crt,brick_height_crt/2]) {
                rotate([90,0,45]) {
                    cylinder(brick_height_crt*brick_y_crt,keyring_diameter,keyring_diameter,center=true);
                }
            }
        }
    }

    if (text_on_top != "" && !nubs_on_top) {
        color("green")
            translate([brick_x_crt/2,brick_y_crt/2+text_offset_y,brick_height_crt])
                linear_extrude(text_extrusion_factor * nubs_height)
                    text(text_on_top, size=text_size_top, halign="center", valign="center", language=text_language);
    }
    if(text_on_front != "") {
        color("green")
            rotate([90,0,0]) translate([brick_x_crt/2,text_size_front/2+text_offset_y,-0.5])
                linear_extrude(nubs_height) text(text_on_front, size=text_size_front, halign="center", valign="center", language=text_language);
        }
    if(text_on_back != "") {
        color("green")
            rotate([90,0,180]) translate([(brick_x_crt/2)*-1, text_size_back/2+text_offset_y, brick_y_crt])
                linear_extrude(nubs_height) text(text_on_back, size=text_size_back, halign="center", valign="center", language=text_language);
    }
}
