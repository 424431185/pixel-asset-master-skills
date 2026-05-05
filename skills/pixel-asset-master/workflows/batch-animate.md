---
description: Batch generate animation frames for existing static sprites
---

# Batch Animate Workflow

Standalone workflow for adding animation frames to existing static pixel art sprites.

## Steps

1. **Identify Assets to Animate**
   - Read `spec_lock.md` for declared animation requirements
   - List all assets that need animation but only have static frames
   - Confirm with user which animations to generate

2. **Define Animation Specs**
   For each asset:
   - Animation name (idle / walk / attack / etc.)
   - Frame count
   - FPS
   - Loop or one-shot
   - Key poses (describe each frame's pose/action)

3. **Generate Frames**
   - Use each static sprite as the base/reference
   - Generate animation frames sequentially
   - Maintain consistent palette, size, and style
   - Keep silhouette readable in every frame

4. **Validate Frames**
   ```bash
   python scripts/asset_validator.py <project_path>
   ```
   - All frames same dimensions
   - All colors in palette
   - No anti-aliasing
   - Frame count matches spec

5. **Name and Organize**
   - Follow naming convention: `<asset>_<animation>_<frame>.png`
   - Place in correct `assets/<category>/` directory

6. **Update spec_lock.md**
   - Add animation entries to per-asset specs

## Animation Generation Guidelines

- **Idle**: Subtle movement (breathing, bobbing, blinking). 2-4 frames.
- **Walk**: Full walk cycle. 4-6 frames. Foot contact → passing → contact.
- **Run**: Lean forward, faster stride. 4-6 frames.
- **Attack**: Wind-up → strike → recovery. 3-6 frames.
- **Hurt**: Flash/recoil. 2-3 frames.
- **Die**: Collapse/fade. 4-6 frames.
- **Cast**: Charge → release. 4-6 frames.

## Frame Consistency Rules

- All frames of same animation: identical canvas size
- Character anchor point (feet position) stays consistent across frames
- Palette subset stays the same across all frames
- No new colors introduced mid-animation
