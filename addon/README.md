# AzkiRIG Blender Add-on

AzkiRIG is a companion add-on for the AzkiRig Minecraft character rig.

## Current status — 0.1.0

This first implementation is deliberately limited to operations that can be mapped from the rig's currently identified datablock names:

- Toggle face, eyes, eyebrows, and mouth visibility.
- Toggle armor, cape, and elytra visibility.
- Switch visibility between the Wide Arms and Slim Arms groups.
- Replace the skin image in the `AzkiRig Skin` material.
- Replace image nodes used by main armor or leggings materials.
- Restore visibility to the state captured when the add-on was enabled.

The add-on does not rename, delete, re-parent, or rebuild rig objects.

## Installation

1. In Blender, open **Edit → Preferences → Get Extensions**.
2. Use **Install from Disk** and select a ZIP containing the contents of this `addon/` folder, with `blender_manifest.toml` at the ZIP root.
3. Enable **AzkiRIG**.
4. Open the 3D Viewport and press **N** to open the sidebar.
5. Select the **AzkiRIG** tab.

For local development, the `addon/` folder can also be installed as an extension package using Blender's extension development workflow.

## Important mapping notes

The object and collection names in `config.py` come from a static inspection of the supplied AzkiRig Face file. A full in-Blender audit of collection nesting, material node graphs, and object visibility is still required.

Texture replacement currently updates every Image Texture node in each resolved target material. If a material contains multiple image nodes for different purposes, they will all receive the selected image. This behavior must be narrowed after inspecting the actual node graphs.

## Not implemented yet

The following requested features are intentionally deferred until the rig can be inspected inside Blender:

- Eyebrow image/default mode and eyebrow color.
- Eye and pupil color controls.
- Eye/pupil emission controls.
- Pupil texture selection.
- Independent armor visibility and armor texture mapping by exact material.
- A verified Wide/Slim arm switch that accounts for all collection and render states.
- A rig-aware reset for material values and texture assignments.
- Dynamic Parent integration.

These need the actual material node layouts, collection hierarchy, constraints, and parenting setup. Guessing those structures could damage the rig's existing setup.
