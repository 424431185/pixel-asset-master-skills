# Execution Lock

## canvas
- base_size: 32x32
- tile_size: 32x32
- format: RGBA PNG

## palette
- name: <palette_name>
- colors:
  - #000000
  - <...all palette hex values>

## style
- sub_style: outlined
- outline_color: #000000
- shading: 3-tone
- dithering: none
- light_direction: top-left

## per_sprite_budget
- max_colors: 16

## assets
- characters:
  - name: <asset_name>
    size: 32x32
    colors: <subset or "all">
    animations: <list or "none">
- tiles:
  - name: <asset_name>
    size: 32x32
    colors: <subset or "all">
    animations: <list or "none">
- items:
  - name: <asset_name>
    size: 16x16
    colors: <subset or "all">
    animations: <list or "none">
- ui:
  - name: <asset_name>
    size: variable
    colors: <subset or "all">
    animations: <list or "none">
- effects:
  - name: <asset_name>
    size: 32x32
    colors: <subset or "all">
    animations: <list or "none">
- backgrounds:
  - name: <asset_name>
    size: 256x144
    colors: <subset or "all">
    animations: <list or "none">

## forbidden
- Anti-aliasing
- Gradient fills
- Partial opacity (1-254 alpha)
- Colors outside declared palette
- Sub-pixel rendering
