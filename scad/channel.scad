/**
* MachineBlocks
* https://machineblocks.com/examples/boxes-enclosures
*
* Channel 6x1
* Copyright (c) 2022 - 2025 Jan Philipp Knoeller <pk@pksoftware.de>
*
* Published under license:
* Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International 
* https://creativecommons.org/licenses/by-nc-sa/4.0/
*
*/
use <mod/block.scad>;


lego_brick_channel([0,0,0]  ,[5,2,4], [true,false,"classic"]);

//l?|lego_brick([-1,-1.5,1]  ,[7,1,1], [true,false,"none"]);
lego_brick([-1,-1.5,0]  ,[1,1,2], [true,false,"classic",0]);
lego_brick([5,-1.5,0]  ,[1,1,2], [true,false,"classic",0]);

lego_brick([0,-2.5,1]  ,[5,2,2], [true,false,"classic",2]);

module lego_brick_channel(position, shape_size, params) {
    translate([((shape_size[0]/2)+position[0])*8,((shape_size[1]/2)+position[1])*8,position[2]*3.2])brick_channel(shape_size,params);
}

module brick_channel(shape_size,params) {
    /* [View] */
    // How to view the brick in the editor
    viewMode = "print"; // [print, assembled, cover]

    /* [Size] */

    // Box size in X-direction specified as multiple of an 1x1 brick.
    boxSizeX = shape_size[0]; // [1:32] 
    // Box size in Y-direction specified as multiple of an 1x1 brick.
    boxSizeY = shape_size[1]; // [1:32] 
    // Total box height specified as number of layers. Each layer has the height of one plate.
    boxLayers = shape_size[2]; // [1:24]

    /* [Appearance] */

    // Type of cut-out on the underside.
    baseCutoutType = "classic"; // [none, classic]
    // Whether the base should have knobs
    baseKnobs = false;
    // Type of the base knobs
    baseKnobType = "classic"; // [classic, technic]
    // Whether base knobs should be centered.
    baseKnobCentered = false;
    // Whether the pit should contain knobs
    basePitKnobs = false;
    // Type of the base pit knobs
    basePitKnobType = "classic"; // [classic, technic]
    // Whether base pit knobs should be centered.
    basePitKnobCentered = false;
    // Pit wall thickness
    basePitWallThickness = 0.333;
    // Pit wall gaps
    basePitWallGaps = [[0, 0, 0], [1, 0, 0]];
    // Whether the base should have a tongue
    baseTongue = true;

    // Whether the box should have a lid
    lid = true;
    // Lid height specified as number of layers. Each layer has the height of one plate.
    lidLayers = 1; // [1:24]
    // Whether the lid should have knobs
    lidKnobs = true;
    // Type of the lid knobs
    lidKnobType = "classic"; // [classic, technic]
    // Whether lid knobs should be centered.
    lidKnobCentered = false;
    // Whether lid should have pillars
    lidPillars = true;
    // Whether lid should be permanent (non removable)
    lidPermanent = true;

    /* [Quality] */

    // Quality of the preview in relation to the final rendering.
    previewQuality = 0.5; // [0.1:0.1:1]
    // Number of drawn fragments for roundings in the final rendering.
    roundingResolution = 64; // [16:8:128]

    /* [Calibration] */

    //Adjustment of the height (mm)
    baseHeightAdjustment = 0.0;
    //Adjustment of each side (mm)
    baseSideAdjustment = -0.1;
    //Diameter of the knobs (mm)
    knobSize = 5.1;
    //Thickness of the walls (mm)
    wallThickness = 1.5;
    //Diameter of the Z-Tubes (mm)
    tubeZSize = 6.3;

    block(
        grid=[boxSizeX, boxSizeY],
        baseLayers = boxLayers - (lid ? lidLayers : 0),
        baseCutoutType = baseCutoutType,

        knobs = baseKnobs,
        knobType = baseKnobType,
        knobCentered = baseKnobCentered,
        
        pit=true,
        pitWallGaps = basePitWallGaps, //boxType != "box" ? (boxType == "channel_corner" ? [ [ 0, 0, 0 ], [ 2, 0, 0 ] ] : [ [ 0, 0, 0 ], [ 1, 0, 0 ] ]) : [],
        pitWallThickness = basePitWallThickness,
        pitKnobs = basePitKnobs,
        pitKnobType = basePitKnobType,
        pitKnobCentered = basePitKnobCentered,

        tongue = baseTongue,
        tongueHeight = lidPermanent ? 2.0 : 1.8,
        tongueClampThickness = lidPermanent ? 0.1 : 0,
        tongueOuterAdjustment = lidPermanent ? 0.0 : -0.1,
        tongueRoundingRadius = lidPermanent ? 0.0 : 0.4,
        
        baseHeightAdjustment = baseHeightAdjustment,
        baseSideAdjustment = baseSideAdjustment,
        knobSize = knobSize,
        wallThickness = wallThickness,
        tubeZSize = tubeZSize
    );

