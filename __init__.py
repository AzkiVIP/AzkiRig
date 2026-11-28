bl_info = {
    "name": "AzkiRig Control Panel",
    "author": "AzkiVIP",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar (N) > AzkiRig & Shift+A",
    "description": "AzkiRIG is a Blender add-on designed to simplify the customization and management of Minecraft character rigs.(Visibility, Materials, Emission, Arm Mode, and Dynamic Parent)",
    "category": "Rigging",
}

import bpy
from bpy.props import PointerProperty

from . import (
    config,
    rig_utils,
    dynamic_parent,
    properties,
    operators,
    ui,
)


classes = (
    properties.AZKIRIG_PG_scene_manager,
    properties.AZKIRIG_PG_properties,
    operators.AZKIRIG_OT_add_rig,
    operators.AZKIRIG_OT_reset_section,
    operators.AZKIRIG_OT_reset_all,
    operators.AZKIRIG_OT_dp_create,
    operators.AZKIRIG_OT_dp_disable,
    operators.AZKIRIG_OT_dp_clear,
    operators.AZKIRIG_OT_dp_bake,
    ui.AZKIRIG_PT_main_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.azkirig_manager = PointerProperty(type=properties.AZKIRIG_PG_scene_manager)
    bpy.types.Object.azkirig = PointerProperty(type=properties.AZKIRIG_PG_properties)
    bpy.types.VIEW3D_MT_add.append(ui.draw_shift_a_menu)


def unregister():
    bpy.types.VIEW3D_MT_add.remove(ui.draw_shift_a_menu)
    del bpy.types.Object.azkirig
    del bpy.types.Scene.azkirig_manager
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()