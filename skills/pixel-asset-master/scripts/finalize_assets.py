#!/usr/bin/env python3
"""Pixel Asset Master - Asset Finalizer

Post-process pixel art assets: quantize to palette, clean borders, index colors.

Usage:
    python finalize_assets.py <project_path> [--quantize] [--clean] [--index]
    python finalize_assets.py <project_path> --all
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


def cmd_quantize(project_path):
    """将所有素材量化到声明的调色板"""
    if not HAS_PIL:
        print("[ERROR] Pillow required: pip install Pillow")
        sys.exit(1)

    project_path = Path(project_path)
    palette = _load_palette(project_path)
    if not palette:
        print("[ERROR] No palette found in spec_lock.md")
        sys.exit(1)

    print(f"Quantizing to {len(palette)} colors...")

    assets_dir = project_path / "assets"
    if not assets_dir.exists():
        print("[WARN] No assets directory")
        return

    # 构建 PIL 调色板
    pal_rgb = []
    for hex_c in palette:
        r = int(hex_c[1:3], 16)
        g = int(hex_c[3:5], 16)
        b = int(hex_c[5:7], 16)
        pal_rgb.extend([r, g, b])

    # 填充到256色
    while len(pal_rgb) < 768:
        pal_rgb.extend([0, 0, 0])

    count = 0
    for png in sorted(assets_dir.rglob("*.png")):
        img = Image.open(png).convert("RGBA")

        # 量化每个像素到最近调色板颜色
        pixels = list(img.getdata())
        new_pixels = []
        for r, g, b, a in pixels:
            if a < 128:
                new_pixels.append((0, 0, 0, 0))  # 透明
            else:
                nearest = _find_nearest(r, g, b, palette)
                new_pixels.append((*nearest, 255))

        img_quantized = Image.new("RGBA", img.size)
        img_quantized.putdata(new_pixels)
        img_quantized.save(png, "PNG")
        count += 1

    print(f"[OK] Quantized {count} asset(s)")


def cmd_clean(project_path):
    """清除杂散像素"""
    if not HAS_PIL:
        print("[ERROR] Pillow required")
        sys.exit(1)

    project_path = Path(project_path)
    assets_dir = project_path / "assets"
    if not assets_dir.exists():
        return

    count = 0
    for png in sorted(assets_dir.rglob("*.png")):
        img = Image.open(png).convert("RGBA")
        pixels = list(img.getdata())
        w, h = img.size

        changed = False
        new_pixels = list(pixels)

        for y in range(h):
            for x in range(w):
                idx = y * w + x
                r, g, b, a = pixels[idx]

                if a < 128:
                    continue

                # 检查是否是孤立的像素（四周都是透明）
                neighbors = []
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        nidx = ny * w + nx
                        nr, ng, nb, na = pixels[nidx]
                        if na >= 128:
                            neighbors.append((nr, ng, nb))

                if not neighbors:
                    # 孤立像素，设为透明
                    new_pixels[idx] = (0, 0, 0, 0)
                    changed = True

        if changed:
            img_clean = Image.new("RGBA", img.size)
            img_clean.putdata(new_pixels)
            img_clean.save(png, "PNG")
            count += 1

    print(f"[OK] Cleaned stray pixels in {count} asset(s)")


def cmd_index(project_path):
    """将RGBA PNG转为索引色PNG"""
    if not HAS_PIL:
        print("[ERROR] Pillow required")
        sys.exit(1)

    project_path = Path(project_path)
    palette = _load_palette(project_path)

    assets_dir = project_path / "assets"
    if not assets_dir.exists():
        return

    count = 0
    for png in sorted(assets_dir.rglob("*.png")):
        img = Image.open(png).convert("RGBA")
        pixels = list(img.getdata())

        # 构建索引色映射
        pal_colors = []
        for hex_c in palette:
            r = int(hex_c[1:3], 16)
            g = int(hex_c[3:5], 16)
            b = int(hex_c[5:7], 16)
            pal_colors.append((r, g, b))

        # 创建调色板图像
        pal_img = Image.new("P", img.size)
        pal_data = []
        for r, g, b, a in pixels:
            if a < 128:
                pal_data.append(0)  # 索引0=透明
            else:
                nearest_idx = _find_nearest_index(r, g, b, pal_colors)
                pal_data.append(nearest_idx)

        pal_img.putdata(pal_data)

        # 设置调色板
        pal_rgb = [0, 0, 0]  # 索引0=透明
        for r, g, b in pal_colors:
            pal_rgb.extend([r, g, b])
        while len(pal_rgb) < 768:
            pal_rgb.extend([0, 0, 0])

        pal_img.putpalette(pal_rgb)

        # 设置透明色
        pal_img.info["transparency"] = 0

        pal_img.save(png, "PNG")
        count += 1

    print(f"[OK] Converted {count} asset(s) to indexed PNG")


def _load_palette(project_path):
    """从 spec_lock.md 加载调色板"""
    spec_lock = project_path / "spec_lock.md"
    if not spec_lock.exists():
        return []

    content = spec_lock.read_text(encoding="utf-8")
    palette = []
    in_palette = False
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("## palette"):
            in_palette = True
            continue
        if line.startswith("## ") and in_palette:
            in_palette = False
            continue
        if in_palette and line.startswith("- #"):
            palette.append(line[2:].upper())

    return palette


def _find_nearest(r, g, b, palette_hex):
    """找到调色板中最近的颜色"""
    best = None
    best_dist = float("inf")
    for hex_c in palette_hex:
        pr = int(hex_c[1:3], 16)
        pg = int(hex_c[3:5], 16)
        pb = int(hex_c[5:7], 16)
        dist = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if dist < best_dist:
            best_dist = dist
            best = (pr, pg, pb)
    return best


def _find_nearest_index(r, g, b, pal_colors):
    """找到调色板中最近颜色的索引"""
    best_idx = 1  # 0是透明
    best_dist = float("inf")
    for i, (pr, pg, pb) in enumerate(pal_colors):
        dist = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if dist < best_dist:
            best_dist = dist
            best_idx = i + 1  # +1 因为0是透明
    return best_idx


def main():
    parser = argparse.ArgumentParser(description="Pixel Asset Master - Asset Finalizer")
    parser.add_argument("project_path", help="Project directory path")
    parser.add_argument("--quantize", action="store_true", help="Quantize colors to declared palette")
    parser.add_argument("--clean", action="store_true", help="Remove stray isolated pixels")
    parser.add_argument("--index", action="store_true", help="Convert to indexed PNG")
    parser.add_argument("--all", action="store_true", help="Run all post-processing steps")
    args = parser.parse_args()

    if args.all or args.quantize:
        cmd_quantize(args.project_path)
    if args.all or args.clean:
        cmd_clean(args.project_path)
    if args.all or args.index:
        cmd_index(args.project_path)

    if not (args.quantize or args.clean or args.index or args.all):
        parser.print_help()


if __name__ == "__main__":
    main()
