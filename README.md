# Common Project: One Concept a Day

**[Visit the Website](https://mschwar.github.io/common-project/)** | **Progress: 5 of 50 concepts completed**

## Overview

A collection of PhD-level concepts explained in kindergarten-simple language. The site shows one concept per day, cycling through 50 based on the day of year. The first five entries are fully written; the rest are placeholders so we can perfect the UX first.

## Live Site

Live preview features the **Emergent Complexity** card (Day 4) for iteration. Daily rotation will resume once more entries are complete.

Features:
- Featured card display (temporarily fixed)
- Minimal layout focused on one concept at a time
- Mobile-responsive design
- Code block support for visual examples

## Repository Structure

- `/docs/` - GitHub Pages site (served)
  - `index.html` - Minimal single-page display
  - `css/style.css` - Layout and typography
  - `js/script.js` - Daily cycling logic
  - `data/concepts.json` - Concepts data (first 5 filled, 6-50 placeholders)
  - `full-index.md` - Legacy outline index
- `/entries/` - Original markdown source files
- `/scripts/` - Automation tools
- `/index.html` - Local mirror of the Pages landing page

## Setup

GitHub Pages serves from `/docs` on the `main` branch. No build step required.

## License

MIT License - Matthew Schwartz
