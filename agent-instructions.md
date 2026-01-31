# Instructions for the Agent Building Common Projects Entries

## Purpose
You are an AI agent (e.g., powered by Grok or similar) tasked with generating daily entries for the Common Projects repository. Each entry explains a PhD-level concept in kindergarten-simple terms, without losing nuance. Draw from the `ideas.csv` list, one per day/entry.

## Core Guidelines
- **Input**: Select the next unused concept from `ideas.csv` (track via a simple log or git commits).
- **Output**: A single Markdown file in `/entries/` named `day-XXX-concept-title.md` (e.g., `day-001-probability-basics.md`). Keep under 500 words.
- **Format** (strictly follow):
  1. **Concept Title**: Bold and clear.
  2. **Kindergarten Explanation**: Explain as if to a 5-year-old. Use analogies (e.g., coin flips for probability). Start with the problem/puzzle, build incrementally like classic explainer videos (differential steering: spokes → gears; servo: coarse → fine alignment).
  3. **Why It Matters**: One sentence on heuristics or real-world impact.
  4. **Connections Unlocked**: Link to 1-3 previous/future concepts (e.g., "Builds on Power Laws (Day 3)").
  5. **Quick Exercise**: A simple prompt to apply the idea.
- **Style**:
  - Clean, uncluttered: Short sentences, no jargon (define if used).
  - Preserve complexity: Layer steps to show "why" it works, not just "what."
  - Inspirations: Mirror videos like "How Differential Steering Works" (problem-first, visual buildup) or "Central Station Fire-Control" (feedback loops via diagrams/circuits).
- **Process**:
  1. Research lightly if needed (use your knowledge; no external tools unless specified).
  2. Ensure accuracy: Base on established science (e.g., debunk myths in Lamarckian evolution).
  3. Update `/index.md` with new links/connections after generation.
  4. Commit to git: Message like "Add Day XXX: Concept Title".
- **Edge Cases**:
  - If concept is visual (e.g., chaos theory), suggest a simple ASCII diagram or note for future image.
  - Build progressively: Early entries foundational (stats), later more advanced (evolution, systems).
- **Sustainability**: Generate one per "day" (or on demand). If automating, use a script to call the agent API.

Follow architecture/rules in `agent-architecture.md` for consistency.