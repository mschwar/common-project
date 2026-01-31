# Common Project: One Concept a Day

**🌐 [Visit the Website](https://matthew41785338.github.io/common-projects/)** | **📊 Progress: 5 of 50 concepts**

## Overview

This repository hosts "Common Project," a collection of PhD-level concepts explained in kindergarten-simple language. Each entry distills complex ideas from science, statistics, biology, evolution, and systems thinking into bite-sized explanations. The goal: Build heuristics, unlock connections, and reveal emergent patterns like power laws or state changes—one concept at a time.

Inspired by Feynman's teaching style and classic explainer videos (e.g., differential steering or WWII servo systems), we prioritize:

- **Simplicity without losing depth**: Start with real-world problems, use everyday analogies, layer complexity gradually.
- **Daily rhythm**: One entry per day, archived here for easy access
- **Interconnections**: Entries link to each other, forming a web like an "Encyclopedia Galactica" for paradigms and frameworks

This isn't just reading—it's a toolkit for better thinking. Apply concepts to daily life, spot patterns in nature/society, and evolve your mental models.

## Repository Structure

- [`/entries/`](./entries/): Markdown files for each concept (e.g., `day-001-probability-basics.md`)
- [`/docs/`](./docs/): GitHub Pages website (auto-generated from markdown)
- [`/scripts/`](./scripts/): Automation tools for conversion and validation
- [`ideas.csv`](./ideas.csv): Source list of 50 concepts to cover
- [`index.md`](./index.md): Master index with connections and themes
- [`tracking.json`](./tracking.json): Progress tracking

## Quick Start

### View the Website

Visit **[GitHub Pages site](https://matthew41785338.github.io/common-projects/)** to read entries with beautiful formatting.

### Local Development

1. **Clone the repository**

```bash
git clone https://github.com/Matthew41785338/common-projects.git
cd common-projects/common-projects
```

1. **Install dependencies** (optional, for automation)

```bash
pip install -r requirements.txt
```

1. **Validate an entry**

```bash
python scripts/validate_entry.py entries/day-001-probability-basics.md
```

1. **Convert markdown to HTML**

```bash
python scripts/convert_to_html.py
```

1. **Update the index**

```bash
python scripts/update_index.py
```

## How to Contribute

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for detailed guidelines. Quick summary:

1. **Suggest concepts**: Open an issue with your idea
2. **Submit entries**: Follow the template in `/templates/entry-template.md`
3. **Ensure quality**: Use `validate_entry.py` before submitting
4. **Submit PR**: Include clear description of your contribution

## Deployment

The site automatically deploys to GitHub Pages via GitHub Actions when you push to `main`:

- Markdown entries are converted to HTML
- Index is updated with new concepts
- Website is rebuilt and published

Configure GitHub Pages to use the `/docs` folder from the `main` branch.

## Current Progress

✅ **Completed (5 entries):**

- Day 1: Probability Basics
- Day 2: Bayesian Statistics
- Day 3: Power Laws
- Day 4: Emergent Complexity
- Day 5: State Changes

📋 **Up Next:** Optimal Foraging Theory, Life History Theory, and 43 more concepts!

## License & Credits

**License**: MIT  
**Creator**: Matthew Schwartz ([@Matthew41785338](https://twitter.com/Matthew41785338))  
**Last Updated**: January 31, 2026

Contributions welcome! Let's make complex ideas common knowledge. 🧠✨
