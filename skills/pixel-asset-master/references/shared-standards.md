# Shared Technical Standards — Pixel Art Assets

Common technical constraints for Pixel Asset Master.

---

## 1. Pixel Art Banned Features Blacklist

The following are **forbidden** in generated pixel art assets:

| Banned Feature | Reason |
|----------------|--------|
| Anti-aliasing | Breaks pixel-perfect aesthetic |
| Sub-pixel rendering | Not possible at pixel scale |
| Gradient fills | Use dithering instead |
| Partial opacity (1-254 alpha) | Pixel art uses fully opaque or fully transparent only |
| Blur effects | Breaks crisp edges |
| Bezier curves | Pixels are axis-aligned |
| Vector scaling artifacts | Must be pixel-perfect at declared size |
| Colors outside declared palette | Violates palette consistency |

---

## 2. File Format Standards

### 2.1 PNG Requirements

| Property | Required Value |
|----------|---------------|
| Format | PNG-8 (indexed) or PNG-32 (RGBA) |
| Bit depth | 8-bit indexed preferred; RGBA acceptable |
| Transparency | Alpha channel (index 0 for indexed mode) |
| DPI | 72 (irrelevant for pixel art, but consistent) |
| Interlacing | None |

### 2.2 Sprite Sheet Format

Standard sprite sheet layout:

```
+---+---+---+---+---+---+
| 0 | 1 | 2 | 3 | 4 | 5 |  ← Row = animation frames
+---+---+---+---+---+---+
| 6 | 7 | 8 | 9 |   |   |  ← Multiple rows = multiple animations
+---+---+---+---+---+---+
```

**Manifest format** (`manifest.json`):
```json
{
  "name": "player",
  "size": {"width": 32, "height": 32},
  "palette": "db32",
  "animations": {
    "idle": {"row": 0, "frames": 4, "fps": 8, "loop": true},
    "walk": {"row": 1, "frames": 6, "fps": 12, "loop": true},
    "attack": {"row": 2, "frames": 5, "fps": 12, "loop": false}
  }
}
```

---

## 3. Palette File Formats

### 3.1 GPL Format (GIMP Palette)

```
GIMP Palette
Name: Custom Palette
Columns: 8
#
255 255 255	#FFFFFF
0   0   0   	#000000
...
```

### 3.2 PAL Format (JASC Palette)

```
JASC-PAL
0100
16
255 255 255
0 0 0
...
```

### 3.3 ACT Format (Photoshop Color Table)

Raw binary: 256 × 3 bytes (RGB), followed by 2-byte count (big-endian) + 2-byte transparency index.

---

## 4. Tile Set Standards

### 4.1 Tile Size Conventions

| Standard | Tile Size | Common In |
|----------|-----------|-----------|
| NES | 16x16 | Classic console games |
| SNES | 16x16 | 16-bit era |
| RPG Maker 2000/2003 | 16x16 | RPG Maker |
| RPG Maker MV/MZ | 48x48 | Modern RPG Maker |
| General indie | 32x32 | Most common |
| HD indie | 64x64 | Detailed environments |

### 4.2 Tile Edge Matching

Tiles that form continuous surfaces MUST have matching edges:

- **Autotile format**: 5×3 grid (2×2 corners + 4 edges + center + 4 inner corners)
- **Bitmask format**: 47-tile set covering all 47 edge combinations (bitmask 0-46)
- **Simple format**: Center + 4 edges + 4 corners = 9 tiles minimum

### 4.3 Tile Sheet Layout

```
+------+------+------+------+
| TL   | T    | TR   |      |
+------+------+------+      |
| L    | C    | R    |      |
+------+------+------+------+
| BL   | B    | BR   |      |
+------+------+------+------+
```

Each cell = one tile at declared tile size.

---

## 5. Animation Standards

### 5.1 Frame Timing

| Animation Type | Typical FPS | Typical Frames |
|---------------|-------------|----------------|
| Idle | 6-8 | 2-4 |
| Walk | 8-12 | 4-6 |
| Run | 12-16 | 4-6 |
| Attack | 12-16 | 3-6 |
| Spell cast | 8-12 | 4-8 |
| Hurt | 8-12 | 2-3 |
| Death | 6-10 | 4-6 |
| UI transition | 12-24 | 2-4 |

### 5.2 Animation Sheet Layout

Standard: one row per animation, frames left-to-right.

```
Row 0: idle_0, idle_1, idle_2, idle_3
Row 1: walk_0, walk_1, walk_2, walk_3, walk_4, walk_5
Row 2: attack_0, attack_1, attack_2, attack_3, attack_4
```

---

## 6. Color Quantization

When an AI-generated image needs to be reduced to the declared palette:

1. **Nearest-color mapping**: Map each pixel to the closest palette color (Euclidean distance in RGB space)
2. **Dithering** (optional): Ordered dithering (Bayer matrix) for smooth gradients
3. **Clean-up**: Remove stray single-pixel artifacts after quantization

**Quantization script**:
```bash
python ${SKILL_DIR}/scripts/finalize_assets.py <project_path> --quantize
```

---

## 7. Post-processing Pipeline

Must be executed in order:

```bash
# 1. Quantize all assets to declared palette
python ${SKILL_DIR}/scripts/finalize_assets.py <project_path> --quantize

# 2. Clean stray pixels and enforce pixel-perfect edges
python ${SKILL_DIR}/scripts/finalize_assets.py <project_path> --clean

# 3. Validate all assets
python ${SKILL_DIR}/scripts/asset_validator.py <project_path>

# 4. Pack sprite sheets
python ${SKILL_DIR}/scripts/sprite_sheet.py <project_path>

# 5. Export final package
# Output:
#   exports/<project_name>_<timestamp>.zip
#   ├── sprites/           ← Individual PNGs
#   ├── sheets/            ← Packed sprite sheets
#   ├── palettes/          ← Palette files (GPL/PAL/ACT)
#   └── manifest.json      ← Asset manifest with metadata
```

**Prohibited**:
- NEVER skip the quantize step
- NEVER skip the validation step
- NEVER export assets that fail validation
