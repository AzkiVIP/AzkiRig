import bpy
from .config import CONFIG
from . import rig_utils, dynamic_parent as dp


def draw_shift_a_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("azkirig.add_rig", text=CONFIG["shift_a_label"], icon="ARMATURE_DATA")


def draw_section_header(layout, props, exp_prop: str, title: str, icon: str, reset_section: str = None):
    box = layout.box()
    row = box.row(align=True)
    is_open = getattr(props, exp_prop)
    row.prop(
        props,
        exp_prop,
        text=title,
        icon="TRIA_DOWN" if is_open else "TRIA_RIGHT",
        emboss=False,
    )
    if reset_section:
        op = row.operator("azkirig.reset_section", text="", icon="FILE_REFRESH")
        op.section = reset_section
    return box, is_open


class AZKIRIG_PT_main_panel(bpy.types.Panel):
    bl_label = "AzkiRig"
    bl_idname = "AZKIRIG_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AzkiRig"

    def draw(self, context):
        layout = self.layout
        manager = context.scene.azkirig_manager
        arm = rig_utils.get_selected_armature(context)
        props = rig_utils.get_active_rig_props(context)

        # RIG SELECTOR (Armature Name Only) + RESET ALL AT TOP
        top_box = layout.box()
        row_sel = top_box.row(align=True)
        row_sel.label(text="", icon="ARMATURE_DATA")
        row_sel.prop(manager, "active_armature_name", text="")

        if not arm or not props:
            top_box.label(text="No Armature found in scene.", icon="INFO")
            return

        row_reset = top_box.row(align=True)
        row_reset.scale_y = 1.3
        row_reset.operator("azkirig.reset_all", text=f"Reset All ({arm.name})", icon="LOOP_BACK")

        # 1. SKIN & 17. ARM MODE
        box, is_open = draw_section_header(layout, props, "exp_skin_arm", "Skin & Arm Mode", "USER", "SKIN_ARM")
        if is_open:
            col = box.column(align=True)
            col.label(text="Skin Texture:")
            col.template_ID(props, "skin_image", open="image.open")
            col.separator()
            row = col.row(align=True)
            row.label(text="Arm Mode:")
            row.prop(props, "arm_mode", expand=True)

        # 2-5. FACE VISIBILITY
        box, is_open = draw_section_header(layout, props, "exp_face_vis", "Face Visibility", "HIDE_OFF", "FACE_VIS")
        if is_open:
            grid = box.grid_flow(row_major=True, columns=2, even_columns=True, align=True)
            grid.prop(props, "show_face", text="Face", toggle=True)
            grid.prop(props, "show_eyebrow", text="Eyebrow", toggle=True)
            grid.prop(props, "show_eye", text="Eye", toggle=True)
            grid.prop(props, "show_mouth", text="Mouth", toggle=True)

        # 12-13. EYEBROW
        box, is_open = draw_section_header(layout, props, "exp_eyebrow", "Eyebrow", "BRUSH_DATA", "EYEBROW")
        if is_open:
            col = box.column(align=True)
            col.prop(props, "eyebrow_mode", expand=True)
            if props.eyebrow_mode == "COLOR":
                col.prop(props, "eyebrow_color", text="Color")
            elif props.eyebrow_mode == "IMAGE":
                col.template_ID(props, "eyebrow_image", open="image.open")

        # 14-15. EYE & PUPIL
        box, is_open = draw_section_header(layout, props, "exp_eye_pupil", "Eye & Pupil", "HIDE_OFF", "EYE_PUPIL")
        if is_open:
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(props, "eye_target", expand=True)

            if props.eye_target in {"EYE", "BOTH"}:
                col.separator()
                col.label(text="Eye:")
                col.row(align=True).prop(props, "eye_mode", expand=True)
                if props.eye_mode == "IMAGE":
                    col.template_ID(props, "eye_image", open="image.open")
                elif props.eye_mode == "COLOR":
                    row = col.row(align=True)
                    row.label(text="Eye Color:")
                    row.prop(props, "eye_color", text="")

            if props.eye_target in {"PUPIL", "BOTH"}:
                col.separator()
                col.label(text="Pupil:")
                col.row(align=True).prop(props, "pupil_mode", expand=True)
                if props.pupil_mode == "IMAGE":
                    col.template_ID(props, "pupil_image", open="image.open")
                elif props.pupil_mode == "COLOR":
                    row = col.row(align=True)
                    row.label(text="Pupil Color:")
                    row.prop(props, "pupil_color", text="")

        # 16. EMISSION + CUSTOM COLOR UNLINK/RELINK
        box, is_open = draw_section_header(layout, props, "exp_emission", "Eye / Pupil Emission", "LIGHT_SUN", "EMISSION")
        if is_open:
            col = box.column(align=True)
            col.prop(props, "emission_enabled", text="Enable Emission", toggle=True)
            if props.emission_enabled:
                row = col.row(align=True)
                row.prop(props, "emission_target", expand=True)
                col.separator()
                col.prop(
                    props,
                    "emission_use_custom_color",
                    text="Custom Emission Color",
                    toggle=True,
                    icon="UNLINKED" if props.emission_use_custom_color else "LINKED",
                )
                row2 = col.row(align=True)
                if props.emission_use_custom_color:
                    row2.prop(props, "emission_color", text="")
                row2.prop(props, "emission_strength", text="Strength")

        # 8-9. CAPE & ELYTRA
        box, is_open = draw_section_header(layout, props, "exp_accessories", "Cape & Elytra", "MOD_CLOTH", "ACCESSORIES")
        if is_open:
            row = box.row(align=True)
            row.prop(props, "show_cape", text="Cape", toggle=True)
            row.prop(props, "show_elytra", text="Elytra", toggle=True)

        # 10. ARMOR VISIBILITY
        box, is_open = draw_section_header(layout, props, "exp_armor_vis", "Armor Visibility", "MOD_ARMATURE", "ARMOR_VIS")
        if is_open:
            col = box.column(align=True)
            col.prop(props, "show_armor_all", text="All Armor", toggle=True)

            sub_col = col.column(align=True)
            sub_col.enabled = props.show_armor_all

            grid_sub = sub_col.grid_flow(row_major=True, columns=2, even_columns=True, align=True)
            grid_sub.prop(props, "show_armor_helmet", text="Helmet", toggle=True)
            grid_sub.prop(props, "show_armor_chest", text="Chestplate", toggle=True)
            grid_sub.prop(props, "show_armor_leggings", text="Leggings", toggle=True)
            grid_sub.prop(props, "show_armor_boots", text="Boots", toggle=True)

            sub_col.separator()
            sub_col.label(text="Armor Parts:")
            grid_parts = sub_col.grid_flow(row_major=True, columns=2, even_columns=True, align=True)
            grid_parts.prop(props, "show_part_hat_layer", text="Hat Layer.001", toggle=True)
            grid_parts.prop(props, "show_part_helmet", text="Helmet", toggle=True)
            grid_parts.prop(props, "show_part_chestplate", text="Chestplate", toggle=True)
            grid_parts.prop(props, "show_part_left_arm_armor", text="Left Arm Armor", toggle=True)
            grid_parts.prop(props, "show_part_right_arm_armor", text="Right Arm Armor", toggle=True)
            grid_parts.prop(props, "show_part_belt", text="Belt", toggle=True)
            grid_parts.prop(props, "show_part_left_leg_armor", text="Left Leg Armor", toggle=True)
            grid_parts.prop(props, "show_part_right_leg_armor", text="Right Leg Armor", toggle=True)
            grid_parts.prop(props, "show_part_left_boot", text="Left Boot", toggle=True)
            grid_parts.prop(props, "show_part_right_boot", text="Right Boot", toggle=True)

        # 11. ARMOR TEXTURES
        box, is_open = draw_section_header(layout, props, "exp_armor_tex", "Armor Textures", "TEXTURE", "ARMOR_TEX")
        if is_open:
            col = box.column(align=True)
            col.label(text="Main Armor:")
            col.template_ID(props, "armor_main_image", open="image.open")
            col.separator()
            col.label(text="Leggings:")
            col.template_ID(props, "armor_leggings_image", open="image.open")

        # 18. DYNAMIC PARENT
        box, is_open = draw_section_header(layout, props, "exp_dp", "Dynamic Parent", "CON_CHILDOF")
        if is_open:
            col = box.column(align=True)

            status_box = col.box()
            status_row = status_box.row(align=True)
            status_row.label(text=dp.dp_get_active_dp_label(context), icon="LINKED")

            col.separator(factor=0.6)

            row_main = col.row(align=True)
            row_main.scale_y = 1.2
            row_main.operator("azkirig.dp_create", text="Bind", icon="CONSTRAINT_BONE")
            row_main.operator("azkirig.dp_disable", text="Release", icon="UNLINKED")

            col.separator(factor=0.4)

            row_sub = col.row(align=True)
            row_sub.operator("azkirig.dp_bake", text="Bake Keys", icon="KEYFRAME_HLT")
            row_sub.operator("azkirig.dp_clear", text="Clear All", icon="TRASH")