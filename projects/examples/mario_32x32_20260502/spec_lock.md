# spec_lock.md — NES Mario Walk

> Machine-readable execution contract.

## Project

- **name**: mario
- **size**: 32x32
- **date**: 20260502
- **palette**: NES Classic

## Canvas

- **frame_width**: 32
- **frame_height**: 32
- **facing**: 4-dir (down/up/left/right)

## Assets

### character_mario

- **category**: characters
- **canvas**: 32x32
- **max_colors**: 8
- **actions**:
  - walk_down: 3 frames
  - walk_up: 3 frames
  - walk_left: 3 frames
  - walk_right: 3 frames

## Sprite Sheet Layout

- **file**: mario_walk.png
- **total_frames**: 12
- **rows**: 4 (down/up/left/right)
- **cols**: 3
- **sheet_size**: 96x128
