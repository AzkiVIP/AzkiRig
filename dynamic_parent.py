import bpy


def dp_get_rotation_mode(obj):
    if obj.rotation_mode in ("QUATERNION", "AXIS_ANGLE"):
        return obj.rotation_mode.lower()
    return "euler"


def dp_get_selected_objects(context):
    if context.mode not in ("OBJECT", "POSE"):
        return None
    if context.mode == "OBJECT":
        active = context.active_object
        selected = [obj for obj in context.selected_objects if obj != active]
        if active:
            selected.append(active)
        return selected
    if context.mode == "POSE":
        active = context.active_pose_bone
        selected = [bone for bone in context.selected_pose_bones if bone != active]
        if active:
            selected.append(active)
        return selected
    return None


def dp_get_last_constraint(obj):
    if not obj or not getattr(obj, "constraints", None):
        return None
    for const in reversed(obj.constraints):
        if const.name.startswith("DP_") and const.influence == 1:
            return const
    return None


def dp_get_active_dp_label(context):
    """Dapatkan informasi target Dynamic Parent aktif untuk tampilan UI."""
    obj = context.active_object
    if not obj:
        return "None (No Active Object)"

    if obj.type == "ARMATURE" and obj.mode == "POSE" and context.active_pose_bone:
        target_holder = context.active_pose_bone
    else:
        target_holder = obj

    if not target_holder or not getattr(target_holder, "constraints", None):
        return "No Active Link"

    for const in reversed(target_holder.constraints):
        if const.name.startswith("DP_"):
            status = "ON" if const.influence > 0.5 else "OFF"
            tgt = const.target.name if const.target else "None"
            sub = f" -> {const.subtarget}" if getattr(const, "subtarget", "") else ""
            return f"[{status}] {tgt}{sub}"
    return "No Active Link"


def dp_insert_keyframe(obj, frame):
    rot_mode = dp_get_rotation_mode(obj)
    for data_path in ("location", f"rotation_{rot_mode}", "scale"):
        obj.keyframe_insert(data_path=data_path, frame=frame)


def dp_insert_keyframe_constraint(constraint, frame):
    constraint.keyframe_insert(data_path="influence", frame=frame)


def dp_keyframe_insert_obj(obj):
    obj.keyframe_insert(data_path="location")
    if obj.rotation_mode == "QUATERNION":
        obj.keyframe_insert(data_path="rotation_quaternion")
    elif obj.rotation_mode == "AXIS_ANGLE":
        obj.keyframe_insert(data_path="rotation_axis_angle")
    else:
        obj.keyframe_insert(data_path="rotation_euler")
    obj.keyframe_insert(data_path="scale")


def dp_keyframe_insert_pbone(arm, pbone):
    dp_path = f'pose.bones["{pbone.name}"]'
    arm.keyframe_insert(data_path=f"{dp_path}.location")
    if pbone.rotation_mode == "QUATERNION":
        arm.keyframe_insert(data_path=f"{dp_path}.rotation_quaternion")
    elif pbone.rotation_mode == "AXIS_ANGLE":
        arm.keyframe_insert(data_path=f"{dp_path}.rotation_axis_angle")
    else:
        arm.keyframe_insert(data_path=f"{dp_path}.rotation_euler")
    arm.keyframe_insert(data_path=f"{dp_path}.scale")


def dp_disable_constraint(obj, const, frame):
    if isinstance(obj, bpy.types.PoseBone):
        matrix_final = obj.matrix.copy()
    else:
        matrix_final = obj.matrix_world.copy()

    dp_insert_keyframe(obj, frame=frame - 1)
    dp_insert_keyframe_constraint(const, frame=frame - 1)

    const.influence = 0
    if isinstance(obj, bpy.types.PoseBone):
        obj.matrix = matrix_final
    else:
        obj.matrix_world = matrix_final

    dp_insert_keyframe(obj, frame=frame)
    dp_insert_keyframe_constraint(const, frame=frame)


