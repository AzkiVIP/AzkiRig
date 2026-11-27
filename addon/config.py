"""Known AzkiRig datablock names.

These mappings are based on names found in the supplied AzkiRig Face file.
They are intentionally centralized so they can be adjusted after a full
Blender-side hierarchy and material audit.
"""

TARGETS = {
    "FACE": {
        "label": "Face",
        "collections": ("Face",),
        "objects": ("Head",),
    },
    "EYES": {
        "label": "Eyes",
        "collections": ("eye",),
        "objects": ("eye.L", "eye.R", "pupil.L", "pupil.L.001"),
    },
    "EYEBROWS": {
        "label": "Eyebrows",
        "collections": ("eyebrow",),
        "objects": ("eyebrow.L", "eyebrow.R"),
    },
    "MOUTH": {
        "label": "Mouth",
        "collections": (),
        "objects": ("mouth", "teeth"),
    },
    "ARMOR": {
        "label": "Armor",
        "collections": ("armor",),
        "objects": (
            "Helmet", "Chestplate",
            "Left Arm Armor", "Right Arm Armor",
            "Left Leg Armor", "Right Leg Armor",
            "Left Boot", "Right Boot",
        ),
    },
    "CAPE": {
        "label": "Cape",
        "collections": ("cape",),
        "objects": ("cape",),
    },
    "ELYTRA": {
        "label": "Elytra",
        "collections": ("elytra",),
        "objects": ("left_wing", "right_wing"),
    },
    "WIDE_ARMS": {
        "label": "Wide Arms",
        "collections": ("wide arms",),
        "objects": (
            "Wide Left Arm", "Wide Right Arm",
            "Wide Left Arm Layer", "Wide Right Arm Layer",
        ),
    },
    "SLIM_ARMS": {
        "label": "Slim Arms",
        "collections": ("slim arms",),
        "objects": (
            "Slim Left Arm", "Slim Right Arm",
            "Slim Left Arm Layer", "Slim Right Arm Layer",
        ),
    },
}

TEXTURE_SLOTS = {
    "SKIN": "AzkiRig Skin",
}
