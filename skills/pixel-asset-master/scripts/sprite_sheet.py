#!/usr/bin/env python3
"""Pixel Asset Master - Sprite Sheet Packer

Pack individual PNG sprites into sprite sheets with manifest.

Usage:
    python sprite_sheet.py <project_path>
    python sprite_sheet.py <project_path> --by-category
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def pack_sheets(project_path, by_category=True):
    """将素材打包为精灵图"""
    project_path = Path(project_path)
    assets_dir = project_path / "assets"
    sheets_dir = project_path / "sheets"

    if not assets_dir.exists():
        print("[ERROR] No assets directory")
        return

    if not HAS_PIL:
        print("[ERROR] Pillow required: pip install Pillow")
        sys.exit(1)

    sheets_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"sheets": []}

    categories = sorted(d.name for d in assets_dir.iterdir() if d.is_dir())

    for cat in categories:
        cat_dir = assets_dir / cat
        pngs = sorted(cat_dir.glob("*.png"))

        if not pngs:
            continue

        # 获取所有帧尺寸
        sizes = {}
        for png in pngs:
            img = Image.open(png)
            key = f"{img.width}x{img.height}"
            if key not in sizes:
                sizes[key] = []
            sizes[key].append(png)

        # 按尺寸分组打包
        for size_key, files in sizes.items():
            w, h = map(int, size_key.split("x"))

            if by_category:
                # 按动画分组
                anim_groups = _group_by_animation(files)
                for anim_name, anim_files in anim_groups.items():
                    sheet_name = f"{cat}_{anim_name}_{size_key}.png"
                    _create_sheet(sheets_dir / sheet_name, anim_files, w, h, manifest, cat, anim_name)
            else:
                sheet_name = f"{cat}_{size_key}.png"
                _create_sheet(sheets_dir / sheet_name, files, w, h, manifest, cat, "all")

    # 写入 manifest
    manifest_path = sheets_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Generated {len(manifest['sheets'])} sheet(s), manifest saved")


def _group_by_animation(files):
    """按动画名称分组文件"""
    groups = {}
    for f in files:
        # 从文件名提取动画名: player_idle_0 → player_idle
        stem = f.stem
        parts = stem.rsplit("_", 1)
        if len(parts) == 2 and parts[1].isdigit():
            anim_name = parts[0]
        else:
            anim_name = stem

        if anim_name not in groups:
            groups[anim_name] = []
        groups[anim_name].append(f)

    return groups


def _create_sheet(sheet_path, files, tile_w, tile_h, manifest, category, anim_name):
    """创建单个精灵图"""
    n = len(files)
    cols = min(n, 16)  # 最多16列
    rows = (n + cols - 1) // cols

    sheet = Image.new("RGBA", (cols * tile_w, rows * tile_h), (0, 0, 0, 0))

    for i, f in enumerate(files):
        img = Image.open(f).convert("RGBA")
        col = i % cols
        row = i // cols
        sheet.paste(img, (col * tile_w, row * tile_h))

    sheet.save(sheet_path, "PNG")

    manifest["sheets"].append({
        "file": sheet_path.name,
        "category": category,
        "animation": anim_name,
        "tile_size": {"width": tile_w, "height": tile_h},
        "columns": cols,
        "rows": rows,
        "frame_count": n,
        "frames": [f.stem for f in files],
    })

    print(f"  Packed: {sheet_path.name} ({n} frames, {cols}x{rows})")


def main():
    parser = argparse.ArgumentParser(description="Pixel Asset Master - Sprite Sheet Packer")
    parser.add_argument("project_path", help="Project directory path")
    parser.add_argument("--by-category", action="store_true", default=True, help="Pack by category and animation")
    args = parser.parse_args()

    pack_sheets(args.project_path, args.by_category)


if __name__ == "__main__":
    main()
