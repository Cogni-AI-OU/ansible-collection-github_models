# AGENTS.md

Persistent single-source truth for autonomous agent behavior.

## Key Files & Context Injection

- Project overview & install: [README.md](README.md)
- Agent configuration & conventions: [.github/copilot-instructions.md](.github/copilot-instructions.md)
- Workflow navigation: [.tours/getting-started.tour](.tours/getting-started.tour)
- Latest org baseline: <https://github.com/Cogni-AI-OU/.github/blob/main/AGENTS.md>

Read and merge these when operating inside corresponding sub-directories (order = precedence):

- [`.github/AGENTS.md`](.github/AGENTS.md)
- Any `AGENTS.md` or `SKILL.md` in ancestor, then current directory tree

## Common Tasks

### Testing

```bash
# Run Molecule tests
molecule test

# Syntax check
molecule syntax
```

## Related Prompts or Skills (load when relevant)

- **ansible**: Conventions, idempotency, and linting for Ansible content.
- **molecule**: Molecule testing workflows for Ansible roles.
- **git**: Guide for using git with non-interactive, safe operations.
