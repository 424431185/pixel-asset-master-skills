#!/usr/bin/env python3
"""Pixel Asset Master - Project Manager

Init, validate, and manage pixel art asset generation projects.

Usage:
    python project_manager.py init <project_name> [--size 32x32] [--palette default]
    python project_manager.py import-sources <project_path> <files...> [--move]
    python project_manager.py validate <project_path>
"""

import argparse
import csv
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# ── 常量 ──────────────────────────────────────────────

SKILL_DIR = Path(__file__).resolve().parent.parent
PROJECTS_DIR = SKILL_DIR.parent.parent / "projects"

ASSET_CATEGORIES = ["characters", "tiles", "items", "ui", "effects", "backgrounds"]

PROJECT_TEMPLATE = {
    "design_spec.md": "",
    "spec_lock.md": "",
    "images": [],
    "assets": {cat: [] for cat in ASSET_CATEGORIES},
    "animations": [],
    "sheets": [],
    "notes": [],
    "exports": [],
}


def cmd_init(args):
    """初始化新项目"""
    name = args.project_name
    size = args.size or "32x32"
    palette = args.palette or "default"
    date_str = datetime.now().strftime("%Y%m%d")

    # 解析尺寸
    try:
        w, h = size.lower().split("x")
        w_int, h_int = int(w), int(h)
    except ValueError:
        print(f"[ERROR] Invalid size format: {size}. Expected WxH (e.g. 32x32)")
        sys.exit(1)

    # 尺寸上限验证
    MAX_SIZE = 2048
    if w_int > MAX_SIZE or h_int > MAX_SIZE:
        print(f"[ERROR] Size {size} exceeds maximum {MAX_SIZE}x{MAX_SIZE}")
        sys.exit(1)
    if w_int < 1 or h_int < 1:
        print(f"[ERROR] Size {size} is too small. Minimum 1x1.")
        sys.exit(1)

    project_name = f"{name}_{size}_{date_str}"
    project_path = PROJECTS_DIR / project_name

    if project_path.exists():
        print(f"[ERROR] Project already exists: {project_path}")
        sys.exit(1)

    # 创建目录结构
    project_path.mkdir(parents=True, exist_ok=True)
    for cat in ASSET_CATEGORIES:
        (project_path / "assets" / cat).mkdir(parents=True, exist_ok=True)
    (project_path / "animations").mkdir(parents=True, exist_ok=True)
    (project_path / "sheets").mkdir(parents=True, exist_ok=True)
    (project_path / "notes").mkdir(parents=True, exist_ok=True)
    (project_path / "exports").mkdir(parents=True, exist_ok=True)
    (project_path / "images").mkdir(parents=True, exist_ok=True)

    # 生成初始 spec_lock.md
    _generate_initial_spec_lock(project_path, name, size, palette)

    # 生成初始 design_spec.md
    _generate_initial_design_spec(project_path, name, size, palette)

    print(f"[OK] Project initialized: {project_path}")
    print(f"     Size: {size}")
    print(f"     Palette: {palette}")
    print(f"     Categories: {', '.join(ASSET_CATEGORIES)}")


def cmd_import_sources(args):
    """导入参考图片"""
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"[ERROR] Project not found: {project_path}")
        sys.exit(1)

    images_dir = project_path / "images"
    imported = []

    for src in args.files:
        src_path = Path(src)
        if not src_path.exists():
            print(f"[WARN] File not found, skipping: {src}")
            continue

        dst = images_dir / src_path.name
        if args.move:
            shutil.move(str(src_path), str(dst))
        else:
            shutil.copy2(str(src_path), str(dst))
        imported.append(dst.name)
        print(f"  Imported: {dst.name}")

    print(f"[OK] Imported {len(imported)} file(s) to {images_dir}")


