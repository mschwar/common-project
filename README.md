# Common Project: One Concept a Day

**[Visit the Website](https://matthew41785338.github.io/common-projects/)** | **50 concepts complete**

## Overview

A collection of PhD-level concepts explained in kindergarten-simple language. Each entry distills complex ideas from science, statistics, biology, evolution, and systems thinking into bite-sized explanations.

The website displays one concept per day, cycling through all 50 based on the day of year. Minimal, serene, no clutter.

Topics span: probability, game theory, chaos, evolution, ecology, thermodynamics, and more.

## Live Site

The page shows today's concept automatically. Return tomorrow for the next one.

Features:
- Daily rotation (day of year modulo 50)
- Full explanation with connections to other concepts
- Mobile-responsive design

## Repository Structure

- `/docs/` - GitHub Pages site
  - `index.html` - Minimal single-page display
  - `concepts.json` - All 50 concepts with full content
  - `script.js` - Daily cycling logic
  - `styles.css` - Clean, minimal styling
- `/entries/` - Original markdown source files
- `/scripts/` - Automation tools

## Setup

GitHub Pages serves from `/docs` folder on `main` branch. No build step required.

## License

MIT License - Matthew Schwartz
