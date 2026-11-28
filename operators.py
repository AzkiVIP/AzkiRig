import os
import bpy
from bpy.props import StringProperty
from .config import CONFIG
from . import rig_utils, dynamic_parent as dp


class AZKIRIG_OT_add_rig(bpy.types.Operator):
    """Append AzkiRig Face from root blend file and apply initial settings"""
    bl_idname = "azkirig.add_rig"
    bl_label = CONFIG["shift_a_label"]
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        filepath = rig_utils.get_rig_blend_path()
        if not os.path.isfile(filepath):
            self.report({"ERROR"}, f"Rig blend file not found: {filepath}")
            return {"CANCELLED"}

        col_name = CONFIG["rig_append_collection_name"]
        obj_name = CONFIG["rig_append_object_name"]

        with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
            if col_name and col_name in data_from.collections:
                data_to.collections = [col_name]
            elif obj_name and obj_name in data_from.objects:
                data_to.objects = [obj_name]
            else:
                self.report({"ERROR"}, "Target collection or object not found in rig file.")
                return {"CANCELLED"}

        added_arm = None
        for col in data_to.collections:
            if col:
                context.scene.collection.children.link(col)
                for ob in col.all_objects:
                    if ob.type == "ARMATURE":
                        added_arm = ob

        for ob in data_to.objects:
            if ob and ob.name not in context.scene.objects:
                context.scene.collection.objects.link(ob)
                if ob.type == "ARMATURE":
                    added_arm = ob

        rig_utils.hide_wgts_collections(context, added_arm)

        if added_arm:
            added_arm.location = context.scene.cursor.location
            context.view_layer.objects.active = added_arm
            added_arm.select_set(True)
            context.scene.azkirig_manager.active_armature_name = added_arm.name
            rig_utils.apply_all_settings_to_rig(context, added_arm, added_arm.azkirig)

        self.report({"INFO"}, f"Added {CONFIG['shift_a_label']} and applied rig settings.")
        return {"FINISHED"}


class AZKIRIG_OT_reset_section(bpy.types.Operator):
    """Reset settings for this section"""
    bl_idname = "azkirig.reset_section"
    bl_label = "Reset Section"
    bl_options = {"REGISTER", "UNDO"}

    section: StringProperty()

    def execute(self, context):
        arm = rig_utils.get_selected_armature(context)
        props = rig_utils.get_active_rig_props(context)
        if not arm or not props:
            self.report({"ERROR"}, "No target armature selected.")
            return {"CANCELLED"}

        if self.section == "SKIN_ARM":
            props.skin_image = None
            props.arm_mode = "WIDE"
            rig_utils.apply_arm_mode(context, arm, props)
        elif self.section == "FACE_VIS":
            props.show_face = True
            props.show_eyebrow = True
            props.show_eye = True
            props.show_mouth = True
            rig_utils.apply_face_visibility(context, arm, props)
        elif self.section == "EYEBROW":
            props.eyebrow_use_image = False
            props.eyebrow_image = None
            props.eyebrow_color = (0.112, 0.051, 0.026, 1.0)
            rig_utils.apply_eyebrow_style(arm, props)
        elif self.section == "EYE_PUPIL":
            props.eye_target = "BOTH"
            props.eye_mode = "SKIN"
            props.eye_image = None
            props.eye_color = (1.0, 1.0, 1.0, 1.0)
            props.pupil_mode = "SKIN"
            props.pupil_image = None
            props.pupil_color = (0.084, 0.047, 0.25, 1.0)
            rig_utils.apply_eye_pupil_style(arm, props)
        elif self.section == "EMISSION":
            props.emission_enabled = False
            props.emission_target = "BOTH"
            props.emission_use_custom_color = False
            props.emission_color = (1.0, 1.0, 1.0, 1.0)
            props.emission_strength = 3.0
            rig_utils.apply_emission(arm, props)
        elif self.section == "ACCESSORIES":
            props.show_cape = False
            props.show_elytra = False
            rig_utils.apply_accessories_visibility(context, arm, props)
        elif self.section == "ARMOR_VIS":
            props.show_armor_all = False
            props.show_armor_helmet = True
            props.show_armor_chest = True
            props.show_armor_leggings = True
            props.show_armor_boots = True
            props.show_part_hat_layer = True
            props.show_part_helmet = True
            props.show_part_chestplate = True
            props.show_part_left_arm_armor = True
            props.show_part_right_arm_armor = True
            props.show_part_belt = True
            props.show_part_left_leg_armor = True
            props.show_part_right_leg_armor = True
            props.show_part_left_boot = True
            props.show_part_right_boot = True
            rig_utils.apply_armor_visibility(context, arm, props)
        elif self.section == "ARMOR_TEX":
            props.armor_main_image = None
            props.armor_leggings_image = None

        self.report({"INFO"}, f"Reset section '{self.section}' for {arm.name}.")
        return {"FINISHED"}


