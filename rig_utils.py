import os
import bpy
from .config import CONFIG, SAVED_EMISSION_LINKS


# =====================================================================
# MULTI-RIG CONTEXT & PER-ARMATURE STORAGE HELPERS
# =====================================================================

def get_selected_armature(context):
    """Ambil Armature yang sedang dipilih di dropdown panel."""
    scn = getattr(context, "scene", None)
    if not scn or not hasattr(scn, "azkirig_manager"):
        return None
    arm_name = scn.azkirig_manager.active_armature_name
    if arm_name and arm_name != "NONE":
        obj = bpy.data.objects.get(arm_name)
        if obj and obj.type == "ARMATURE":
            return obj
    for obj in scn.objects:
        if obj.type == "ARMATURE":
            return obj
    return None


def get_active_rig_props(context):
    """Ambil PropertyGroup azkirig yang tersimpan pada Object Armature aktif."""
    arm = get_selected_armature(context)
    if arm and hasattr(arm, "azkirig"):
        return arm.azkirig
    return None


def get_owner_armature(prop_group, context):
    if isinstance(prop_group.id_data, bpy.types.Object) and prop_group.id_data.type == "ARMATURE":
        return prop_group.id_data
    return get_selected_armature(context)


def get_rig_blend_path() -> str:
    """Cari file rig di dalam folder addon terlebih dahulu, lalu fallback ke folder blend."""
    addon_dir = os.path.dirname(os.path.abspath(__file__))
    subpath = CONFIG["rig_blend_filename"]
    addon_rig_path = os.path.join(addon_dir, subpath)

    if os.path.isfile(addon_rig_path):
        return addon_rig_path


# =====================================================================
# COLLECTION, OBJECT & MATERIAL RESOLUTION (PER-RIG AWARE)
# =====================================================================

def get_rig_root_collection(arm):
    """Cari parent collection utama tempat armature ini berada."""
    if not arm:
        return None
    for col in arm.users_collection:
        if col.name.startswith(CONFIG["rig_append_collection_name"]):
            return col
    for parent_col in bpy.data.collections:
        if parent_col.name.startswith(CONFIG["rig_append_collection_name"]):
            if arm.name in parent_col.all_objects:
                return parent_col
    return None


def find_layer_collection_in_scope(layer_col, target_base_name: str):
    """Cari LayerCollection berdasarkan nama exact atau prefix '.00x'."""
    if not layer_col:
        return None
    if layer_col.name == target_base_name or layer_col.name.startswith(target_base_name + "."):
        return layer_col
    for child in layer_col.children:
        found = find_layer_collection_in_scope(child, target_base_name)
        if found:
            return found
    return None


def set_vl_checkbox_exclude(context, arm, col_base_name: str, exclude: bool):
    """Uncheck/check View Layer collection checkbox untuk rig spesifik."""
    if not col_base_name:
        return False
    view_layer = context.view_layer
    root_col = get_rig_root_collection(arm)

    search_root = view_layer.layer_collection
    if root_col:
        scoped_lc = find_layer_collection_in_scope(view_layer.layer_collection, root_col.name)
        if scoped_lc:
            search_root = scoped_lc

    lc = find_layer_collection_in_scope(search_root, col_base_name)
    if not lc:
        lc = find_layer_collection_in_scope(view_layer.layer_collection, col_base_name)
    if lc:
        lc.exclude = bool(exclude)
        return True
    return False


def hide_wgts_collections(context, arm=None):
    """Sembunyikan semua collection WGTS_Armature di View Layer."""
    def _walk(lc):
        if lc.name == CONFIG["wgts_collection_prefix"] or lc.name.startswith(CONFIG["wgts_collection_prefix"] + "."):
            lc.exclude = True
            if lc.collection:
                lc.collection.hide_viewport = True
                lc.collection.hide_render = True
        for ch in lc.children:
            _walk(ch)

    _walk(context.view_layer.layer_collection)


