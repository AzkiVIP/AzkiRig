"""Scene lookup, visibility and material helpers for AzkiRIG."""

import bpy

from .config import TARGETS


_INITIAL_VISIBILITY = {}


def _walk_collection(collection):
    """Yield objects in a collection and all nested collections."""
    for obj in collection.objects:
        yield obj
    for child in collection.children:
        yield from _walk_collection(child)


def resolve_target(key):
    """Return (collections, objects) found for a configured target."""
    spec = TARGETS.get(key)
    if not spec:
        return [], []

    collections = []
    objects = []

    for name in spec["collections"]:
        collection = bpy.data.collections.get(name)
        if collection:
            collections.append(collection)
            objects.extend(_walk_collection(collection))

    for name in spec["objects"]:
        obj = bpy.data.objects.get(name)
        if obj:
            objects.append(obj)

    # The master armor collection should control only the collection itself,
    # preserving each armor object's independent visibility state.
    if key == "ARMOR" and collections:
        objects.clear()
    elif key == "ARMOR" and not collections:
        fallback_names = (
            "Helmet", "Chestplate",
            "Left Arm Armor", "Right Arm Armor",
            "Left Leg Armor", "Right Leg Armor",
            "Left Boot", "Right Boot",
        )
        objects.extend(
            bpy.data.objects[name]
            for name in fallback_names
            if bpy.data.objects.get(name)
        )

    # Keep datablocks unique while preserving their order.
    collections = list(dict.fromkeys(collections))
    objects = list(dict.fromkeys(objects))
    return collections, objects


def target_members(key):
    collections, objects = resolve_target(key)
    return collections, objects


def set_target_visibility(key, visible):
    """Set viewport and render visibility. Returns affected datablock count."""
    collections, objects = resolve_target(key)
    for collection in collections:
        collection.hide_viewport = not visible
        collection.hide_render = not visible

    for obj in objects:
        obj.hide_viewport = not visible
        obj.hide_render = not visible

    return len(collections) + len(objects)


def toggle_target_visibility(key):
    collections, objects = resolve_target(key)
    members = collections + objects
    if not members:
        return None, 0

    # If every member is hidden in both contexts, show the target; otherwise hide it.
    all_hidden = all(
        member.hide_viewport and member.hide_render
        for member in members
    )
    visible = all_hidden
    count = set_target_visibility(key, visible)
    return visible, count


def capture_initial_visibility():
    """Snapshot current visibility so Reset can restore the opened rig state."""
    _INITIAL_VISIBILITY.clear()

    for key in TARGETS:
        collections, objects = resolve_target(key)
        for collection in collections:
            _INITIAL_VISIBILITY[("COLLECTION", collection.name)] = (
                collection.hide_viewport,
                collection.hide_render,
            )
        for obj in objects:
            _INITIAL_VISIBILITY[("OBJECT", obj.name)] = (
                obj.hide_viewport,
                obj.hide_render,
            )


def restore_target_visibility(key):
    collections, objects = resolve_target(key)
    restored = 0

    for collection in collections:
        state = _INITIAL_VISIBILITY.get(("COLLECTION", collection.name))
        if state is not None:
            collection.hide_viewport, collection.hide_render = state
            restored += 1

    for obj in objects:
        state = _INITIAL_VISIBILITY.get(("OBJECT", obj.name))
        if state is not None:
            obj.hide_viewport, obj.hide_render = state
            restored += 1

    return restored


def restore_all_visibility():
    restored = 0
    for key in TARGETS:
        restored += restore_target_visibility(key)
    return restored


def objects_in_collection_names(names):
    found = []
    for name in names:
        collection = bpy.data.collections.get(name)
        if collection:
            found.extend(_walk_collection(collection))
    return list(dict.fromkeys(found))


def materials_from_objects(objects):
    materials = []
    for obj in objects:
        if obj.type != "MESH":
            continue
        for slot in obj.material_slots:
            material = slot.material
            if material and material.use_nodes and material not in materials:
                materials.append(material)
    return materials


def materials_for_texture_slot(slot):
    """Resolve materials for a replacement slot without changing unrelated materials."""
    if slot == "SKIN":
        material = bpy.data.materials.get("AzkiRig Skin")
        return [material] if material and material.use_nodes else []

    armor_objects = objects_in_collection_names(("armor",))
    if not armor_objects:
        fallback_names = (
            "Helmet", "Chestplate",
            "Left Arm Armor", "Right Arm Armor",
            "Left Leg Armor", "Right Leg Armor",
            "Left Boot", "Right Boot",
        )
        armor_objects = [
            bpy.data.objects[name]
            for name in fallback_names
            if bpy.data.objects.get(name)
        ]

    if slot == "ARMOR_LEGGINGS":
        armor_objects = [
            obj for obj in armor_objects
            if "leg" in obj.name.lower() and "boot" not in obj.name.lower()
        ]
    elif slot == "ARMOR_MAIN":
        armor_objects = [
            obj for obj in armor_objects
            if "leg" not in obj.name.lower()
        ]

    return materials_from_objects(armor_objects)


def replace_material_images(materials, filepath):
    """Replace image references on Image Texture nodes in the supplied materials."""
    image = bpy.data.images.load(filepath, check_existing=True)
    changed = 0

    for material in materials:
        for node in material.node_tree.nodes:
            if node.type == "TEX_IMAGE":
                node.image = image
                changed += 1

    return changed, image
