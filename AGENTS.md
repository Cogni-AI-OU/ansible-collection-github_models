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

# Run unit tests
python -m pytest tests/unit

# Syntax check
molecule syntax
```

## Related Prompts or Skills (load when relevant)

- **ansible**: Conventions, idempotency, and linting for Ansible content.
- **molecule**: Molecule testing workflows for Ansible roles.
- **git**: Guide for using git with non-interactive, safe operations.

## AI Agents Module (`ai_agents`)

Autonomous agents using this module should be aware of the following:

- **SDK Requirement**: Requires `azure-ai-agents` package.
- **Authentication**: Uses `StaticTokenCredential` to pass the GitHub token to the Azure SDK. It falls back to `GITHUB_TOKEN` or `GH_TOKEN`.
- **Endpoint Support**: The default endpoint `https://models.inference.ai.azure.com` currently returns `api_not_supported` for the Agents API. When encountering this, do not attempt workarounds; either use a compatible Azure AI Foundry endpoint or stick to `ai_inference_chat`.
- **Response Extraction**: The module uses `order="desc"` when listing messages and breaks on the first assistant/agent message to reliably retrieve the latest response.
- **Validation**: Exactly one of `prompt` or `messages` is required.
