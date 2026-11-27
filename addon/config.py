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
    "ARMOR_HELMET": {
        "label": "Helmet",
        "collections": (),
        "objects": ("Helmet",),
    },
    "ARMOR_CHESTPLATE": {
        "label": "Chestplate",
        "collections": (),
        "objects": ("Chestplate",),
    },
    "ARMOR_ARMS": {
        "label": "Arm Armor",
        "collections": (),
        "objects": ("Left Arm Armor", "Right Arm Armor"),
    },
    "ARMOR_LEGS": {
        "label": "Leg Armor",
        "collections": (),
        "objects": ("Left Leg Armor", "Right Leg Armor"),
    },
    "ARMOR_BOOTS": {
        "label": "Boots",
        "collections": (),
        "objects": ("Left Boot", "Right Boot"),
    },
    "ARMOR": {
        "label": "Armor",
        "collections": ("armor",),
        "objects": (),
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