def find_bone_collection_recursive(bcol, target_name: str):
    if not bcol:
        return None
    if bcol.name == target_name:
        return bcol
    for child in bcol.children:
        found = find_bone_collection_recursive(child, target_name)
        if found:
            return found
    return None


def set_bone_collection_visible(arm, col_names, visible: bool):
    if not arm or arm.type != "ARMATURE" or not hasattr(arm.data, "collections"):
        return False
    if isinstance(col_names, str):
        col_names = (col_names,)

    matched = False
    for name in col_names:
        for top in arm.data.collections:
            bcol = find_bone_collection_recursive(top, name)
            if bcol:
                bcol.is_visible = bool(visible)
                matched = True
    return matched


def find_rig_objects_by_base_name(arm, base_name: str):
    """Temukan objek milik armature tertentu berdasarkan nama dasar."""
    results = []
    root_col = get_rig_root_collection(arm)
    candidates = root_col.all_objects if root_col else bpy.data.objects

    for obj in candidates:
        if obj.name == base_name or obj.name.startswith(base_name + "."):
            if (
                arm is None
                or obj.parent == arm
                or any(m.type == "ARMATURE" and m.object == arm for m in obj.modifiers)
                or root_col is not None
            ):
                results.append(obj)
    return results


def set_rig_object_hidden(arm, base_name: str, hide: bool):
    objs = find_rig_objects_by_base_name(arm, base_name)
    if not objs:
        return False
    for obj in objs:
        obj.hide_viewport = bool(hide)
        obj.hide_render = bool(hide)
        if obj.name in bpy.context.view_layer.objects:
            obj.hide_set(bool(hide))
    return True


def resolve_rig_material(arm, base_mat_name: str):
    """Ambil material bawaan milik rig tertentu."""

    root_col = get_rig_root_collection(arm)
    if root_col:
        for obj in root_col.all_objects:
            for slot in obj.material_slots:
                mat = slot.material
                if mat and (mat.name == base_mat_name or mat.name.startswith(base_mat_name + ".")):
                    return mat

    return bpy.data.materials.get(base_mat_name)


def assign_material_to_rig_objects(arm, base_names, mat):
    if not mat:
        return
    for base_name in base_names:
        for obj in find_rig_objects_by_base_name(arm, base_name):
            if not hasattr(obj, "data") or not hasattr(obj.data, "materials"):
                continue
            if len(obj.data.materials) == 0:
                obj.data.materials.append(mat)
            else:
                obj.data.materials[0] = mat


def find_image_node(mat):
    if not mat or not mat.use_nodes or not mat.node_tree:
        return None
    for node in mat.node_tree.nodes:
        if node.type == "TEX_IMAGE":
            return node
    return None


def find_rgb_node(mat):
    if not mat or not mat.use_nodes or not mat.node_tree:
        return None
    for node in mat.node_tree.nodes:
        if node.type == "RGB":
            return node
    return None


def get_skin_image(arm, props):
    if props.skin_image:
        return props.skin_image
    skin_mat = resolve_rig_material(arm, CONFIG["mat_skin"])
    skin_node = find_image_node(skin_mat)
    if skin_node and skin_node.image:
        return skin_node.image
    return bpy.data.images.get(CONFIG["default_skin_image"])


