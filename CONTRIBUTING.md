# Contributing to Pixel Asset Master

Thank you for your interest in contributing! This guide will help you get started.

## Ways to Contribute

- **Palettes** — New pixel art palettes or palette metadata
- **Sprite templates** — Character, tile, item, UI, effect, or background layouts
- **Scripts** — Improvements to validation, post-processing, and sprite sheet export
- **Docs** — Clarifications, translations, or new usage guides
- **Bug reports** — Reproducible issues with clear descriptions
- **Ideas** — Feature requests and design suggestions

## Getting Started

### Prerequisites

- **Python 3.8+** — required for the helper scripts
- **Pillow** — installed through `requirements.txt`

### Setup

```bash
git clone <your-repository-url>
cd pixel-asset-master-skills
pip install -r requirements.txt
```

## Before You Open a PR

To keep the project focused and easy to maintain:

- **Tiny fixes** — open an issue if the maintainer can apply the fix faster than reviewing a PR
- **Focused bug fixes** — PRs are welcome when the fix is self-contained and includes local verification
- **Substantial features** — open an issue first to discuss fit and direction
- **Structural changes** — discuss first; the project deliberately stays close to its skill-based shape

## What We Accept / What We Don't

**Welcome:**

- Bug fixes with clear reproduction steps
- New palettes, size presets, or sprite templates
- Documentation clarifications and translations
- Validation improvements that stay within the declared pixel art constraints
- Post-processing improvements for generated assets

**Not a fit by default:**

- Requiring `uv`, `poetry`, or another package manager as the official install path
- Adding CI, test frameworks, pre-commit hooks, or linting infrastructure without prior discussion
- Repackaging the skill as a SaaS, desktop app, or installer
- Large-scale renames or broad cosmetic reformatting unrelated to a real fix
- Committing generated `projects/`, exports, or private reference images

## Contribution Workflow

1. **Fork** the repository and create a branch from `main`
2. **One PR, one thing** — keep each PR focused on a single concern
3. **Write a useful PR description** — explain what changed and why
4. **Test locally** before submitting
5. **Do not overstate** — if your PR claims tests or behavior changes, make sure the diff actually contains them

## Local Verification

```bash
python skills/pixel-asset-master/scripts/project_manager.py --help
python skills/pixel-asset-master/scripts/palette_analyzer.py --help
python skills/pixel-asset-master/scripts/asset_validator.py --help
python skills/pixel-asset-master/scripts/finalize_assets.py --help
python skills/pixel-asset-master/scripts/sprite_sheet.py --help
```

## Pixel Asset Guidelines

If your contribution involves generated images or example assets:

- Keep pixel edges crisp
- Avoid anti-aliasing unless explicitly documented as intentional
- Keep palette usage clear and reproducible
- Prefer small, reviewable example files
- Do not include private or copyrighted reference images unless you have the right to publish them

## Reporting Bugs

Open an issue and include:

- A clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Environment details, including OS and Python version
- The relevant project structure or `spec_lock.md` excerpt, if applicable

## Code of Conduct

Please read and follow our [Code of Conduct](./CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](./LICENSE).
