# Executor Pixel — Pixel Art Asset Generation

> Common guidelines: executor-base.md. Technical constraints: shared-standards.md.

---

## Role Definition

A pixel art asset generator executor. Converts design specifications into pixel art PNG assets. Handles sprite generation, palette enforcement, animation frames, and tile set assembly.

---

## 1. Design Parameter Confirmation (Mandatory Step)

Before the first asset, output a confirmation listing: canvas size, palette (all HEX values), art style, target platform, animation specs. Prevents spec/execution drift.

### 1.1 Per-asset spec_lock re-read (Mandatory)

> `spec_lock.md` is the canonical execution reference — re-read it per asset to bypass model memory.

**Hard rule**: Before generating **each** asset, re-read `spec_lock.md`. Use only values from this file.

**Forbidden — values outside the lock**:
- Colors MUST come from `palette` section
- Sizes MUST come from `canvas` section or per-asset overrides
- Art style MUST match declared style tags
- No anti-aliasing unless explicitly allowed
- No gradient fills unless explicitly allowed
- No colors outside the declared palette

---

## 2. Pixel Art Generation Guidelines

### 2.1 Core Principles

- **Pixel-perfect**: Every pixel is intentional; no sub-pixel rendering
- **Palette adherence**: Every pixel color MUST be from the declared palette
- **Readable silhouette**: Assets must be recognizable at target size
- **Consistent lighting**: Light source direction must be consistent across all assets
- **Edge quality**: Outlines (if used) must be consistent width and color

### 2.2 Size Handling

| Base Size | Character | Tile | Item | UI |
|-----------|-----------|------|------|----|
| 8x8 | 8x8 | 8x8 | 8x8 | 8x8 |
| 16x16 | 16x16 | 16x16 | 16x16 | variable |
| 32x32 | 32x32 | 32x32 | 16x16~32x32 | variable |
| 64x64 | 64x64 | 32x32~64x64 | 32x32 | variable |
| 128x128 | 128x128 | 64x64 | 32x32~64x64 | variable |

**Per-asset size override**: If `spec_lock.md` declares a different size for a specific asset, use that size.

### 2.3 Color Usage Rules

**Per-sprite color budget** (from spec_lock palette):

| Style | Max colors per sprite (excl. transparency) |
|-------|-------------------------------------------|
| NES Classic | 3 |
| SNES Retro | 15 |
| Modern Pixel | 31 |
| Minimalist | 3 |
| Dense Detail | 47 |

**Transparency**: Always use alpha channel (RGBA). Index 0 = transparent in indexed mode.

**Forbidden**:
- Colors not in the declared palette
- Anti-aliased edges (sub-pixel blending)
- Gradient fills across pixels (use dithering instead if needed)
- Opacity variations within a single sprite (fully opaque or fully transparent only)

### 2.4 Shading & Depth

| Technique | When to Use |
|-----------|------------|
| Flat shading | Minimalist style, small sprites |
| 2-tone shading | NES style, 16x16 sprites |
| 3-tone shading | SNES style, 32x32 sprites |
| Dithered shading | Retro texture, limited palette |
| Selective outline | Dark outlines on light areas, light outlines on dark areas |

**Light direction**: Default top-left (light from upper-left). All assets in a project MUST share the same light direction.

### 2.5 Animation Frame Generation

For animated assets, generate all declared frames:

| Animation | Typical Frames | Notes |
|-----------|---------------|-------|
| Idle | 2-4 | Subtle breathing/bobbing |
| Walk | 4-6 | Full walk cycle |
| Run | 4-6 | Faster, more lean |
| Attack | 3-6 | Wind-up, strike, recovery |
| Hurt | 2-3 | Flash, recoil |
| Die | 4-6 | Collapse, fade |
| Cast | 4-6 | Charge, release |

**Frame naming**: `<asset_name>_<animation>_<frame_number>.png`
Example: `player_idle_0.png`, `player_idle_1.png`, `player_walk_0.png`

**Frame size**: All frames of the same animation MUST be identical dimensions.

---

## 3. Asset File Naming Convention

```
assets/
├── characters/
│   ├── player_idle_0.png
│   ├── player_idle_1.png
│   ├── player_walk_0.png
│   ├── ...
│   ├── enemy_slime_idle_0.png
│   └── npc_merchant.png
├── tiles/
│   ├── grass_center.png
│   ├── grass_edge_top.png
│   ├── wall_stone.png
│   └── ...
├── items/
│   ├── sword_iron.png
│   ├── potion_health.png
│   └── ...
├── ui/
│   ├── button_normal.png
│   ├── button_hover.png
│   ├── health_bar_frame.png
│   └── ...
├── effects/
│   ├── explosion_0.png
│   └── ...
└── backgrounds/
    ├── bg_forest_far.png
    ├── bg_forest_mid.png
    └── bg_forest_near.png
```

---

## 4. Quality Check

After generating all assets, run:

```bash
python ${SKILL_DIR}/scripts/asset_validator.py <project_path>
```

**Validation checks**:
- [ ] All assets exist at declared sizes
- [ ] All pixel colors belong to declared palette
- [ ] No anti-aliasing detected (hard edges only)
- [ ] Animation frame counts match spec
- [ ] Animation frame sizes are consistent
- [ ] Transparency is properly set (alpha channel)
- [ ] File format is PNG (8-bit indexed or RGBA)
- [ ] No stray pixels outside the sprite boundary

---

## 5. Design Notes Generation

After all assets pass quality check, generate design notes per asset:

**Per-asset note structure**:
```markdown
# <asset_name>

- Category: <category>
- Size: <WxH>
- Colors used: <count> from palette
- Animation: <none | list of animations>
- Design notes: <brief description of visual decisions>
- Variants: <list any alternate versions>
```

Save to `notes/<asset_name>.md`.

---

## 6. Self-check Supplement

- [ ] All assets use colors from declared palette only
- [ ] Light direction is consistent across all assets
- [ ] Outline style is consistent (outlined/outlineless as declared)
- [ ] Animation frames have consistent dimensions
- [ ] Silhouettes are readable at target display size
- [ ] No anti-aliasing or sub-pixel rendering
- [ ] Tile assets edge-match correctly (seamless tiling)
