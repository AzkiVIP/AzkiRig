"""AzkiRIG 3D View sidebar."""

import bpy
from bpy.types import Panel

from .config import TARGETS


class AZKIRIG_PT_main(Panel):
    bl_label = "AzkiRIG"
    bl_idname = "AZKIRIG_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AzkiRIG"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Visibility", icon="HIDE_OFF")
        for key in ("FACE", "EYES", "EYEBROWS", "MOUTH"):
            self._draw_target_row(layout, key)

        layout.separator()
        layout.label(text="Equipment", icon="OUTLINER_COLLECTION")
        for key in ("ARMOR", "CAPE", "ELYTRA"):
            self._draw_target_row(layout, key)

        layout.separator()
        layout.label(text="Arm Style", icon="ARMATURE_DATA")
        row = layout.row(align=True)
        self._draw_target_button(row, "WIDE_ARMS")
        self._draw_target_button(row, "SLIM_ARMS")

        layout.separator()
        layout.label(text="Texture Replacement", icon="TEXTURE")
        for slot, label in (
            ("SKIN", "Replace Skin"),
            ("ARMOR_MAIN", "Replace Armor Main"),
            ("ARMOR_LEGGINGS", "Replace Leggings"),
        ):
            op = layout.operator(
                "azkirig.replace_texture",
                text=label,
                icon="FILE_IMAGE",
            )
            op.slot = slot

        layout.separator()
        row = layout.row(align=True)
        row.operator("azkirig.reset_all", text="Reset All", icon="LOOP_BACK")

    @staticmethod
    def _draw_target_row(layout, key):
        row = layout.row(align=True)
        AZKIRIG_PT_main._draw_target_button(row, key)
        op = row.operator(
            "azkirig.reset_target",
            text="",
            icon="LOOP_BACK",
            emboss=True,
        )
        op.target = key

    @staticmethod
    def _draw_target_button(layout, key):
        op = layout.operator(
            "azkirig.toggle_target",
            text=TARGETS[key]["label"],
            icon="HIDE_OFF",
        )
        op.target = key


CLASSES = (AZKIRIG_PT_main,)
