# <Project Name> - Design Spec

> Human-readable design narrative. Machine-readable contract: spec_lock.md.

## I. Project Information

| Item | Value |
| ---- | ----- |
| **Project Name** | |
| **Canvas Size** | |
| **Asset Count** | |
| **Art Style** | |
| **Target Platform** | |
| **Color Palette** | |
| **Created Date** | |

---

## II. Canvas Specification

| Property | Value |
| -------- | ----- |
| **Base sprite size** | WxH |
| **Tile size** | WxH |
| **Background size** | WxH |
| **Transparency** | Alpha channel (RGBA) |

---

## III. Color Palette

### Palette Name: <name>

| Index | HEX | Role |
| ----- | --- | ---- |
| 0 | | Transparent |
| 1 | | |
| 2 | | |
| ... | | |

### Palette Usage Rules

- All sprite pixels MUST use colors from this palette
- Per-sprite color budget: <N> colors (excl. transparency)
- Light source direction: <top-left / top / etc.>

---

## IV. Art Style Definition

| Property | Value |
| -------- | ----- |
| **Sub-style** | Outlined / Outlineless / Dithered / Cel-shaded / Textured |
| **Outline color** | (if outlined) |
| **Shading depth** | Flat / 2-tone / 3-tone / Dithered |
| **Dithering** | None / Ordered / Selective |
| **Light direction** | Top-left (default) |

---

## V. Asset List

### Characters

| Asset | Size | Colors | Animation | Description | Priority |
| ----- | ---- | ------- | --------- | ----------- | -------- |
| | | | | | | |

### Tiles

| Asset | Size | Colors | Animation | Description | Priority |
| ----- | ---- | ------- | --------- | ----------- | -------- |
| | | | | | | |

### Items

| Asset | Size | Colors | Animation | Description | Priority |
| ----- | ---- | ------- | --------- | ----------- | -------- |
| | | | | | | |

### UI

| Asset | Size | Colors | Animation | Description | Priority |
| ----- | ---- | ------- | --------- | ----------- | -------- |
| | | | | | | |

### Effects

| Asset | Size | Colors | Animation | Description | Priority |
| ----- | ---- | ------- | --------- | ----------- | -------- |
| | | | | | | |

### Backgrounds

| Asset | Size | Colors | Animation | Description | Priority |
| ----- | ---- | ------- | --------- | ----------- | -------- |
| | | | | | | |

---

## VI. Animation Specification

| Asset | Animation | Frames | FPS | Loop | Notes |
| ----- | --------- | ------ | --- | ---- | ----- |
| | | | | | | |

---

## VII. Technical Constraints

- No anti-aliasing
- No gradient fills (use dithering)
- No partial opacity (fully opaque or transparent only)
- All colors from declared palette
- Consistent light direction across all assets
- Pixel-perfect at declared size (no scaling artifacts)

---

## VIII. Platform Export Notes

| Platform | Special Requirements |
| -------- | ------------------- |
| | |
