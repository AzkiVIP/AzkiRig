"""AzkiRIG - Blender tools for the AzkiRig Minecraft character rig."""

bl_info = {
    "name": "AzkiRIG",
    "author": "AzkiVIP",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > AzkiRIG",
    "description": "Visibility and texture tools for AzkiRig",
    "category": "Rigging",
}

import bpy

from . import operators, ui
from .utils import capture_initial_visibility


def register():
    for cls in operators.CLASSES:
        bpy.utils.register_class(cls)
    for cls in ui.CLASSES:
        bpy.utils.register_class(cls)
    capture_initial_visibility()


def unregister():
    for cls in reversed(ui.CLASSES):
        bpy.utils.unregister_class(cls)
    for cls in reversed(operators.CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
