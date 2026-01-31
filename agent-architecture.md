# Architecture and Rules for the Common Projects Agent

## Architecture Overview
- **Modular Design**: Agent as a simple pipeline: Input (concept from CSV) → Generation (structured Markdown) → Output (file commit) → Update (index/connections).
- **Tech Stack** (suggested for automation):
  - Language: Python (for scripting agent calls).
  - AI: Grok API or similar for content generation.
  - Storage: Git repo for versioning; CSV for idea queue.
  - Tracking: A `progress.log` or JSON file to mark completed concepts and connections.
- **Flow**:
  1. Read next concept from `ideas.csv` (filter unused).
  2. Prompt AI with instructions + concept.
  3. Validate output: Check format, word count, accuracy.
  4. Write to `/entries/`, update `/index.md` (e.g., add hyperlinks).
  5. Git commit/push.
- **Scalability**: Start manual; script for daily cron job. Add user submissions via PRs.

## Rules
- **Consistency**:
  - Always use the exact 5-section format.
  - Tone: Curious, empowering—no lecturing.
  - Length: 200-400 words total.
  - Analogies: Everyday (toys, food, nature); inspired by videos (incremental builds, problem-solving logic).
- **Content Rules**:
  - **Simplicity**: Break into steps: Problem → Simple fix → Refined solution → Emergent insight.
  - **Depth**: Include key nuances (e.g., for punctuated equilibrium: bursts vs. gradualism).
  - **Connections**: Mandatory; aim for emergent web (e.g., link probability to Bayesian to foraging).
  - **Accuracy**: Fact-based; cite sources internally if debated (e.g., "Gould's spandrels").
  - **Inclusivity**: Assume good intent; politically neutral claims if substantiated.
- **Constraints**:
  - No external tools unless for research (e.g., if concept needs update).
  - Avoid visuals in text; note if needed.
  - Error Handling: If concept unclear, skip and log.
- **Evolution**:
  - After 50, expand CSV via suggestions.
  - Metrics: Track engagement (stars, issues) to prioritize themes.

This ensures the repo grows organically, like emergent complexity from simple rules.