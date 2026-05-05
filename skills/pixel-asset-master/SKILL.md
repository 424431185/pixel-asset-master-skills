---
name: pixel-asset-master
description: >
  AI-driven 2D pixel game asset generation system. Converts game design descriptions
  into pixel art sprites, tilesets, animations, and UI elements through multi-role
  collaboration. Exports as sprite sheets and individual PNGs. Use when user asks to
  "create pixel art", "generate game sprites", "make tileset", "生成像素素材",
  "做游戏瓦片", "制作精灵图", or mentions "pixel-asset-master".
---

# Pixel Asset Master Skill

> AI-driven 2D pixel game asset generation system. Converts game design descriptions into pixel art sprites, tilesets, animations, and UI elements through multi-role collaboration and exports as sprite sheets / individual PNGs.

**Core Pipeline**: `Game Description → Create Project → Style Confirmation → Strategist → [Image_Generator] → Executor → Post-processing → Export`

> [!CAUTION]
> ## 🚨 Global Execution Discipline (MANDATORY)
>
> **This workflow is a strict serial pipeline. The following rules have the highest priority — violating any one of them constitutes execution failure:**
>
> 1. **SERIAL EXECUTION** — Steps MUST be executed in order; the output of each step is the input for the next. Non-BLOCKING adjacent steps may proceed continuously once prerequisites are met
> 2. **BLOCKING = HARD STOP** — Steps marked ⛔ BLOCKING require a full stop; the AI MUST wait for an explicit user response before proceeding
> 3. **NO CROSS-PHASE BUNDLING** — Cross-phase bundling is FORBIDDEN
> 4. **GATE BEFORE ENTRY** — Each Step has prerequisites (🚧 GATE) listed at the top; these MUST be verified before starting that Step
> 5. **NO SPECULATIVE EXECUTION** — "Pre-preparing" content for subsequent Steps is FORBIDDEN
> 6. **NO SUB-AGENT GENERATION** — Executor Step 6 pixel art generation is context-dependent and MUST be completed by the current main agent end-to-end
> 7. **SEQUENTIAL ASSET GENERATION** — Assets MUST be generated sequentially in one continuous pass
> 8. **SPEC_LOCK RE-READ PER ASSET** — Before generating each asset, Executor MUST re-read `spec_lock.md`. All colors / sizes / palettes MUST come from this file

> [!IMPORTANT]
> ## 🌐 Language & Communication Rule
>
> - **Response language**: match the user's input. Explicit user override takes precedence.
> - **Template format**: `design_spec.md` MUST follow its original English template structure regardless of conversation language. Content values may be in the user's language.

> [!IMPORTANT]
> ## 🔌 Compatibility With Generic Coding Skills
>
> - `pixel-asset-master` is a repository-specific workflow, not a general application scaffold
> - Do NOT create `.worktrees/`, `tests/`, branch workflows, or generic engineering structure by default
> - On conflict with a generic coding skill, follow this skill unless the user explicitly says otherwise

## Main Pipeline Scripts

| Script | Purpose |
|--------|---------|
| `${SKILL_DIR}/scripts/project_manager.py` | Project init / validate / manage |
| `${SKILL_DIR}/scripts/palette_analyzer.py` | Palette extraction and validation |
| `${SKILL_DIR}/scripts/asset_validator.py` | Pixel art asset quality check |
| `${SKILL_DIR}/scripts/sprite_sheet.py` | Sprite sheet packing and export |
| `${SKILL_DIR}/scripts/image_gen.py` | AI image generation (multi-provider) |
| `${SKILL_DIR}/scripts/finalize_assets.py` | Asset post-processing (quantize, clean, index) |

For complete tool documentation, see `${SKILL_DIR}/scripts/README.md`.

## Template Index

| Index | Path | Purpose |
|-------|------|---------|
| Palette library | `${SKILL_DIR}/templates/palettes/palettes_index.json` | Query available pixel art color palettes |
| Size presets | `${SKILL_DIR}/templates/sizes/sizes_index.json` | Query standard pixel art dimensions |
| Sprite templates | `${SKILL_DIR}/templates/sprites/sprites_index.json` | Query sprite layout templates (character, tile, item, UI) |

