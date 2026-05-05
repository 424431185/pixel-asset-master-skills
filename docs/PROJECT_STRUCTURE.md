# Project Structure

本文档记录 `pixel-asset-master-skills` 的 GitHub 仓库结构约定。

## 顶层结构

```text
.
├── README.md
├── README_CN.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── requirements.txt
├── docs/
│   └── PROJECT_STRUCTURE.md
├── index.html
├── projects/
│   ├── README.md
│   └── examples/
│       └── ancient_scholar_256x256_20260502/  (removed)
│       └── mario_32x32_20260502/
└── skills/
    └── pixel-asset-master/
```

## Skill 结构

```text
skills/pixel-asset-master/
├── SKILL.md
├── references/
│   ├── executor-pixel.md
│   ├── shared-standards.md
│   └── strategist.md
├── scripts/
│   ├── README.md
│   ├── asset_validator.py
│   ├── finalize_assets.py
│   ├── palette_analyzer.py
│   ├── project_manager.py
│   └── sprite_sheet.py
├── templates/
│   ├── design_spec_reference.md
│   ├── spec_lock_reference.md
│   ├── palettes/
│   │   └── palettes_index.json
│   ├── sizes/
│   │   └── sizes_index.json
│   └── sprites/
│       └── sprites_index.json
└── workflows/
    ├── batch-animate.md
    └── create-palette.md
```

## 目录职责

- **`skills/pixel-asset-master/SKILL.md`**：AI skill 的主入口，定义完整像素素材生产流水线。
- **`references/`**：拆分角色职责和执行标准，避免主入口过长。
- **`scripts/`**：辅助命令行工具，用于项目初始化、调色板分析、素材校验和导出。
- **`templates/`**：调色板、尺寸、精灵布局和规格文件模板。
- **`workflows/`**：可独立调用的补充流程。
- **`docs/`**：仓库维护文档。

## 生成内容边界

以下内容属于本地运行产物，不建议提交 Git：

- `projects/*`（但保留 `projects/README.md` 和 `projects/examples/` 作为示例）
- `exports/`
- 打包文件，例如 `*.zip`、`*.tar.gz`
- 临时文件，例如 `*.tmp`、`*.bak`
- 本地环境文件，例如 `.env`、`.venv/`

## 架构整理记录

本次整理将项目明确为“仓库级文档 + 单 skill 包”的形式：

- 根目录只保留 GitHub 展示、依赖和协作文件。
- skill 的可执行主体仍保留在 `skills/pixel-asset-master/`。
- 生成项目统一输出到根目录 `projects/`，并由 `.gitignore` 排除。
- 根 `README.md` 使用产品页式结构，包含徽章、语言入口、Quick Start、Documentation 表和贡献入口。
- 新增 `README_CN.md`，与英文 README 保持同等导航能力。
- 根 `requirements.txt` 转发到 `skills/pixel-asset-master/requirements.txt`，保证 skill 可独立安装依赖。
- 新增 `SECURITY.md` 与 `CODE_OF_CONDUCT.md`，补齐开源协作文件。
- 新增 `index.html` 作为项目展示页，含樱花树序列帧动画、古风小生多动作精灵图动画和全页花瓣粒子。
- `projects/examples/` 保留示例项目（含 design_spec、spec_lock、精灵图和 manifest），供用户参考。
- `sizes_index.json` 扩展至 2048x2048，新增 High-Res Pixel 和 Cinematic Pixel 风格。
- `sprites_index.json` 人物模板新增 `facing_directions`、`common_actions`、`recommended_sizes`、`actions` 字段。
- `SKILL.md` Step 4 六项确认第 6 项扩展为动画详细确认（面朝方向 + 动作列表 + 每动作帧数）。