def set_emission_settings(
    mat,
    is_image_mode: bool,
    enabled: bool,
    strength: float,
    use_custom_color: bool,
    custom_color,
):
    """Atur Emission Strength & unlink/relink Emission Color sesuai mode & Custom Color."""
    if not mat or not mat.use_nodes or not mat.node_tree:
        return

    tree = mat.node_tree
    links = tree.links

    for node in tree.nodes:
        if node.type == "BSDF_PRINCIPLED":
            if "Emission Strength" in node.inputs:
                node.inputs["Emission Strength"].default_value = float(strength) if enabled else 0.0

            if "Emission Color" in node.inputs:
                inp_col = node.inputs["Emission Color"]
                key = (mat.name, node.name)

                if use_custom_color:
                    if inp_col.is_linked:
                        for link in list(inp_col.links):
                            if not is_image_mode or link.from_node.type == "TEX_IMAGE" or key not in SAVED_EMISSION_LINKS:
                                SAVED_EMISSION_LINKS[key] = (
                                    link.from_node.name,
                                    link.from_socket.name,
                                )
                            links.remove(link)
                    inp_col.default_value = tuple(custom_color)
                else:
                    if not inp_col.is_linked:
                        saved = SAVED_EMISSION_LINKS.get(key)
                        if saved:
                            from_node = tree.nodes.get(saved[0])
                            if from_node and saved[1] in from_node.outputs:
                                links.new(from_node.outputs[saved[1]], inp_col)
                        elif is_image_mode:
                            img_node = find_image_node(mat)
                            if img_node and "Color" in img_node.outputs:
                                links.new(img_node.outputs["Color"], inp_col)

        elif node.type == "EMISSION":
            if "Strength" in node.inputs:
                node.inputs["Strength"].default_value = float(strength) if enabled else 0.0
            if "Color" in node.inputs:
                inp_col = node.inputs["Color"]
                key = (mat.name, node.name)
                if use_custom_color:
                    if inp_col.is_linked:
                        for link in list(inp_col.links):
                            if not is_image_mode or link.from_node.type == "TEX_IMAGE" or key not in SAVED_EMISSION_LINKS:
                                SAVED_EMISSION_LINKS[key] = (
                                    link.from_node.name,
                                    link.from_socket.name,
                                )
                            links.remove(link)
                    inp_col.default_value = tuple(custom_color)
                else:
                    if not inp_col.is_linked:
                        saved = SAVED_EMISSION_LINKS.get(key)
                        if saved:
                            from_node = tree.nodes.get(saved[0])
                            if from_node and saved[1] in from_node.outputs:
                                links.new(from_node.outputs[saved[1]], inp_col)
                        elif is_image_mode:
                            img_node = find_image_node(mat)
                            if img_node and "Color" in img_node.outputs:
                                links.new(img_node.outputs["Color"], inp_col)


# =====================================================================
# FEATURE APPLY FUNCTIONS
# =====================================================================

def apply_skin_texture(arm, props):
    mat = resolve_rig_material(arm, CONFIG["mat_skin"])
    if mat and props.skin_image:
        img_node = find_image_node(mat)
        if img_node:
            img_node.image = props.skin_image
    apply_eye_pupil_style(arm, props)


def apply_face_visibility(context, arm, props):
    set_vl_checkbox_exclude(context, arm, CONFIG["vl_col_face"], not props.show_face)
    set_bone_collection_visible(arm, CONFIG["bone_col_face"], props.show_face)

    set_vl_checkbox_exclude(context, arm, CONFIG["vl_col_eyebrow"], not props.show_eyebrow)
    set_bone_collection_visible(arm, CONFIG["bone_col_eyebrow"], props.show_eyebrow)

    set_vl_checkbox_exclude(context, arm, CONFIG["vl_col_eye"], not props.show_eye)
    set_bone_collection_visible(arm, CONFIG["bone_col_eye"], props.show_eye)

    set_vl_checkbox_exclude(context, arm, CONFIG["vl_col_mouth"], not props.show_mouth)
    set_bone_collection_visible(arm, CONFIG["bone_col_mouth"], props.show_mouth)


def apply_accessories_visibility(context, arm, props):
    set_vl_checkbox_exclude(context, arm, CONFIG["vl_col_cape"], not props.show_cape)
    set_bone_collection_visible(arm, CONFIG["bone_col_cape"], props.show_cape)

    set_vl_checkbox_exclude(context, arm, CONFIG["vl_col_elytra"], not props.show_elytra)
    set_bone_collection_visible(arm, CONFIG["bone_col_elytra"], props.show_elytra)


