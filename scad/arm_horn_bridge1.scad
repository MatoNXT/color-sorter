/*      
        Even More Customizable Straight LEGO Technic Beam
        Based on Customizable Straight LEGO Technic Beam
         and Parametric LEGO Technic Beam by "projunk" and "stevemedwin"
        
        www.thingiverse.com/thing:203935
        
        Also uploaded to Prusaprinters.org at https://www.prusaprinters.org/prints/33038-even-more-customizable-straight-beam-for-legotm-te
        
        Modified by Sam Kass
        November 2015
*/

// user parameters

// Hole sequence. o for round hole, + for plus-shaped hole, capital O for sideways hole, capital P for sideways plus, and x for blank spot. eg. "+ooo+", "oOo", "oxPxo", etc.
//holes = ""; // 5 holes with plusses at end

// If true, piece will be half-height
//half_height="false"; // [true, false]
difference() {
    union(){
        //rotate([0,0,0])translate([0,-8,0])drawBeam("ooooooo",false,1);
        rotate([0,0,0])translate([44,0,0])drawBeam("xo",false,1);
        rotate([0,0,0])translate([0,0,0])drawBeam("ooooox",false,1);
        #rotate([0,0,0])translate([38,0,0])cube([10,7.3,7.8]);
   }
}

/* [Hidden] */

$fn=50*1.0;


Pitch = 8*1.0;
Radius1 = 5.0/2;
Radius2 = 6.1/2;
//Height = half_height=="true"?4.0:7.8*1.0;
Depth = 0.85*1.0;
Width = 7.3*1.0; 
Plus_Width = 2.0*1.0;

Overhang = 0.05*1.0;

module body(holes,Height)
{
    translate([0, Width/2, 0]) 
    hull() {
        cylinder(r=Width/2, h=Height);
        
        translate([(len(holes)-1)*Pitch, 0, 0]) 
            cylinder(r=Width/2, h=Height);
    }
}

module hole(Height)
{
    union()
	{
        //core
        cylinder(r=Radius1,h=Height);
        
        //top countersink
        translate([0,0,Height-Depth+Overhang]) 
            cylinder(r=Radius2,h=Depth);
        
        //bottom countersink
        translate([0,0,-Overhang/2]) 
            cylinder(r=Radius2,h=Depth);
        
        translate([0,0,Depth-Overhang])
            cylinder(h=(Radius2 - Radius1), r1=Radius2, r2=Radius1);
    }
}

module plus(Height) {

    union() {
        translate([-Plus_Width/2, -Radius1, -Overhang]) 
            cube([Plus_Width, Radius1*2, Height+Overhang*2]);
        translate([-Radius1, -Plus_Width/2, -Overhang]) 
            cube([Radius1*2, Plus_Width, Height+Overhang*2]);
    }
}

module drawBeam(holes,half_height,height)
{
    Height = height * (half_height==true?4.0:7.8*1.0);
    difference()
    {
        body(holes,Height);
       
        for (i = [1:len(holes)])
        {
            if (holes[i-1] == "+")
                translate([(i-1)*Pitch, Width/2, 0])
                    plus(Height);
            else if (holes[i-1] == "o")
                translate([(i-1)*Pitch, Width/2, 0])
                    hole(Height);
            else if (holes[i-1] == "O")
                rotate([90,0,0])
                translate([(i-1)*Pitch, Width/2,-Pitch+Depth/2])
                    hole(Height);
            else if (holes[i-1] == "P")
                rotate([90,0,0])
                translate([(i-1)*Pitch, Width/2,-Pitch+Depth/2])
                    plus(Height);
            else if (holes[i-1] == "x") {}
            else
                translate([(i-1)*Pitch, Width/2, 0])
                    hole(Height);
        }
    }
}

