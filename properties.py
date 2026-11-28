import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    PointerProperty,
)
from . import rig_utils


def armature_items_callback(self, context):
    items = []
    scn = getattr(context, "scene", None)
    if scn:
        for obj in scn.objects:
            if obj.type == "ARMATURE":
                items.append((obj.name, obj.name, f"Control settings for {obj.name}"))
    if not items:
        items.append(("NONE", "No Armature in Scene", "Add or select an armature"))
    return items


def on_change_active_armature(self, context):
    arm = rig_utils.get_selected_armature(context)
    if arm:
        context.view_layer.objects.active = arm


def on_update_skin(self, context):
    arm = rig_utils.get_owner_armature(self, context)
    rig_utils.apply_skin_texture(arm, self)


def on_update_face_vis(self, context):
    arm = rig_utils.get_owner_armature(self, context)
    rig_utils.apply_face_visibility(context, arm, self)


def on_update_accessories_vis(self, context):
    arm = rig_utils.get_owner_armature(self, context)
    rig_utils.apply_accessories_visibility(context, arm, self)


def on_update_armor_vis(self, context):
    arm = rig_utils.get_owner_armature(self, context)
    rig_utils.apply_armor_visibility(context, arm, self)


def on_update_armor_tex(self, context):
    arm = rig_utils.get_owner_armature(self, context)
    rig_utils.apply_armor_textures(arm, self)


def on_update_eyebrow(self, context):
    arm = rig_utils.get_owner_armature(self, context)
    rig_utils.apply_eyebrow_style(arm, self)


def on_update_eye_pupil(self, context):
    arm = rig_utils.get_owner_armature(self, context)
    rig_utils.apply_eye_pupil_style(arm, self)


def on_update_emission(self, context):
    arm = rig_utils.get_owner_armature(self, context)
    rig_utils.apply_emission(arm, self)


def on_update_arm_mode(self, context):
    arm = rig_utils.get_owner_armature(self, context)
    rig_utils.apply_arm_mode(context, arm, self)


class AZKIRIG_PG_scene_manager(bpy.types.PropertyGroup):
    active_armature_name: EnumProperty(
        name="Target Rig",
        description="Select which AzkiRig armature to control",
        items=armature_items_callback,
        update=on_change_active_armature,
    )