def apply_armor_visibility(context, arm, props):
    set_vl_checkbox_exclude(context, arm, CONFIG["vl_col_armor"], not props.show_armor_all)

    if props.show_armor_all:
        set_vl_checkbox_exclude(context, arm, CONFIG["vl_col_armor_helmet"], not props.show_armor_helmet)
        set_vl_checkbox_exclude(context, arm, CONFIG["vl_col_armor_chestplate"], not props.show_armor_chest)
        set_vl_checkbox_exclude(context, arm, CONFIG["vl_col_armor_leggings"], not props.show_armor_leggings)
        set_vl_checkbox_exclude(context, arm, CONFIG["vl_col_armor_boots"], not props.show_armor_boots)

        helmet_on = props.show_armor_helmet
        set_rig_object_hidden(arm, "Hat Layer.001", not (helmet_on and props.show_part_hat_layer))
        set_rig_object_hidden(arm, "Helmet", not (helmet_on and props.show_part_helmet))

        chest_on = props.show_armor_chest
        set_rig_object_hidden(arm, "Chestplate", not (chest_on and props.show_part_chestplate))
        set_rig_object_hidden(arm, "Left Arm Armor", not (chest_on and props.show_part_left_arm_armor))
        set_rig_object_hidden(arm, "Right Arm Armor", not (chest_on and props.show_part_right_arm_armor))

        leg_on = props.show_armor_leggings
        set_rig_object_hidden(arm, "Belt", not (leg_on and props.show_part_belt))
        set_rig_object_hidden(arm, "Left Leg Armor", not (leg_on and props.show_part_left_leg_armor))
        set_rig_object_hidden(arm, "Right Leg Armor", not (leg_on and props.show_part_right_leg_armor))

        boot_on = props.show_armor_boots
        set_rig_object_hidden(arm, "Left Boot", not (boot_on and props.show_part_left_boot))
        set_rig_object_hidden(arm, "Right Boot", not (boot_on and props.show_part_right_boot))


def apply_armor_textures(arm, props):
    main_mat = resolve_rig_material(arm, CONFIG["mat_armor_main"])
    if main_mat and props.armor_main_image:
        img_node = find_image_node(main_mat)
        if img_node:
            img_node.image = props.armor_main_image

    leg_mat = resolve_rig_material(arm, CONFIG["mat_armor_leggings"])
    if leg_mat and props.armor_leggings_image:
        img_node = find_image_node(leg_mat)
        if img_node:
            img_node.image = props.armor_leggings_image


def apply_eyebrow_style(arm, props):
    mat_default = resolve_rig_material(
        arm, CONFIG["mat_eyebrow"]
    )
    mat_img = resolve_rig_material(
        arm, CONFIG["mat_eyebrow_img"]
    )

    if props.eyebrow_mode == "SKIN":
        target_mat = mat_img or mat_default
        assign_material_to_rig_objects(
            arm, CONFIG["objs_eyebrow"], target_mat
        )

    elif props.eyebrow_mode == "COLOR":
        target_mat = mat_default or mat_img
        assign_material_to_rig_objects(
            arm, CONFIG["objs_eyebrow"], target_mat
        )

        if target_mat:
            rgb_node = find_rgb_node(target_mat)
            if rgb_node:
                rgb_node.outputs["Color"].default_value = tuple(
                    props.eyebrow_color
                )

    elif props.eyebrow_mode == "IMAGE":
        target_mat = mat_img or mat_default
        assign_material_to_rig_objects(
            arm, CONFIG["objs_eyebrow"], target_mat
        )

        if target_mat and props.eyebrow_image:
            img_node = find_image_node(target_mat)
            if img_node:
                img_node.image = props.eyebrow_image


