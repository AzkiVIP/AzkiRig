# AzkiRIG

**A Blender add-on for Minecraft character rig customization.**

AzkiRIG provides an integrated control panel for customizing and managing Minecraft character rigs directly inside Blender.

Instead of manually navigating through multiple Blender properties and collections, AzkiRIG brings common rig customization tools into one interface.

## Features

### Character Customization
- **Skin Texture** — Replace the character's skin texture.
- **Arm Mode** — Switch between Wide and Slim arms.
- **Eyebrow** — Choose between Skin Texture, Solid Color, and Custom Image.
- **Eye & Pupil** — Customize eye and pupil appearance independently or together.
- **Emission** — Configure emission for eyes, pupils, or both, including custom color and strength.

### Visibility Controls
- Toggle individual facial features:
  - Face
  - Eyebrows
  - Eyes
  - Mouth
- Toggle Cape and Elytra visibility.
- Control armor visibility globally, by armor category, and by individual armor parts.

### Armor Customization
- Replace the main armor texture.
- Replace the leggings texture.

### Dynamic Parent
Create flexible parenting relationships for objects and pose bones.

Available controls:
- **Bind** — Create a Dynamic Parent relationship.
- **Release** — Disable the active relationship while preserving animation.
- **Bake Keys** — Bake the resulting motion into keyframes.
- **Clear All** — Remove Dynamic Parent constraints and related animation data.

### Rig Management
- Add the bundled Minecraft rig through the `Shift + A` menu.
- Manage rig settings through the dedicated sidebar panel.
- Reset individual sections or all settings.

## Requirements

- Blender 5.0 or newer.

## Installation

1. Download the latest `AzkiRIG` ZIP package.
2. Open Blender.
3. Go to **Edit → Preferences → Get Extensions**.
4. Open the dropdown menu and select **Install from Disk**.
5. Select the downloaded ZIP package.
6. Enable AzkiRIG if it is not enabled automatically.

## Usage

1. Open the 3D Viewport.
2. Press `N` to open the Sidebar.
3. Select the **AzkiRig** tab.
4. Use the controls to customize your character.

To add a new rig, press `Shift + A` and select **AzkiRig**.

## Project Structure

The repository contains:

- `__init__.py` — Add-on registration and metadata.
- `blender_manifest.toml` — Blender Extension metadata.
- `config.py` — Centralized rig configuration.
- `properties.py` — Add-on settings and properties.
- `operators.py` — Blender operators.
- `rig_utils.py` — Rig, visibility, and material utilities.
- `dynamic_parent.py` — Dynamic Parent functionality.
- `ui.py` — Sidebar interface.
- `AzkiRig.blend` — Bundled rig asset.
- `textures/` — Character and equipment textures.

## License

AzkiRIG is intended to be distributed under the **GNU General Public License v3.0 or later (GPL-3.0-or-later)**.

See the `LICENSE` file for the full license terms.

## Credits

Created by **AzkiVIP**.

*Crafted to Stand Out.*