def dp_create_obj(context, op):
    obj = context.active_object
    scn = context.scene
    selected = [o for o in context.selected_objects if o != obj]

    if len(selected) != 1:
        op.report({"ERROR"}, "Select two objects (parent first, then active child).")
        return

    parent_obj = selected[0]
    dp_keyframe_insert_obj(obj)

    bpy.ops.object.constraint_add_with_targets(type="CHILD_OF")
    last_const = obj.constraints[-1]
    last_const.target = parent_obj

    if parent_obj.type == "ARMATURE" and parent_obj.data.bones.active:
        last_const.subtarget = parent_obj.data.bones.active.name
        last_const.name = f"DP_{parent_obj.name}.{last_const.subtarget}"
    else:
        last_const.name = f"DP_{parent_obj.name}"

    with context.temp_override(object=obj, active_object=obj, constraint=last_const):
        bpy.ops.constraint.childof_set_inverse(constraint=last_const.name, owner="OBJECT")

    cur = scn.frame_current
    scn.frame_current = cur - 1
    last_const.influence = 0
    obj.keyframe_insert(data_path=f'constraints["{last_const.name}"].influence')

    scn.frame_current = cur
    last_const.influence = 1
    obj.keyframe_insert(data_path=f'constraints["{last_const.name}"].influence')

    for ob in selected:
        ob.select_set(False)
    obj.select_set(True)


def dp_create_pbone(context, op):
    arm = context.active_object
    pbone = context.active_pose_bone
    scn = context.scene
    selected_objs = context.selected_objects

    if not pbone:
        op.report({"ERROR"}, "No active Pose Bone.")
        return

    parent_obj = None
    parent_pbone = None

    if len(selected_objs) == 2:
        others = [o for o in selected_objs if o != arm]
        parent_obj = others[0]
        if parent_obj.type == "ARMATURE":
            parent_pbone = parent_obj.data.bones.active
    elif len(selected_objs) == 1:
        parent_obj = arm
        selected_bones = [b for b in context.selected_pose_bones if b != pbone]
        if len(selected_bones) != 1:
            op.report({"ERROR"}, "Select one parent pose bone and one active child pose bone.")
            return
        parent_pbone = selected_bones[0]
    else:
        op.report({"ERROR"}, "Select two objects or two valid pose bones.")
        return

    dp_keyframe_insert_pbone(arm, pbone)
    bpy.ops.pose.constraint_add_with_targets(type="CHILD_OF")
    last_const = pbone.constraints[-1]
    last_const.target = parent_obj

    if parent_obj.type == "ARMATURE" and parent_pbone:
        last_const.subtarget = parent_pbone.name
        last_const.name = f"DP_{parent_obj.name}.{parent_pbone.name}"
    else:
        last_const.name = f"DP_{parent_obj.name}"

    with context.temp_override(object=arm, active_object=arm, constraint=last_const):
        bpy.ops.constraint.childof_set_inverse(constraint=last_const.name, owner="BONE")

    cur = scn.frame_current
    scn.frame_current = cur - 1
    last_const.influence = 0
    arm.keyframe_insert(
        data_path=f'pose.bones["{pbone.name}"].constraints["{last_const.name}"].influence'
    )

    scn.frame_current = cur
    last_const.influence = 1
    arm.keyframe_insert(
        data_path=f'pose.bones["{pbone.name}"].constraints["{last_const.name}"].influence'
    )


def dp_clear_data(obj, pbone):
    if obj and obj.animation_data and obj.animation_data.action:
        action = obj.animation_data.action
        dp_curves = [
            fc for fc in action.fcurves
            if "constraints" in fc.data_path and "DP_" in fc.data_path
        ]
        dp_keys = sorted({kp.co[0] for fc in dp_curves for kp in fc.keyframe_points})

        for fc in action.fcurves[:]:
            if fc.data_path.startswith("constraints") and "DP_" in fc.data_path:
                action.fcurves.remove(fc)
            else:
                for frame in dp_keys:
                    for kp in fc.keyframe_points[:]:
                        if kp.co[0] == frame:
                            fc.keyframe_points.remove(kp)
                if not fc.keyframe_points:
                    action.fcurves.remove(fc)

    target = pbone if pbone else obj
    if target and getattr(target, "constraints", None):
        for const in target.constraints[:]:
            if const.name.startswith("DP_"):
                target.constraints.remove(const)