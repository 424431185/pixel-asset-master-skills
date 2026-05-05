# Pixel Asset Master — 用 AI 从游戏设计稿生成 2D 像素游戏素材

[![Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB.svg)](https://www.python.org/)

[English](./README.md) | 中文

输入游戏概念、风格方向或参考图片，得到结构化的像素素材项目：角色、瓦片、物品、UI、特效、背景、动画帧、精灵图和导出元数据。

> **工作方式** — Pixel Asset Master 是一个面向 AI IDE 的 workflow skill。你在聊天面板中描述需求，AI 会按流程确认风格约束，并完成项目初始化、素材规划、生成、校验和导出。

> **本地优先** — 项目文件和生成素材默认保存在本地 `projects/`。是否调用外部 API，取决于你接入的 AI 工具或图片生成服务。

Pixel Asset Master 关注：

- **游戏可用结构**：素材按 `characters`、`tiles`、`items`、`ui`、`effects`、`backgrounds` 分类。
- **严格视觉契约**：`spec_lock.md` 记录画布尺寸、调色板、风格、颜色预算和禁用渲染方式。
- **可复用模板**：内置调色板、尺寸预设和精灵布局参考。
- **校验工具**：脚本辅助检查调色板、颜色数量、图片格式和精灵图导出。
- **适合 AI 执行**：分阶段确认，降低提示词模糊性，让长流程素材生成更一致。

---

## 快速开始

### 1. 环境要求

| 依赖 | 是否必须 | 用途 |
|------|:-------:|------|
| Python 3.8+ | ✅ 是 | 运行辅助脚本 |
| Pillow | ✅ 是 | 图片分析、校验、量化和精灵图打包 |

安装依赖：

```bash
pip install -r requirements.txt
```

### 2. 获取项目

**方式 A — 下载 ZIP**：从 GitHub 下载仓库 ZIP 并解压。

**方式 B — Git clone**：

```bash
git clone <your-repository-url>
cd pixel-asset-master-skills
pip install -r requirements.txt
```

### 3. 放入 AI Coding IDE

下载或解压后，请把整个 **`pixel-asset-master-skills/` 文件夹** 作为工作区打开，而不是只打开其中某个文件。

| IDE | 使用方式 |
|-----|----------|
| **Cursor** | `File → Open Folder...` 选择 `pixel-asset-master-skills/`，然后让聊天 Agent 读取 `skills/pixel-asset-master/SKILL.md`。 |
| **Trae** | 将该文件夹作为项目/工作区打开，在聊天中提及 `skills/pixel-asset-master/SKILL.md` 后再提出素材需求。 |
| **Windsurf** | 在 Windsurf 中打开该文件夹，使用 Cascade 聊天，并在开始像素素材任务时引用 `skills/pixel-asset-master/SKILL.md`。 |
| **其他 AI Coding IDE** | 打开仓库根目录，并让 Agent 读取 `skills/pixel-asset-master/SKILL.md`。 |

推荐第一句提示词：

```text
读取 skills/pixel-asset-master/SKILL.md，并帮我创建一个像素素材项目。
```

### 4. 创建像素素材项目

```bash
python skills/pixel-asset-master/scripts/project_manager.py init demo --size 32x32 --palette DB32
```

生成项目会保存在 `projects/`，默认不会提交到 Git。

### 5. 选择生成方式

#### 方式 A — 不使用参考图片

适合只有文字想法、游戏设定、美术方向或剧情描述的情况。

示例提示词：

```text
读取 skills/pixel-asset-master/SKILL.md。
创建一个 64x64、4 方向 RPG 角色精灵图。
风格：水墨工笔像素风。
动作：待机和走路。
不使用参考图。
```

AI 应该执行：

1. 确认风格、尺寸、调色板、面朝方向、动作列表和每个动作帧数。
2. 创建或更新 `projects/<project_name>/design_spec.md`。
3. 创建或更新 `projects/<project_name>/spec_lock.md`。
4. 生成 PNG 素材、动画帧、精灵图和 manifest。

#### 方式 B — 使用参考图片

适合已有角色设定图、瓦片参考、UI 草图、氛围图或游戏截图，并希望生成结果贴近这些参考图的情况。

先导入参考图片：

```bash
python skills/pixel-asset-master/scripts/project_manager.py import-sources projects/demo_32x32_YYYYMMDD path/to/reference.png
```

然后对 AI 说：

```text
读取 skills/pixel-asset-master/SKILL.md。
使用 projects/demo_32x32_YYYYMMDD/images/ 下的图片作为视觉参考。
生成匹配的像素素材，并保持轮廓、配色氛围和风格约束一致。
```

AI 应该先分析参考图，提取风格和调色板约束，再继续完成 spec lock、素材生成、校验和导出流程。

### 6. 校验并导出

```bash
python skills/pixel-asset-master/scripts/project_manager.py validate projects/demo_32x32_YYYYMMDD
python skills/pixel-asset-master/scripts/asset_validator.py projects/demo_32x32_YYYYMMDD
python skills/pixel-asset-master/scripts/finalize_assets.py projects/demo_32x32_YYYYMMDD --all
python skills/pixel-asset-master/scripts/sprite_sheet.py projects/demo_32x32_YYYYMMDD --by-category
```

> **AI 丢失上下文？** 让它读取 `skills/pixel-asset-master/SKILL.md`。

---

## 仓库结构

```text
skills/
└── pixel-asset-master/
    ├── SKILL.md
    ├── requirements.txt
    ├── references/
    ├── scripts/
    ├── templates/
    └── workflows/
```

## 文档

| | 文档 | 说明 |
|---|------|------|
| 📖 | [SKILL.md](./skills/pixel-asset-master/SKILL.md) | 核心 workflow 和执行规则 |
| 🛠️ | [Scripts & Tools](./skills/pixel-asset-master/scripts/README.md) | 脚本用法和命令示例 |
| 🏗️ | [Project Structure](./docs/PROJECT_STRUCTURE.md) | 仓库结构和生成内容边界 |
| 🤝 | [Contributing](./CONTRIBUTING.md) | 贡献范围和流程 |
| 🔐 | [Security](./SECURITY.md) | 安全问题报告方式和范围 |

## 不应提交的内容

- **生成项目**：`projects/`
- **导出包**：`exports/`、`*.zip`、`*.tar.gz`
- **密钥**：`.env`、真实 API Key、Token、私有账号信息

## 参与贡献

见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## License

[MIT](LICENSE)

[⬆ 回到顶部](#pixel-asset-master--用-ai-从游戏设计稿生成-2d-像素游戏素材)