    if(lid){
        translate(viewMode != "print" ? [0, 0, ((boxLayers - lidLayers) + (viewMode == "cover" ? 2*lidLayers : 0)) * 3.2] : [boxSizeX > boxSizeY ? 0 : (boxSizeX + 0.5) * 8.0, boxSizeX > boxSizeY ? -(boxSizeY + 0.5) * 8.0 : 0, 0])
            block(
                grid=[boxSizeX, boxSizeY],
                baseLayers = lidLayers,
                baseCutoutType = lidPermanent ? "groove" : "classic",

                knobs = lidKnobs,
                knobType = lidKnobType,
                knobCentered = lidKnobCentered,

                pillars = lidPillars,
                pitWallGaps = basePitWallGaps, //boxType != "box" ? (boxType == "channel_corner" ? [ [ 0, 0, 0 ], [ 2, 0, 0 ] ] : [ [ 0, 0, 0 ], [ 1, 0, 0 ] ]) : [],

                baseHeightAdjustment = baseHeightAdjustment,
                baseSideAdjustment = baseSideAdjustment,
                knobSize = knobSize,
                wallThickness = wallThickness,
                tubeZSize = tubeZSize
            );
    }
}

module lego_brick(position, shape_size, params) {
    translate([((shape_size[0]/2)+position[0])*8,((shape_size[1]/2)+position[1])*8,position[2]*3.2])brick(shape_size,params);
}

module brick(shape_size,params) {
    
    // Brick size in X-direction specified as multiple of an 1x1 brick.
    brickSizeX = shape_size[0]; // [1:32]  
    // Brick size in Y-direction specified as multiple of an 1x1 brick.
    brickSizeY = shape_size[1]; // [1:32]  
    // Height of brick specified as number of layers. Each layer has the height of one plate.
    baseLayers = shape_size[2]; // [1:24]

    /* [Appearance] */

    // Type of cut-out on the underside.
    baseCutoutType = params[2]; // [none, classic]
    // Whether to draw knobs.
    knobs = params[0];
    // Whether knobs should be centered.
    knobCentered = false;
    // Type of the knobs
    knobType = "classic"; // [classic, technic]

    // Whether to draw pillars.
    pillars = true;

    // Whether brick should have Technic holes along X-axis.
    holesX = false;
    // Whether brick should have Technic holes along Y-axis.
    holesY = false;
    // Whether brick should have Technic holes along Z-axis.
    holesZ = params[1];

    // Whether brick should have a pit
    pit = false;
    // Whether knobs should be drawn inside pit
    pitKnobs = false;
    // Pit wall thickness as multiple of one brick side length
    pitWallThickness = 0.333;

    // Slanting size on X0 side specified as multiple of an 1x1 brick.
    slantingX0 = 0;
    // Slanting size on X1 side specified as multiple of an 1x1 brick.
    slantingX1 = 0;
    // Slanting size on Y0 side specified as multiple of an 1x1 brick.
    slantingY0 = 0;
    // Slanting size on Y1 side specified as multiple of an 1x1 brick.
    slantingY1 = params[3];

    /* [Quality] */

    // Quality of the preview in relation to the final rendering.
    previewQuality = 0.5; // [0.1:0.1:1]
    // Number of drawn fragments for roundings in the final rendering.
    roundingResolution = 64; // [16:8:128]

    /* [Calibration] */

    // Adjustment of the height (mm)
    baseHeightAdjustment = 0.0;
    // Adjustment of each side (mm)
    baseSideAdjustment = -0.0;
    // Diameter of the knobs (mm)
    knobSize = 5.1;
    // Thickness of the walls (mm)
    wallThickness = 1.5;
    // Diameter of the Z-Tubes (mm)
    tubeZSize = 6.3;

    // Generate the block
    block(
        grid = [brickSizeX, brickSizeY],
        baseLayers = baseLayers,
        baseCutoutType = baseCutoutType,
        
        knobs = knobs,
        knobCentered = knobCentered,
        knobType = knobType,
        
        pillars = pillars,
        
        holesX = holesX,
        holesY = holesY,
        holesZ = holesZ,
        
        pit = pit,
        pitKnobs = pitKnobs,
        pitWallThickness = pitWallThickness,
        
        slanting = ((slantingX0 != 0) || (slantingX1 != 0) || (slantingY0 != 0) || (slantingY1 != 0)) ? [slantingX0, slantingX1, slantingY0, slantingY1] : false, 

        previewQuality = previewQuality,
        baseRoundingResolution = roundingResolution,
        holeRoundingResolution = roundingResolution,
        knobRoundingResolution = roundingResolution,
        pillarRoundingResolution = roundingResolution,

        baseHeightAdjustment = baseHeightAdjustment,
        baseSideAdjustment = baseSideAdjustment,
        knobSize = knobSize,
        wallThickness = wallThickness,
        tubeZSize = tubeZSize
    );
}
