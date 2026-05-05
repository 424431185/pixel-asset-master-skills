# User Project Workspace

This directory stores in-progress pixel art generation projects.

## Create a New Project

```bash
python skills/pixel-asset-master/scripts/project_manager.py init <project_name> --size 256x256 --palette default
```

## Directory Structure

A typical project:

```
project_name_size_YYYYMMDD/
├── design_spec.md          # Human-readable design narrative
├── spec_lock.md            # Machine-readable execution contract
├── images/                 # User-provided reference images
├── assets/                 # Generated pixel art assets (PNG)
│   ├── characters/
│   ├── tiles/
│   ├── items/
│   ├── ui/
│   ├── effects/
│   └── backgrounds/
├── animations/             # Animation frame sequences
├── sheets/                 # Packed sprite sheets
├── notes/                  # Design notes per asset
└── exports/                # Final export directory
```

## Notes

- Contents under this directory are excluded by `.gitignore`
- Completed projects can be moved to `examples/` for sharing
