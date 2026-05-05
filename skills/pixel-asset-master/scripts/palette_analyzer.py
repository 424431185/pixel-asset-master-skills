#!/usr/bin/env python3
"""Pixel Asset Master - Palette Analyzer

Extract dominant colors from reference images and validate palettes.

Usage:
    python palette_analyzer.py extract <image_path> [--count 16]
    python palette_analyzer.py validate <project_path>
    python palette_analyzer.py distance <color1> <color2>
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


def extract_palette(image_path, count=16):
    """从图片提取主色调"""
    if not HAS_PIL:
        print("[ERROR] Pillow required: pip install Pillow")
        sys.exit(1)

    img = Image.open(image_path).convert("RGBA")
    pixels = list(img.getdata())

    # 过滤透明像素
    opaque = [(r, g, b) for r, g, b, a in pixels if a > 128]

    if not opaque:
        print("[ERROR] No opaque pixels found in image")
        return []

    # 简单颜色量化：按频率排序后聚类
    color_counts = {}
    for r, g, b in opaque:
        # 量化到4级（减少颜色变体）
        qr = (r >> 4) << 4
        qg = (g >> 4) << 4
        qb = (b >> 4) << 4
        key = (qr, qg, qb)
        color_counts[key] = color_counts.get(key, 0) + 1

    # 按频率排序
    sorted_colors = sorted(color_counts.items(), key=lambda x: -x[1])

    # 取前N个，合并相近颜色
    palette = []
    for (r, g, b), _ in sorted_colors:
        hex_color = f"#{r:02X}{g:02X}{b:02X}"
        # 检查是否与已有颜色太近
        too_close = False
        for existing in palette:
            er, eg, eb = int(existing[1:3], 16), int(existing[3:5], 16), int(existing[5:7], 16)
            dist = ((r - er) ** 2 + (g - eg) ** 2 + (b - eb) ** 2) ** 0.5
            if dist < 30:
                too_close = True
                break
        if not too_close:
            palette.append(hex_color)
        if len(palette) >= count:
            break

    return palette


def validate_palette(project_path):
    """验证项目中的素材是否使用了声明的调色板"""
    project_path = Path(project_path)
    spec_lock = project_path / "spec_lock.md"

    if not spec_lock.exists():
        print("[ERROR] spec_lock.md not found")
        return

    # 解析 spec_lock 中的调色板
    content = spec_lock.read_text(encoding="utf-8")
    palette_colors = set()
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
            palette_colors.add(line[2:].upper())

    if not palette_colors:
        print("[WARN] No palette colors found in spec_lock.md")
        return

    print(f"Declared palette: {len(palette_colors)} colors")

    # 检查所有 PNG 素材
    if not HAS_PIL:
        print("[WARN] Pillow not installed, skipping image validation")
        return

    issues = []
    assets_dir = project_path / "assets"
    if not assets_dir.exists():
        print("[WARN] No assets directory yet")
        return

    for png in assets_dir.rglob("*.png"):
        img = Image.open(png).convert("RGBA")
        pixels = list(img.getdata())
        for r, g, b, a in pixels:
            if a < 128:
                continue  # 跳过透明
            hex_c = f"#{r:02X}{g:02X}{b:02X}"
            if hex_c.upper() not in palette_colors:
                issues.append(f"{png.name}: color {hex_c} not in palette")
                break  # 每个文件只报一次

    if issues:
        print(f"[WARN] {len(issues)} asset(s) with out-of-palette colors:")
        for issue in issues[:20]:
            print(f"  - {issue}")
    else:
        print("[OK] All assets use declared palette colors")


def color_distance(c1, c2):
    """计算两个颜色之间的欧氏距离"""
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


def main():
    parser = argparse.ArgumentParser(description="Pixel Asset Master - Palette Analyzer")
    sub = parser.add_subparsers(dest="command")

    # extract
    p_extract = sub.add_parser("extract", help="Extract palette from image")
    p_extract.add_argument("image_path", help="Path to reference image")
    p_extract.add_argument("--count", type=int, default=16, help="Number of colors to extract")

    # validate
    p_validate = sub.add_parser("validate", help="Validate assets against project palette")
    p_validate.add_argument("project_path", help="Project directory path")

    # distance
    p_dist = sub.add_parser("distance", help="Calculate distance between two colors")
    p_dist.add_argument("color1", help="First color (hex, e.g. #FF0000)")
    p_dist.add_argument("color2", help="Second color (hex, e.g. #00FF00)")

    args = parser.parse_args()

    if args.command == "extract":
        palette = extract_palette(args.image_path, args.count)
        print(f"Extracted {len(palette)} colors:")
        for c in palette:
            print(f"  {c}")
    elif args.command == "validate":
        validate_palette(args.project_path)
    elif args.command == "distance":
        dist = color_distance(args.color1, args.color2)
        print(f"Distance: {dist:.1f} (max=441.7)")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
