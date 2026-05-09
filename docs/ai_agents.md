# ai_agents module

Interface for AI Agents using Azure AI Agents SDK.

## Description

- Provides an interface for creating and interacting with AI Agents via the azure-ai-agents SDK.
- Can act like create_and_process handling agent creation, thread creation, sending messages, and waiting for the response.
- Supports universally both stateless one-shots (creates new agent & thread on the fly) and stateful conversation by providing `thread_id` and `agent_id`.
- Leverages the `azure-ai-agents` SDK.

## Options

| Parameter | Description | Required | Default |
| --- | --- | --- | --- |
| endpoint | The endpoint for the AI Inference service. | No | `https://models.github.ai/inference` |
| token | The GitHub token for authentication. | No | (Uses GITHUB_TOKEN env var) |
| model | The model to use for completion. | Required if agent_id is not provided | `microsoft/phi-4-mini-reasoning` |
| agent_id | The ID of an existing agent. If not provided, a new agent will be created. | No | |
| thread_id | The ID of an existing thread. If not provided, a new thread will be created. | No | |
| name | The name of the agent to create. | No | |
| instructions | The instructions for the agent to follow. | No | |
| prompt | A single user prompt. | One of prompt/messages | |
| messages | A list of messages to add to the thread. | One of prompt/messages | |

## Requirements

- `azure-ai-agents` Python package.
- `azure-core` Python package.
- `azure-identity` Python package (if using specific credentials).
