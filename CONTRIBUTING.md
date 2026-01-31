# Contributing to Common Projects

Thank you for your interest in contributing! This project aims to make PhD-level concepts accessible to everyone.

## How to Contribute

### Suggest New Concepts

1. Open an issue with the concept name and why it's important
2. Include the general theme (Statistics, Biology, Systems, etc.)
3. Optionally suggest connections to existing concepts

### Submit Entry Pull Requests

1. Fork the repository
2. Create a new entry following the template in `/templates/entry-template.md`
3. Ensure your entry follows these guidelines:
   - **5-section format**: Title, Kindergarten Explanation, Why It Matters, Connections, Quick Exercise
   - **Word count**: 200-400 words total
   - **Tone**: Curious and empowering, like explaining to a friend
   - **Analogies**: Use everyday examples (toys, food, nature)
   - **Accuracy**: Base on established science
4. Run validation: `python scripts/validate_entry.py your-entry.md`
5. Submit PR with clear description

### Entry Format Requirements

Each entry must include:

1. **Concept Title**: Clear and bold
2. **Kindergarten Explanation**: Explain as if to a 5-year-old, start with the problem
3. **Why It Matters**: One sentence on real-world impact
4. **Connections Unlocked**: Link to 1-3 related concepts
5. **Quick Exercise**: Simple prompt to apply the idea

### Style Guidelines

- **Simplicity**: Short sentences, minimal jargon
- **Depth**: Show *why* it works, not just *what* it is
- **Incremental**: Build from problem → simple solution → refined insight
- **Connections**: Link to other entries to build the knowledge web

### Validation Checklist

Before submitting:

- [ ] Entry follows 5-section format
- [ ] Word count is 200-400 words
- [ ] Analogies are clear and relatable
- [ ] Connections reference existing or planned concepts
- [ ] Tone is friendly and accessible
- [ ] Facts are accurate and sourced when needed
- [ ] File named correctly: `day-XXX-concept-title.md`

## Questions?

Open an issue for clarification on guidelines or to discuss potential contributions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
