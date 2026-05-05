---
description: Create a custom pixel art color palette
---

# Create Palette Workflow

Standalone workflow for creating a custom pixel art color palette.

## Steps

1. **Gather Requirements**
   - Ask user for palette purpose (game genre, mood, reference)
   - Ask for target color count (8 / 16 / 32 / 48 / 64)
   - Ask if they have reference images

2. **Extract or Design Colors**
   - If reference images provided:
     ```bash
     python scripts/palette_analyzer.py extract <image> --count <N>
     ```
   - If no references: design palette from scratch based on genre/mood

3. **Validate Palette**
   - Check contrast ratios between adjacent shades
   - Ensure hue variety (not all same hue)
   - Verify readability at target sprite size
   - Minimum 3 shades per hue (highlight / base / shadow)

4. **Save Palette**
   - Add to `templates/palettes/palettes_index.json`
   - Generate GPL file in `templates/palettes/examples/`
   - Update spec_lock.md if within a project

5. **Preview**
   - Generate a small test sprite using the new palette
   - Show to user for approval

## Palette Design Rules

- **Hue coverage**: Include warm (red/orange/yellow), cool (blue/purple), and neutral (gray/brown) hues
- **Value range**: At least 3 values per hue (light / mid / dark)
- **Saturation**: Include both saturated and desaturated variants
- **Contrast**: Adjacent shades must differ by ≥30 in RGB distance
- **Skin tones**: If characters needed, include at least 2 skin tone ranges
- **Background colors**: Include colors suitable for backgrounds (lower saturation)