class AZKIRIG_PG_properties(bpy.types.PropertyGroup):
    # Collapsible sections
    exp_skin_arm: BoolProperty(name="Skin & Arm Mode", default=True)
    exp_face_vis: BoolProperty(name="Face Visibility", default=True)
    exp_eyebrow: BoolProperty(name="Eyebrow", default=True)
    exp_eye_pupil: BoolProperty(name="Eye & Pupil", default=True)
    exp_emission: BoolProperty(name="Eye / Pupil Emission", default=True)
    exp_accessories: BoolProperty(name="Cape & Elytra", default=True)
    exp_armor_vis: BoolProperty(name="Armor Visibility", default=True)
    exp_armor_tex: BoolProperty(name="Armor Textures", default=True)
    exp_dp: BoolProperty(name="Dynamic Parent", default=True)

    # 1. Skin texture
    skin_image: PointerProperty(name="Skin Image", type=bpy.types.Image, update=on_update_skin)

    # 17. Arm mode
    arm_mode: EnumProperty(
        name="Arm Mode",
        items=[
            ("WIDE", "Wide", "Wide arms mode"),
            ("SLIM", "Slim", "Slim arms mode"),
        ],
        default="WIDE",
        update=on_update_arm_mode,
    )

    # 2-5. Face visibility
    show_face: BoolProperty(name="Face", default=True, update=on_update_face_vis)
    show_eyebrow: BoolProperty(name="Eyebrow", default=True, update=on_update_face_vis)
    show_eye: BoolProperty(name="Eye", default=True, update=on_update_face_vis)
    show_mouth: BoolProperty(name="Mouth", default=True, update=on_update_face_vis)

    # 12-13. Eyebrow texture vs default & color
    eyebrow_mode: EnumProperty(
        name="Eyebrow Mode",
        items=[
            ("SKIN", "Skin Tex", "Use eyebrow texture from character skin"),
            ("COLOR", "Color", "Use a solid eyebrow color"),
            ("IMAGE", "Image", "Use a custom eyebrow image"),
        ],
        default="SKIN",
        update=on_update_eyebrow,
    )

    eyebrow_image: PointerProperty(
        name="Eyebrow Image",
        type=bpy.types.Image,
        update=on_update_eyebrow,
    )

    eyebrow_color: FloatVectorProperty(
        name="Eyebrow Color",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.112, 0.051, 0.026, 1.0),
        update=on_update_eyebrow,
    )

    # 14-15. Eye & Pupil (Default: Skin Texture; Color switches to eye/pupil material)
    eye_target: EnumProperty(
        name="Target",
        items=[
            ("EYE", "Eye", "Configure Eye"),
            ("PUPIL", "Pupil", "Configure Pupil"),
            ("BOTH", "Both", "Configure Eye & Pupil"),
        ],
        default="BOTH",
        update=on_update_eye_pupil,
    )
    eye_mode: EnumProperty(
        name="Eye Mode",
        items=[
            ("SKIN", "Skin Tex", "Use Skin image texture (eye-img)"),
            ("COLOR", "Color", "Use Eye color (eye)"),
            ("IMAGE", "Image", "Use custom Eye image texture (eye-img)"),
        ],
        default="SKIN",
        update=on_update_eye_pupil,
    )
    eye_image: PointerProperty(name="Eye Image", type=bpy.types.Image, update=on_update_eye_pupil)
    eye_color: FloatVectorProperty(
        name="Eye Color",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0),
        update=on_update_eye_pupil,
    )

    pupil_mode: EnumProperty(
        name="Pupil Mode",
        items=[
            ("SKIN", "Skin Tex", "Use Skin image texture (pupil-img)"),
            ("COLOR", "Color", "Use Pupil color (pupil)"),
            ("IMAGE", "Image", "Use custom Pupil image texture (pupil-img)"),
        ],
        default="SKIN",
        update=on_update_eye_pupil,
    )
    pupil_image: PointerProperty(name="Pupil Image", type=bpy.types.Image, update=on_update_eye_pupil)
    pupil_color: FloatVectorProperty(
        name="Pupil Color",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.084, 0.047, 0.25, 1.0),
        update=on_update_eye_pupil,
    )

    # 16. Emission on Eye / Pupil / Both + Custom Color Unlink/Relink
    emission_enabled: BoolProperty(name="Enable Emission", default=False, update=on_update_emission)
    emission_target: EnumProperty(
        name="Emission Target",
        items=[
            ("EYE", "Eye", "Emission on Eye"),
            ("PUPIL", "Pupil", "Emission on Pupil"),
            ("BOTH", "Both", "Emission on Eye & Pupil"),
        ],
        default="BOTH",
        update=on_update_emission,
    )
    emission_use_custom_color: BoolProperty(
        name="Custom Color (Unlink)",
        description="Unlink linked Image Texture from Emission Color to use custom color; toggle off to relink",
        default=False,
        update=on_update_emission,
    )
    emission_color: FloatVectorProperty(
        name="Emission Color",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0),
        update=on_update_emission,
    )
    emission_strength: FloatProperty(
        name="Strength",
        min=0.0,
        max=50.0,
        default=3.0,
        update=on_update_emission,
    )

    # 8-9. Cape & Elytra (default hidden)
    show_cape: BoolProperty(name="Cape", default=False, update=on_update_accessories_vis)
    show_elytra: BoolProperty(name="Elytra", default=False, update=on_update_accessories_vis)

    # 10. Armor visibility (default hidden)
    show_armor_all: BoolProperty(name="All Armor", default=False, update=on_update_armor_vis)
    show_armor_helmet: BoolProperty(name="Helmet", default=True, update=on_update_armor_vis)
    show_armor_chest: BoolProperty(name="Chestplate", default=True, update=on_update_armor_vis)
    show_armor_leggings: BoolProperty(name="Leggings", default=True, update=on_update_armor_vis)
    show_armor_boots: BoolProperty(name="Boots", default=True, update=on_update_armor_vis)

    show_part_hat_layer: BoolProperty(name="Hat Layer.001", default=True, update=on_update_armor_vis)
    show_part_helmet: BoolProperty(name="Helmet", default=True, update=on_update_armor_vis)
    show_part_chestplate: BoolProperty(name="Chestplate", default=True, update=on_update_armor_vis)
    show_part_left_arm_armor: BoolProperty(name="Left Arm Armor", default=True, update=on_update_armor_vis)
    show_part_right_arm_armor: BoolProperty(name="Right Arm Armor", default=True, update=on_update_armor_vis)
    show_part_belt: BoolProperty(name="Belt", default=True, update=on_update_armor_vis)
    show_part_left_leg_armor: BoolProperty(name="Left Leg Armor", default=True, update=on_update_armor_vis)
    show_part_right_leg_armor: BoolProperty(name="Right Leg Armor", default=True, update=on_update_armor_vis)
    show_part_left_boot: BoolProperty(name="Left Boot", default=True, update=on_update_armor_vis)
    show_part_right_boot: BoolProperty(name="Right Boot", default=True, update=on_update_armor_vis)

    # 11. Armor textures (Main & Leggings)
    armor_main_image: PointerProperty(name="Main Armor Image", type=bpy.types.Image, update=on_update_armor_tex)
    armor_leggings_image: PointerProperty(name="Leggings Image", type=bpy.types.Image, update=on_update_armor_tex)