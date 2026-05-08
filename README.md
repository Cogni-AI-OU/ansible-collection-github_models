# Ansible Collection: cogni_ai.github_models

[![PR Reviews][pr-reviews-image]][pr-reviews-link]
[![License][license-image]][license-link]
[![Check][check-image]][check-link]

This collection provides modules and roles for interacting with GitHub AI Inference Models.

## Modules

- `ai_inference_chat`: Stateless interface for GitHub AI Inference Chat Completions.

## Roles

- `github_models`: Role for setting up and using GitHub Models.

## Installation

To install this collection:

```shell
ansible-galaxy collection install git+https://github.com/Cogni-AI-OU/ansible-collection-github_models.git
```

## Usage

### Using the module

```yaml
- name: Ask a question
  cogni_ai.github_models.ai_inference_chat:
    prompt: "What is Ansible?"
```

## Testing

### Docker

Steps to test collection on Docker containers.

1. Install the current collection by running the following commands in shell:

    ```shell
    ansible-galaxy collection install -r requirements.yml
    jinja2 requirements-local.yml.j2 -D "pwd=$PWD" -o requirements-local.yml
    ansible-galaxy collection install -r requirements-local.yml
    ```

    Alternatively, for development purposes, you can consider using symbolic link, e.g.

    ```shell
    ln -vs "$PWD" ~/.ansible/collections/ansible_collections/cogni_ai/github_models
    ```

2. Ensure Docker service (e.g. Docker Desktop) is running.
3. Run playbook from `tests/`:

    ```shell
    ansible-playbook -i tests/inventory/docker-containers.yml tests/playbooks/docker-containers.yml
    ```

4. Run the verify-tag playbook (stops containers after verification):

  ```shell
  ansible-playbook -i tests/inventory/docker-containers.yml tests/playbooks/tags/verify.yml --tags verify
  ```

### Molecule

To test using Molecule, run:

```shell
molecule test
```

## Development

### Setup

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Install Python dependencies (for devcontainer)
pip install -r .devcontainer/requirements.txt
```

### Testing and Validation

```bash
# Run all pre-commit checks
pre-commit run -a

# Run specific checks
pre-commit run markdownlint -a
pre-commit run yamllint -a
pre-commit run black -a
pre-commit run flake8 -a
```

## AI Agents

This repository provides AI agent configurations for automated development.

### Agent Configuration Files

| File/Directory | Audience | Purpose |
| -------------- | -------- | ------- |
| [AGENTS.md](AGENTS.md) | All agents | Repository-specific guidance and workflows |
| [.github/copilot-instructions.md](.github/copilot-instructions.md) | Copilot | Coding standards and project context |
| [.github/FIREWALL.md](.github/FIREWALL.md) | Maintainers | Firewall allowlist guidance for hosted agents |
| [.github/prompts/](.github/prompts/) | All | Prompt templates (`.md` for VS Code, `.yaml` for GitHub Models) |
| [.github/workflows/](.github/workflows/) | Automation | CI, review, and agent workflows including Cogni AI |
| [.github/workflows/cogni-ai-agent.yml](.github/workflows/cogni-ai-agent.yml) | Cogni AI | Event-driven agent workflow for issues, PRs, and discussions |

See also:

- [`AGENTS.md` file format specification](https://agents.md/)
- [Best practices for using GitHub Copilot](https://gh.io/copilot-coding-agent-tips).

## GitHub Actions

For documentation on GitHub Actions workflows, problem matchers, and CI/CD
configuration, see [.github/workflows/README.md](.github/workflows/README.md).

## Contributing

For contribution guidelines, see [CONTRIBUTING.md](https://github.com/Cogni-AI-OU/.github/blob/main/.github/CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<!-- Named links -->

[pr-reviews-image]: https://img.shields.io/github/issues-pr/Cogni-AI-OU/ansible-collection-github_models?label=PR+Reviews&logo=github
[pr-reviews-link]: https://github.com/Cogni-AI-OU/ansible-collection-github_models/pulls
[license-image]: https://img.shields.io/badge/License-MIT-blue.svg
[license-link]: LICENSE
[check-image]: https://github.com/Cogni-AI-OU/ansible-collection-github_models/actions/workflows/check.yml/badge.svg
[check-link]: https://github.com/Cogni-AI-OU/ansible-collection-github_models/actions/workflows/check.yml