class AZKIRIG_OT_reset_all(bpy.types.Operator):
    """Reset all settings for the selected armature"""
    bl_idname = "azkirig.reset_all"
    bl_label = "Reset All"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        arm = rig_utils.get_selected_armature(context)
        props = rig_utils.get_active_rig_props(context)
        if not arm or not props:
            self.report({"ERROR"}, "No target armature selected.")
            return {"CANCELLED"}

        props.skin_image = None
        props.arm_mode = "WIDE"

        props.show_face = True
        props.show_eyebrow = True
        props.show_eye = True
        props.show_mouth = True

        props.eyebrow_use_image = False
        props.eyebrow_image = None
        props.eyebrow_color = (0.112, 0.051, 0.026, 1.0)

        props.eye_target = "BOTH"
        props.eye_mode = "SKIN"
        props.eye_image = None
        props.eye_color = (1.0, 1.0, 1.0, 1.0)
        props.pupil_mode = "SKIN"
        props.pupil_image = None
        props.pupil_color = (0.084, 0.047, 0.25, 1.0)

        props.emission_enabled = False
        props.emission_target = "BOTH"
        props.emission_use_custom_color = False
        props.emission_color = (1.0, 1.0, 1.0, 1.0)
        props.emission_strength = 3.0

        props.show_cape = False
        props.show_elytra = False

        props.show_armor_all = False
        props.show_armor_helmet = True
        props.show_armor_chest = True
        props.show_armor_leggings = True
        props.show_armor_boots = True

        props.show_part_hat_layer = True
        props.show_part_helmet = True
        props.show_part_chestplate = True
        props.show_part_left_arm_armor = True
        props.show_part_right_arm_armor = True
        props.show_part_belt = True
        props.show_part_left_leg_armor = True
        props.show_part_right_leg_armor = True
        props.show_part_left_boot = True
        props.show_part_right_boot = True

        props.armor_main_image = None
        props.armor_leggings_image = None

        rig_utils.apply_all_settings_to_rig(context, arm, props)

        self.report({"INFO"}, f"All settings for {arm.name} have been reset.")
        return {"FINISHED"}


class AZKIRIG_OT_dp_create(bpy.types.Operator):
    """Bind active object or pose bone to parent with animated Child Of"""
    bl_idname = "azkirig.dp_create"
    bl_label = "Bind Parent"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        frame = context.scene.frame_current
        if not obj:
            self.report({"ERROR"}, "No active object.")
            return {"CANCELLED"}

        if obj.type == "ARMATURE":
            if obj.mode != "POSE":
                self.report({"ERROR"}, "Armature objects must be in Pose mode.")
                return {"CANCELLED"}
            pbone = context.active_pose_bone
            const = dp.dp_get_last_constraint(pbone)
            if const:
                dp.dp_disable_constraint(pbone, const, frame)
            dp.dp_create_pbone(context, self)
        else:
            const = dp.dp_get_last_constraint(obj)
            if const:
                dp.dp_disable_constraint(obj, const, frame)
            dp.dp_create_obj(context, self)

        return {"FINISHED"}


class AZKIRIG_OT_dp_disable(bpy.types.Operator):
    """Release active Dynamic Parent link at current frame"""
    bl_idname = "azkirig.dp_disable"
    bl_label = "Release Parent"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode in {"OBJECT", "POSE"}

    def execute(self, context):
        frame = context.scene.frame_current
        targets = dp.dp_get_selected_objects(context)
        if not targets:
            self.report({"ERROR"}, "Nothing selected.")
            return {"CANCELLED"}

        counter = 0
        for item in targets:
            const = dp.dp_get_last_constraint(item)
            if const is None:
                continue
            dp.dp_disable_constraint(item, const, frame)
            counter += 1

        self.report({"INFO"}, f"Released {counter} Dynamic Parent link(s).")
        return {"FINISHED"}


class AZKIRIG_OT_dp_clear(bpy.types.Operator):
    """Remove all Dynamic Parent constraints and keyframes"""
    bl_idname = "azkirig.dp_clear"
    bl_label = "Clear Links"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj:
            return {"CANCELLED"}
        pbone = context.active_pose_bone if obj.type == "ARMATURE" else None
        dp.dp_clear_data(obj, pbone)
        self.report({"INFO"}, "Dynamic Parent links cleared.")
        return {"FINISHED"}


class AZKIRIG_OT_dp_bake(bpy.types.Operator):
    """Bake Dynamic Parent motion into keyframes and remove constraints"""
    bl_idname = "azkirig.dp_bake"
    bl_label = "Bake Keys"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        scn = context.scene
        if not obj:
            return {"CANCELLED"}

        if obj.type == "ARMATURE":
            pbone = context.active_pose_bone
            bpy.ops.nla.bake(
                frame_start=scn.frame_start,
                frame_end=scn.frame_end,
                step=1,
                only_selected=True,
                visual_keying=True,
                clear_constraints=False,
                clear_parents=False,
                bake_types={"POSE"},
            )
            if pbone:
                for const in pbone.constraints[:]:
                    if const.name.startswith("DP_"):
                        pbone.constraints.remove(const)
        else:
            bpy.ops.nla.bake(
                frame_start=scn.frame_start,
                frame_end=scn.frame_end,
                step=1,
                only_selected=True,
                visual_keying=True,
                clear_constraints=False,
                clear_parents=False,
                bake_types={"OBJECT"},
            )
            for const in obj.constraints[:]:
                if const.name.startswith("DP_"):
                    obj.constraints.remove(const)

        self.report({"INFO"}, "Dynamic Parent motion baked and cleared.")
        return {"FINISHED"}