def cmd_validate(args):
    """验证项目结构"""
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"[ERROR] Project not found: {project_path}")
        sys.exit(1)

    issues = []

    # 检查必要文件
    for required in ["design_spec.md", "spec_lock.md"]:
        if not (project_path / required).exists():
            issues.append(f"Missing: {required}")

    # 检查目录
    for cat in ASSET_CATEGORIES:
        d = project_path / "assets" / cat
        if not d.exists():
            issues.append(f"Missing directory: assets/{cat}")

    for required_dir in ["images", "animations", "sheets", "notes", "exports"]:
        if not (project_path / required_dir).exists():
            issues.append(f"Missing directory: {required_dir}")

    # 检查 spec_lock 可解析性
    spec_lock = project_path / "spec_lock.md"
    if spec_lock.exists():
        content = spec_lock.read_text(encoding="utf-8")
        if "palette" not in content:
            issues.append("spec_lock.md missing palette section")
        if "canvas" not in content:
            issues.append("spec_lock.md missing canvas section")

    if issues:
        print(f"[WARN] Validation found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("[OK] Project validation passed")


def _generate_initial_spec_lock(project_path, name, size, palette_name):
    """生成初始 spec_lock.md"""
    # 读取调色板
    palettes_index = SKILL_DIR / "templates" / "palettes" / "palettes_index.json"
    palette_hex = []
    if palettes_index.exists():
        palettes = json.loads(palettes_index.read_text(encoding="utf-8"))
        for p in palettes:
            if p["name"].lower() == palette_name.lower():
                palette_hex = p["hex"]
                palette_name = p["name"]
                break

    if not palette_hex:
        palette_hex = ["#000000", "#FFFFFF"]
        palette_name = "custom"

    colors_yaml = "\n".join(f"  - {c}" for c in palette_hex)

    content = f"""# Execution Lock

## canvas
- base_size: {size}
- tile_size: {size}
- format: RGBA PNG

## palette
- name: {palette_name}
- colors:
{colors_yaml}

## style
- sub_style: outlined
- outline_color: #000000
- shading: 3-tone
- dithering: none
- light_direction: top-left

## per_sprite_budget
- max_colors: 16

## assets
- characters: []
- tiles: []
- items: []
- ui: []
- effects: []
- backgrounds: []

## forbidden
- Anti-aliasing
- Gradient fills
- Partial opacity (1-254 alpha)
- Colors outside declared palette
- Sub-pixel rendering
"""
    (project_path / "spec_lock.md").write_text(content, encoding="utf-8")


def _generate_initial_design_spec(project_path, name, size, palette_name):
    """生成初始 design_spec.md"""
    content = f"""# {name} - Design Spec

> Human-readable design narrative. Machine-readable contract: spec_lock.md.

## I. Project Information

| Item | Value |
| ---- | ----- |
| **Project Name** | {name} |
| **Canvas Size** | {size} |
| **Asset Count** | TBD |
| **Art Style** | TBD |
| **Target Platform** | TBD |
| **Color Palette** | {palette_name} |
| **Created Date** | {datetime.now().strftime("%Y-%m-%d")} |

---

## II-VIII. Sections to be filled by Strategist

(See templates/design_spec_reference.md for full structure)
"""
    (project_path / "design_spec.md").write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Pixel Asset Master - Project Manager")
    sub = parser.add_subparsers(dest="command")

    # init
    p_init = sub.add_parser("init", help="Initialize new project")
    p_init.add_argument("project_name", help="Project name")
    p_init.add_argument("--size", default="32x32", help="Base sprite size (e.g. 32x32)")
    p_init.add_argument("--palette", default="DB32", help="Palette name from index")

    # import-sources
    p_import = sub.add_parser("import-sources", help="Import reference images")
    p_import.add_argument("project_path", help="Project directory path")
    p_import.add_argument("files", nargs="+", help="Files to import")
    p_import.add_argument("--move", action="store_true", help="Move instead of copy")

    # validate
    p_validate = sub.add_parser("validate", help="Validate project structure")
    p_validate.add_argument("project_path", help="Project directory path")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "import-sources":
        cmd_import_sources(args)
    elif args.command == "validate":
        cmd_validate(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
