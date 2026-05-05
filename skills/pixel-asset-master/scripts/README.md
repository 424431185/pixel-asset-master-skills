# Pixel Asset Master - Scripts Reference

## Overview

All scripts are located in `skills/pixel-asset-master/scripts/`. Run from the repository root.

## Scripts

### project_manager.py

Project initialization and management.

```bash
# Initialize new project
python skills/pixel-asset-master/scripts/project_manager.py init <name> --size 32x32 --palette DB32

# Import reference images
python skills/pixel-asset-master/scripts/project_manager.py import-sources <project_path> <files...> --move

# Validate project structure
python skills/pixel-asset-master/scripts/project_manager.py validate <project_path>
```

### palette_analyzer.py

Extract and validate color palettes.

```bash
# Extract palette from reference image
python skills/pixel-asset-master/scripts/palette_analyzer.py extract <image> --count 16

# Validate assets against project palette
python skills/pixel-asset-master/scripts/palette_analyzer.py validate <project_path>

# Calculate color distance
python skills/pixel-asset-master/scripts/palette_analyzer.py distance #FF0000 #00FF00
```

### asset_validator.py

Validate pixel art assets against project specifications.

```bash
python skills/pixel-asset-master/scripts/asset_validator.py <project_path>
```

Checks: palette compliance, color budget, anti-aliasing, animation consistency, file format.

### sprite_sheet.py

Pack individual PNGs into sprite sheets.

```bash
python skills/pixel-asset-master/scripts/sprite_sheet.py <project_path> --by-category
```

Output: sprite sheet PNGs + `manifest.json` with frame metadata.

### finalize_assets.py

Post-process pixel art assets.

```bash
# Quantize colors to declared palette
python skills/pixel-asset-master/scripts/finalize_assets.py <project_path> --quantize

# Clean stray isolated pixels
python skills/pixel-asset-master/scripts/finalize_assets.py <project_path> --clean

# Convert to indexed PNG
python skills/pixel-asset-master/scripts/finalize_assets.py <project_path> --index

# Run all steps
python skills/pixel-asset-master/scripts/finalize_assets.py <project_path> --all
```

## Dependencies

- **Pillow**: Required for image processing (`pip install Pillow`)
- **Python 3.8+**: Minimum version
