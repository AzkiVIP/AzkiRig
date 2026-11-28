# =====================================================================
# CENTRALIZED NAME CONFIGURATION (MUDAH DIGANTI DI SATU TEMPAT)
# =====================================================================

CONFIG = {
    # Shift + A Rig Append Settings
    "rig_blend_filename": "AzkiRig.blend",
    "rig_append_object_name": "AzkiRig",
    "rig_append_collection_name": "AzkiRig",
    "shift_a_label": "AzkiRig",
    "wgts_collection_prefix": "WGTS_Armature",

    # Armature & Bone Collections
    "armature_name": "AzkiRig",
    "bone_col_face": ("face", "faces"),
    "bone_col_eyebrow": ("eyebrow",),
    "bone_col_eye": ("eye",),
    "bone_col_mouth": ("mouth",),
    "bone_col_cape": ("cape",),
    "bone_col_elytra": ("elytra",),
    "bone_col_wide_arms": ("wide arms", "Wide Arms"),
    "bone_col_slim_arms": ("slim arms", "Slim Arms"),

    # View Layer Collections (prefix match supports .001, .002 when multiple rigs exist)
    "vl_col_face": "Face",
    "vl_col_eyebrow": "eyebrow",
    "vl_col_eye": "eye",
    "vl_col_mouth": "mouth",
    "vl_col_cape": "cape",
    "vl_col_elytra": "elytra",
    "vl_col_armor": "armor",
    "vl_col_armor_helmet": "helmet",
    "vl_col_armor_chestplate": "chestplate",
    "vl_col_armor_leggings": "leggings",
    "vl_col_armor_boots": "boots",
    "vl_col_wide_arms": "wide arms",
    "vl_col_slim_arms": "slim arms",

    # Materials
    "mat_skin": "AzkiRig Skin",
    "mat_armor_main": "m_6157139d-3477-676f-7d76-b92c87d535dd.003",
    "mat_armor_leggings": "m_fdb9e998-052f-9998-e7ea-4db6a2c592c6.002",
    "mat_eyebrow": "eyebrow",
    "mat_eyebrow_img": "eyebrow-img",
    "mat_eye": "eye",
    "mat_eye_img": "eye-img",
    "mat_pupil": "pupil",
    "mat_pupil_img": "pupil-img",

    # Default Images
    "default_skin_image": "AzkiRig Skin.png",

    # Target Objects
    "objs_eyebrow": ("eyebrow.L", "eyebrow.R"),
    "objs_eye": ("eye.L", "eye.R"),
    "objs_pupil": ("pupil.L", "pupil.R"),
    "objs_wide_arms": (
        "Wide Left Arm",
        "Wide Left Arm Layer",
        "Wide Right Arm",
        "Wide Right Arm Layer",
    ),
    "objs_slim_arms": (
        "Slim Left Arm",
        "Slim Left Arm Layer",
        "Slim Right Arm",
        "Slim Right Arm Layer",
    ),
    "objs_armor_helmet": ("Hat Layer.001", "Helmet"),
    "objs_armor_chestplate": ("Chestplate", "Left Arm Armor", "Right Arm Armor"),
    "objs_armor_leggings": ("Belt", "Left Leg Armor", "Right Leg Armor"),
    "objs_armor_boots": ("Left Boot", "Right Boot"),
}

# Cache untuk menyimpan link asli Emission Color per material saat di-unlink
SAVED_EMISSION_LINKS = {}