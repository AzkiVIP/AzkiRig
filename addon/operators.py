"""AzkiRIG operators."""

import os

import bpy
from bpy.props import EnumProperty, StringProperty
from bpy.types import Operator

from .config import TARGETS
from .utils import (
    capture_initial_visibility,
    materials_for_texture_slot,
    replace_material_images,
    restore_all_visibility,
    restore_target_visibility,
    toggle_target_visibility,
)


class AZKIRIG_OT_toggle_target(Operator):
    bl_idname = "azkirig.toggle_target"
    bl_label = "Toggle Rig Part"
    bl_options = {"REGISTER", "UNDO"}

    target: EnumProperty(
        name="Target",
        items=[
            (key, spec["label"], f"Toggle visibility for {spec['label']}")
            for key, spec in TARGETS.items()
        ],
    )

    def execute(self, context):
        visible, count = toggle_target_visibility(self.target)
        if visible is None:
            self.report({"WARNING"}, f"No objects or collections found for {self.target}")
            return {"CANCELLED"}

        action = "shown" if visible else "hidden"
        self.report({"INFO"}, f"{TARGETS[self.target]['label']} {action} ({count} datablocks)")
        return {"FINISHED"}


class AZKIRIG_OT_reset_target(Operator):
    bl_idname = "azkirig.reset_target"
    bl_label = "Reset Section"
    bl_options = {"REGISTER", "UNDO"}

    target: EnumProperty(
        name="Target",
        items=[
            (key, spec["label"], f"Restore initial visibility for {spec['label']}")
            for key, spec in TARGETS.items()
        ],
    )

    def execute(self, context):
        count = restore_target_visibility(self.target)
        if not count:
            self.report({"WARNING"}, "No initial visibility snapshot or matching datablocks found")
            return {"CANCELLED"}
        self.report({"INFO"}, f"Restored {TARGETS[self.target]['label']} visibility")
        return {"FINISHED"}


class AZKIRIG_OT_reset_all(Operator):
    bl_idname = "azkirig.reset_all"
    bl_label = "Reset All Visibility"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        count = restore_all_visibility()
        if not count:
            self.report({"WARNING"}, "No initial visibility snapshot was available")
            return {"CANCELLED"}
        self.report({"INFO"}, f"Restored visibility for {count} datablocks")
        return {"FINISHED"}


class AZKIRIG_OT_replace_texture(Operator):
    bl_idname = "azkirig.replace_texture"
    bl_label = "Replace Texture"
    bl_options = {"REGISTER", "UNDO"}

    filepath: StringProperty(subtype="FILE_PATH")
    filter_glob: StringProperty(default="*.png;*.jpg;*.jpeg;*.tif;*.tiff;*.exr", options={"HIDDEN"})
    slot: EnumProperty(
        name="Texture Slot",
        items=(
            ("SKIN", "Skin", "Replace the image nodes in the AzkiRig Skin material"),
            ("ARMOR_MAIN", "Armor Main", "Replace image nodes used by non-leg armor"),
            ("ARMOR_LEGGINGS", "Armor Leggings", "Replace image nodes used by leg armor"),
        ),
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        filepath = bpy.path.abspath(self.filepath)
        if not filepath or not os.path.isfile(filepath):
            self.report({"ERROR"}, "Choose a valid image file")
            return {"CANCELLED"}

        materials = materials_for_texture_slot(self.slot)
        if not materials:
            self.report({"WARNING"}, f"No compatible materials found for {self.slot}")
            return {"CANCELLED"}

        try:
            changed, image = replace_material_images(materials, filepath)
        except Exception as exc:
            self.report({"ERROR"}, f"Could not load or assign image: {exc}")
            return {"CANCELLED"}

        if not changed:
            self.report({"WARNING"}, "No Image Texture nodes were found in the target materials")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Replaced {changed} image node(s) with {image.name}")
        return {"FINISHED"}


CLASSES = (
    AZKIRIG_OT_toggle_target,
    AZKIRIG_OT_reset_target,
    AZKIRIG_OT_reset_all,
    AZKIRIG_OT_replace_texture,
)