## Standalone Workflows

| Workflow | Path | Purpose |
|----------|------|---------|
| `create-palette` | `workflows/create-palette.md` | Standalone palette creation workflow |
| `batch-animate` | `workflows/batch-animate.md` | Batch animation frame generation |

---

## Pipeline Steps

### Step 1: Source Content Processing

🚧 **GATE**: User provides game design description (text/image/reference)

| Input Type | Processing |
|-----------|-----------|
| Text description | Direct use as design brief |
| Reference images | Analyze style, palette, size via `palette_analyzer.py` |
| Game design doc | Extract asset requirements list |
| Existing sprites | Analyze and extend existing style |

**Output**: Structured asset requirements list

---

### Step 2: Project Initialization

🚧 **GATE**: Step 1 complete

```bash
python ${SKILL_DIR}/scripts/project_manager.py init <project_name> --size 32x32 --palette default
```

**Project structure**:
```
projects/<name>_<size>_<date>/
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

If user provides reference images:
```bash
python ${SKILL_DIR}/scripts/project_manager.py import-sources <project_path> <files...> --move
```

---

### Step 3: Style Confirmation

🚧 **GATE**: Step 2 complete

Select pixel art style direction:

| Style | Description | Typical Size | Palette |
|-------|-------------|-------------|--------|
| **NES Classic** | 8-bit console style, hard edges | 16x16 / 32x32 | 4-8 colors per sprite |
| **SNES Retro** | 16-bit console, more detail | 32x32 / 64x64 | 8-16 colors per sprite |
| **Modern Pixel** | Clean, contemporary indie | 32x32 / 64x64 | 16-32 colors per sprite |
| **Minimalist** | Ultra-simple, few pixels | 8x8 / 16x16 | 2-4 colors per sprite |
| **Dense Detail** | Rich detail, large sprites | 64x64 / 128x128 | 24-48 colors per sprite |
| **High-Res Pixel** | Ultra-detailed, illustration-grade | 256x256 / 512x512 | 64-96 colors per sprite |
| **Cinematic Pixel** | Print/billboard quality | 1024x1024 / 2048x2048 | 128-256 colors per sprite |

⛔ **BLOCKING** — Present style options to user, wait for confirmation.

---

### Step 4: Strategist — Six Confirmations

🚧 **GATE**: Step 3 confirmed

The Strategist formulates **Six Confirmations** for the pixel art project:

| # | Confirmation | Description |
|---|-------------|-------------|
| **1** | **Canvas Size** | Base sprite size per frame. Available presets: 8x8 / 16x16 / 24x24 / 32x32 / 48x48 / 64x64 / 128x128 / 256x256 / 512x512 / 1024x1024 / 2048x2048. Custom sizes allowed (max 2048x2048). **For character sprite sheets, prefer ≥ 64x64** for sufficient detail. |
| **2** | **Asset Count** | Total number of assets to generate |
| **3** | **Target Platform** | Game engine / runtime (Unity, Godot, RPG Maker, web, etc.) |
| **4** | **Color Palette** | Specific palette or auto-derived from references |
| **5** | **Art Style** | Pixel art sub-style (outlined / outlineless / dithered / cel-shaded) |
| **6** | **Animation Needs** | For each character asset, confirm the following: |

**Animation detail breakdown** (for character assets):

| Item | Options | Notes |
|------|---------|-------|
| **Facing direction** | `4-dir` (up/down/left/right) / `8-dir` / `side-only` (left+right) / `single` (front-facing only) | Determines how many directional rows the sprite sheet needs |
| **Action list** | Select from common actions below, or specify custom | Each action = one row in the sprite sheet |
| **Frames per action** | Typical 4-8 frames per action; idle can be 2-4, run 6-8, attack 4-6 | More frames = smoother but larger sheet |

**Common character actions**:

| Action | Typical Frames | Description |
|--------|---------------|-------------|
| `idle` | 2-4 | Standing breathing / subtle motion |
| `walk` | 4-6 | Slow-paced walking cycle |
| `run` | 6-8 | Fast running cycle |
| `jump` | 4-6 | Jump ascent + peak |
| `fall` | 2-4 | Falling / descent |
| `attack` | 4-6 | Melee / ranged attack |
| `hurt` | 2-3 | Taking damage reaction |
| `die` | 4-6 | Death animation |
| `cast` | 4-6 | Magic / skill casting |
| `interact` | 2-4 | Opening chest / pushing / pulling |
| `climb` | 4-6 | Ladder / wall climbing |
| `crouch` | 2-3 | Crouching / sneaking |
| `roll` | 4-6 | Dodge roll |
| `swim` | 4-6 | Swimming cycle |

⛔ **BLOCKING** — Present Six Confirmations to user, wait for explicit confirmation.

After confirmation, generate:
- `design_spec.md` — Human-readable design narrative
- `spec_lock.md` — Machine-readable execution contract

---

### Step 5: Image Acquisition

🚧 **GATE**: Step 4 confirmed

| Scenario | Action |
|----------|--------|
| User provided references | Already in `images/`, skip |
| Need additional references | Use `image_gen.py` or web search |
| No references needed | Generate from description only |

---

### Step 6: Executor — Generate Pixel Art Assets

🚧 **GATE**: Step 5 complete, `spec_lock.md` exists

**Role-specific rules**: see `references/executor-pixel.md`

**Generation phases**:
1. **Visual Construction Phase**: Generate all pixel art PNG assets sequentially
2. **Quality Check Gate**: Run `asset_validator.py` on all assets
3. **Logic Construction Phase**: Generate design notes per asset

**Per-asset generation**:
- Re-read `spec_lock.md` before each asset
- Generate at declared canvas size
- Apply declared palette (quantize if needed)
- Save to appropriate `assets/` subdirectory

**Asset categories**:
| Category | Subdirectory | Typical Assets |
|----------|-------------|----------------|
| Characters | `assets/characters/` | Player, NPCs, enemies, bosses |
| Tiles | `assets/tiles/` | Ground, walls, decorations, transitions |
| Items | `assets/items/` | Weapons, potions, keys, collectibles |
| UI | `assets/ui/` | Buttons, frames, icons, bars, panels |
| Effects | `assets/effects/` | Explosions, particles, magic, weather |
| Backgrounds | `assets/backgrounds/` | Parallax layers, sky, terrain |

---

### 🧱 Tile Generation Standards (MANDATORY)

> Tiles are the most common asset type and easiest to make look "fake". The following 9 rules must ALL be satisfied for every tile.

#### 1. Canvas & Format
- **Default size**: `64×64` RGB (no transparency for ground tiles)
- **Palette**: Strict quantization to declared palette in `spec_lock.md`
- **Anti-pattern**: Anti-aliasing, semi-transparent edges, gradients with > palette colors

#### 2. NO Obvious Geometric Patterns ⛔
The #1 cause of "fake-looking" tiles. Forbidden in repeatable terrain:
| ❌ Anti-pattern | ✅ Replace with |
|----------------|----------------|
| Centered cross / star / plus | Random off-center features |
| 4 equal quadrants | Voronoi 8-15 irregular cells |
| Regular sine waves | Low-frequency value noise |
| Horizontal stripe layers | Diagonal/random color blobs |
| Symmetric corner motifs | Single asymmetric accent |
| Straight diagonal cracks | Random walk segments |

> Decorative tiles (e.g., `tile_brick`) **may** use geometric patterns, but only when explicitly designed as architecture, not as terrain.

#### 3. Multi-Tier Color Distribution
Each pixel sampled by probability bucket:
- **70%** main color (palette base)
- **15%** dark accent (-1 palette step)
- **10%** light accent (+1 palette step)
- **5%**  emphasis color (rare highlight/feature)

#### 4. Low-Frequency Value Noise (Required)
For natural color variation, use **value noise + cosine interpolation**:
```python
nodes = [[rng.uniform(-1, 1) for _ in range(gw)] for _ in range(gh)]
# CRITICAL: wrap edges for seamless tiling
for row in nodes: row[gw-1] = row[0]
nodes[gh-1] = list(nodes[0])
# Then cosine-lerp at each pixel
```
Recommended scales:
- Main blob: `8~16 px` per node (large irregular regions)
- Detail: `3~6 px` per node (subtle variation)
- Combine 2 octaves for richer texture

#### 5. Seamless Tiling (4-Edge Wrap) ⛔
Tile must repeat without visible seams. Two enforcement methods:
- **Modulo coordinates**: `img.putpixel((x % W, y % H), color)`
- **Wrap noise nodes**: last row/col equals first
- **Test**: Place `2×2` instances side-by-side; no visible borders

#### 6. Sparse Feature Points (≤ 1% of pixels)
Cracks, mineral veins, moss spots, water droplets, etc:
- **Random-walk paths** for cracks (short, intermittent, never straight)
- **Scattered points** (not clustered, not aligned)
- **Total feature pixels ≤ 1%** of canvas area
- **Forbidden**: Continuous straight lines crossing the tile

#### 7. Low-Noise Visual Coherence
Terrain tiles must feel calm and continuous when shown full-screen:
- **Noise rule**: Avoid salt-and-pepper noise, snow-like white speckles, or evenly scattered bright dots.
- **Highlight rule**: White / near-white pixels are forbidden for ground and underground tiles unless explicitly requested; use warm ochre, muted gray, or one-step lighter palette colors instead.
- **Continuity rule**: Prefer broad, low-frequency color regions and short soft bands over per-pixel randomness.
- **Pixel style rule**: Keep hard pixel edges and readable clusters; do not blur, smear, or use anti-aliased gradients.
- **Ink-gongbi rule**: For this project, terrain should stay in restrained ink-and-gongbi tones: muted earth, sand, jade, water, gray ink; no neon colors or high-contrast glitter.

#### 8. Edge Color Continuity
Edges within `±1 palette step` of interior. Avoid:
- ❌ Black border line around the tile (creates grid effect when tiled)
- ❌ Drastically different color in 1-pixel border
- ✅ Same color distribution on edges as interior

#### 9. Mandatory Validation
Before declaring done, verify:
- [ ] Place 4 copies in `2×2` grid → no seams visible
- [ ] Compare with adjacent tiles (e.g., grass + dirt) → color transition feels natural
- [ ] No symmetric features (rotate 90° / flip → looks different)
- [ ] Quantized to exact palette (`palette_analyzer.py`)
- [ ] Feature density ≤ 1%
- [ ] No visible white speckle noise when viewed at game fullscreen scale

#### Reference Implementation

See `e:/神谱拾遗/projects/ShenPuShiYi_Scenes_64x64_20260502/gen_tiles_v2.py` for working examples of:
- Voronoi stone path with wrap-distance metric
- Two-octave noise jade with cosine interpolation
- Random-walk cracks for clay/bedrock
- Probability-bucketed multi-tier color distribution

---

### Step 7: Post-processing & Export

🚧 **GATE**: Step 6 complete, all assets pass quality check

```bash
# 1. Post-process assets (quantize, clean borders, index colors)
python ${SKILL_DIR}/scripts/finalize_assets.py <project_path>

# 2. Pack sprite sheets
python ${SKILL_DIR}/scripts/sprite_sheet.py <project_path>

# 3. Export final package
# Output:
#   exports/<project_name>_<timestamp>.zip
#   ├── sprites/           ← Individual PNGs
#   ├── sheets/            ← Packed sprite sheets
#   ├── palettes/          ← Palette files (GPL/PAL/ACT)
#   └── manifest.json      ← Asset manifest with metadata
```

**Export formats**:
| Format | Description |
|--------|-------------|
| Individual PNGs | One file per asset/animation frame |
| Sprite sheets | Packed grid with manifest |
| Palette files | GPL / PAL / ACT format |
| Asset manifest | JSON with size, palette, animation metadata |

---

## Role Switching Rules

| Phase | Active Role | Reference File |
|-------|------------|---------------|
| Step 1-3 | Coordinator | This file |
| Step 4 | Strategist | `references/strategist.md` |
| Step 5 | Image_Generator (optional) | `references/image-generator.md` |
| Step 6 | Executor | `references/executor-pixel.md` |
| Step 7 | Post-processor | This file + `references/shared-standards.md` |

**Switching protocol**: Announce role switch with `[Role Switch: <Role>]` before starting the phase.
