#!/usr/bin/env python3
"""Pixel Asset Master - Asset Validator

Validate pixel art assets against project specifications.

Usage:
    python asset_validator.py <project_path>
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def validate_project(project_path):
    """验证项目中的所有素材"""
    project_path = Path(project_path)
    spec_lock = project_path / "spec_lock.md"
    assets_dir = project_path / "assets"

    if not spec_lock.exists():
        print("[ERROR] spec_lock.md not found")
        return False

    if not assets_dir.exists():
        print("[WARN] No assets directory yet")
        return True

    # 解析 spec_lock
    content = spec_lock.read_text(encoding="utf-8")
    palette_colors = set()
    base_size = None
    max_colors = 16

    in_palette = False
    in_canvas = False
    in_budget = False
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("## palette"):
            in_palette = True
            continue
        if line.startswith("## canvas"):
            in_canvas = True
            continue
        if line.startswith("## per_sprite_budget"):
            in_budget = True
            continue
        if line.startswith("## ") and (in_palette or in_canvas or in_budget):
            in_palette = in_canvas = in_budget = False
            continue
        if in_palette and line.startswith("- #"):
            palette_colors.add(line[2:].upper())
        if in_canvas and line.startswith("- base_size:"):
            size_str = line.split(":", 1)[1].strip()
            try:
                w, h = size_str.split("x")
                base_size = (int(w), int(h))
            except ValueError:
                pass
        if in_budget and line.startswith("- max_colors:"):
            try:
                max_colors = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass

    if not palette_colors:
        print("[WARN] No palette colors found in spec_lock.md")

    print(f"Spec: base_size={base_size}, max_colors={max_colors}, palette={len(palette_colors)} colors")

    if not HAS_PIL:
        print("[WARN] Pillow not installed, limited validation")
        return _validate_structure_only(project_path)

    # 验证每个 PNG
    errors = []
    warnings = []
    total_assets = 0

    for png in sorted(assets_dir.rglob("*.png")):
        total_assets += 1
        img = Image.open(png)
        w, h = img.size

        # 检查尺寸是否合理
        if base_size:
            bw, bh = base_size
            if w % bw != 0 or h % bh != 0:
                if w != bw or h != bh:
                    warnings.append(f"{png.name}: size {w}x{h} not a multiple of base {bw}x{bh}")

        # 检查颜色数
        img_rgba = img.convert("RGBA")
        pixels = list(img_rgba.getdata())
        unique_colors = set()
        out_of_palette = set()

        for r, g, b, a in pixels:
            if a < 128:
                continue
            hex_c = f"#{r:02X}{g:02X}{b:02X}"
            unique_colors.add(hex_c)
            if palette_colors and hex_c.upper() not in palette_colors:
                out_of_palette.add(hex_c)

        if len(unique_colors) > max_colors:
            errors.append(f"{png.name}: {len(unique_colors)} colors exceeds budget of {max_colors}")

        if out_of_palette:
            errors.append(f"{png.name}: {len(out_of_palette)} color(s) outside declared palette")

        # 检查是否有抗锯齿（半透明像素）
        semi_transparent = sum(1 for _, _, _, a in pixels if 0 < a < 255)
        if semi_transparent > 0:
            warnings.append(f"{png.name}: {semi_transparent} semi-transparent pixels (possible anti-aliasing)")

    # 结构验证
    struct_ok = _validate_structure_only(project_path, quiet=True)

    # 结果汇总
    print(f"\n{'='*60}")
    print(f"[SCAN] Checked {total_assets} asset(s)")
    if errors:
        print(f"  [ERROR] {len(errors)} error(s):")
        for e in errors:
            print(f"    - {e}")
    if warnings:
        print(f"  [WARN] {len(warnings)} warning(s):")
        for w in warnings:
            print(f"    - {w}")
    if not errors and not warnings:
        print("  [OK] All assets passed validation")
    elif not errors:
        print("  [OK] Passed with warnings")

    return len(errors) == 0


def _validate_structure_only(project_path, quiet=False):
    """仅验证目录结构"""
    project_path = Path(project_path)
    required_dirs = ["assets", "images", "animations", "sheets", "notes", "exports"]
    required_files = ["design_spec.md", "spec_lock.md"]
    issues = []

    for d in required_dirs:
        if not (project_path / d).exists():
            issues.append(f"Missing directory: {d}")

    for f in required_files:
        if not (project_path / f).exists():
            issues.append(f"Missing file: {f}")

    if issues:
        if not quiet:
            for i in issues:
                print(f"  [WARN] {i}")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Pixel Asset Master - Asset Validator")
    parser.add_argument("project_path", help="Project directory path")
    args = parser.parse_args()

    ok = validate_project(args.project_path)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