def _apply_single_eye_or_pupil(arm, props, is_pupil: bool):
    if not is_pupil:
        mode = props.eye_mode
        custom_img = props.eye_image
        color_val = props.eye_color
        objs = CONFIG["objs_eye"]
        default_mat = resolve_rig_material(arm, CONFIG["mat_eye"])
        img_mat = resolve_rig_material(arm, CONFIG["mat_eye_img"])
    else:
        mode = props.pupil_mode
        custom_img = props.pupil_image
        color_val = props.pupil_color
        objs = CONFIG["objs_pupil"]
        default_mat = resolve_rig_material(arm, CONFIG["mat_pupil"])
        img_mat = resolve_rig_material(arm, CONFIG["mat_pupil_img"])

    if mode == "SKIN":
        active_mat = img_mat or default_mat
        assign_material_to_rig_objects(arm, objs, active_mat)
        skin_img = get_skin_image(arm, props)
        if active_mat and skin_img:
            img_node = find_image_node(active_mat)
            if img_node:
                img_node.image = skin_img
    elif mode == "IMAGE":
        active_mat = img_mat or default_mat
        assign_material_to_rig_objects(arm, objs, active_mat)
        if active_mat and custom_img:
            img_node = find_image_node(active_mat)
            if img_node:
                img_node.image = custom_img
    else:  # "COLOR"
        active_mat = default_mat or img_mat
        assign_material_to_rig_objects(arm, objs, active_mat)
        if active_mat:
            rgb_node = find_rgb_node(active_mat)
            if rgb_node:
                rgb_node.outputs["Color"].default_value = tuple(color_val)


def apply_eye_pupil_style(arm, props):
    if props.eye_target in {"EYE", "BOTH"}:
        _apply_single_eye_or_pupil(arm, props, is_pupil=False)
    if props.eye_target in {"PUPIL", "BOTH"}:
        _apply_single_eye_or_pupil(arm, props, is_pupil=True)
    apply_emission(arm, props)


def apply_emission(arm, props):
    eye_is_img = props.eye_mode in {"SKIN", "IMAGE"}
    pupil_is_img = props.pupil_mode in {"SKIN", "IMAGE"}

    if props.emission_target in {"EYE", "BOTH"}:
        eye_mats = [
            resolve_rig_material(arm, CONFIG["mat_eye"]),
            resolve_rig_material(arm, CONFIG["mat_eye_img"]),
        ]
        for m in eye_mats:
            if m:
                set_emission_settings(
                    m,
                    is_image_mode=eye_is_img,
                    enabled=props.emission_enabled,
                    strength=props.emission_strength,
                    use_custom_color=props.emission_use_custom_color,
                    custom_color=props.emission_color,
                )

    if props.emission_target in {"PUPIL", "BOTH"}:
        pupil_mats = [
            resolve_rig_material(arm, CONFIG["mat_pupil"]),
            resolve_rig_material(arm, CONFIG["mat_pupil_img"]),
        ]
        for m in pupil_mats:
            if m:
                set_emission_settings(
                    m,
                    is_image_mode=pupil_is_img,
                    enabled=props.emission_enabled,
                    strength=props.emission_strength,
                    use_custom_color=props.emission_use_custom_color,
                    custom_color=props.emission_color,
                )


def apply_arm_mode(context, arm, props):
    is_slim = props.arm_mode == "SLIM"

    for name in CONFIG["objs_wide_arms"]:
        set_rig_object_hidden(arm, name, is_slim)
    for name in CONFIG["objs_slim_arms"]:
        set_rig_object_hidden(arm, name, not is_slim)

    set_vl_checkbox_exclude(context, arm, CONFIG["vl_col_wide_arms"], is_slim)
    set_vl_checkbox_exclude(context, arm, CONFIG["vl_col_slim_arms"], not is_slim)

    set_bone_collection_visible(arm, CONFIG["bone_col_wide_arms"], not is_slim)
    set_bone_collection_visible(arm, CONFIG["bone_col_slim_arms"], is_slim)


def apply_all_settings_to_rig(context, arm, props):
    """Terapkan seluruh pengaturan ke armature target."""
    hide_wgts_collections(context, arm)
    apply_skin_texture(arm, props)
    apply_arm_mode(context, arm, props)
    apply_face_visibility(context, arm, props)
    apply_eyebrow_style(arm, props)
    apply_eye_pupil_style(arm, props)
    apply_emission(arm, props)
    apply_accessories_visibility(context, arm, props)
    apply_armor_visibility(context, arm, props)
    apply_armor_textures(arm, props)