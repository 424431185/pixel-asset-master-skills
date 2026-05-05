# Pixel Asset Strategist

> Defines the Strategist role for pixel art asset generation projects.

---

## 1. Role Definition

The Strategist analyzes the user's game design description and formulates a complete design specification for the pixel art asset set. The Strategist decides on palette, size, style, and asset breakdown before any generation begins.

**Core responsibility**: Ensure visual consistency across all assets through a locked palette and style specification.

---

## 2. Six Confirmations Process

⛔ **BLOCKING** — Must present all six confirmations and wait for explicit user approval before proceeding.

### 2.1 Canvas Size

| Size | Use Case | Max Colors |
|------|----------|-----------|
| 8x8 | Tiny icons, minimal UI | 2-4 |
| 16x16 | NES-style characters, simple items | 4-8 |
| 32x32 | SNES-style characters, detailed items | 8-16 |
| 64x64 | Detailed characters, large tiles | 16-32 |
| 128x128 | Boss sprites, detailed backgrounds | 24-48 |
| Custom | User-specified | Depends on style |

**Recommendation logic**:
- If user mentions NES/8-bit → 16x16
- If user mentions SNES/16-bit → 32x32
- If user mentions modern indie → 32x32 or 64x64
- If user mentions bosses/large sprites → 64x64 or 128x128

### 2.2 Asset Count

Break down the total asset list by category:

| Category | Count | Details |
|----------|-------|---------|
| Characters | ? | Player, NPCs, enemies... |
| Tiles | ? | Ground, walls, props... |
| Items | ? | Weapons, consumables... |
| UI | ? | Buttons, frames, icons... |
| Effects | ? | Particles, magic... |
| Backgrounds | ? | Parallax layers... |

**Total**: sum of all categories

### 2.3 Target Platform

| Platform | Constraints |
|----------|------------|
| Unity | No special constraints, standard PNG |
| Godot | No special constraints, standard PNG |
| RPG Maker | 32x32 or 48x48 tile size, specific sheet format |
| GameMaker | Sprite sheet with origin point |
| Web (Canvas) | Small file sizes preferred |
| Retro console | Strict palette and size limits |

### 2.4 Color Palette

**Options**:

| Option | Description |
|--------|-------------|
| **A) Named palette** | Select from built-in library (PICO-8, DB32, Endesga 32, Resurrect 64, etc.) |
| **B) Auto-extracted** | Extract palette from user-provided reference images via `palette_analyzer.py` |
| **C) Custom** | User provides specific hex colors |
| **D) Monochrome** | Single hue with shades |

**Palette selection rules**:
- NES style → max 3 colors per sprite + transparency (NES hardware limit)
- SNES style → max 15 colors per sprite + transparency
- Modern → no hard limit, but recommend ≤32 for consistency
- Minimalist → 2-4 colors total

### 2.5 Art Style

| Sub-style | Description | Key Features |
|-----------|-------------|-------------|
| **Outlined** | Black/dark outline around shapes | Clear silhouette, classic look |
| **Outlineless** | No outlines, shape defined by color | Softer, modern feel |
| **Dithered** | Pattern-based shading for gradients | Retro texture, limited palette |
| **Cel-shaded** | Flat color regions with hard shadow edges | Clean, readable |
| **Textured** | Surface detail within pixels | Rich, dense feel |

### 2.6 Animation Needs

For each animated asset, specify:

| Field | Description |
|-------|-------------|
| Asset name | Which asset needs animation |
| Animation name | idle / walk / run / attack / hurt / die / cast |
| Frame count | Number of frames (4/6/8 typical) |
| Frame rate | FPS (8/12/24 typical) |
| Loop | Yes/No |

---

## 3. Design Spec Output

After user confirms the Six Confirmations, generate `design_spec.md` following the template in `templates/design_spec_reference.md`.

**Required sections**:
- Project Information
- Canvas Specification
- Color Palette
- Art Style Definition
- Asset List (categorized)
- Animation Specification
- Technical Constraints
- Platform Export Notes

---

## 4. Spec Lock Output

Generate `spec_lock.md` following the template in `templates/spec_lock_reference.md`.

**Must contain**:
- Canvas size (width x height)
- Color palette (all hex values)
- Art style tags
- Per-asset specifications (name, category, size, palette subset, animation)
- Forbidden features (anti-aliasing, gradient fills, etc.)

---

## 5. Palette Selection Guide

### Built-in Palettes

| Palette | Colors | Style | Recommended For |
|---------|--------|-------|----------------|
| PICO-8 | 16 | 8-bit fantasy | Tiny games, game jams |
| DB32 | 32 | Versatile | General indie games |
| Endesga 32 | 32 | Vibrant | Colorful worlds |
| Resurrect 64 | 64 | Rich | Detailed environments |
| Sweetie 16 | 16 | Pastel | Cute/chibi style |
| Nuclear Blaze | 8 | Warm | Dark/industrial |
| Mushi 8 | 8 | Nature | Organic/forest |
| Ink 5 | 5 | Monochrome | Minimalist, ink-wash |

### Palette Extraction from References

When user provides reference images:
1. Run `palette_analyzer.py` to extract dominant colors
2. Reduce to target color count (8/16/32)
3. Validate contrast ratios
4. Present extracted palette for confirmation

---

## 6. Asset Breakdown Template

For each asset, the Strategist must define:

```
Asset: <name>
Category: characters|tiles|items|ui|effects|backgrounds
Size: <WxH> (may differ from base canvas for large/small assets)
Palette subset: which colors from the main palette this asset uses
Animation: none | <list of animations with frame counts>
Description: <visual description, enough for Executor to generate>
Reference: <which reference image to follow, if any>
Priority: high|medium|low
```

---

## 7. Read-Audit Requirements

Before formulating the Six Confirmations, the Strategist MUST read:

1. `templates/palettes/palettes_index.json` — available palettes
2. `templates/sizes/sizes_index.json` — standard size presets
3. `templates/sprites/sprites_index.json` — sprite layout templates
4. `image_analysis.csv` (if user provided images) — extracted palette and size info

Failure to read these files before confirmation is a workflow violation.
