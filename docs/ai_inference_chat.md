# ai_inference_chat module

Stateless interface for GitHub AI Inference Chat Completions.

## Description

- Provides a stateless interface for GitHub AI Inference Chat Completions.
- Supports one-shot prompts and multi-turn conversations.
- Leverages the `azure-ai-inference` SDK.

## Options

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| endpoint | The endpoint for the AI Inference service. | No | https://models.github.ai/inference |
| token | The GitHub token for authentication. | No | (Uses GITHUB_TOKEN env var) |
| model | The model to use for completion. | No | deepseek/DeepSeek-R1 |
| prompt | A single user prompt. | One of prompt/messages | |
| system_prompt | A system prompt to set the context. | No | |
| messages | A list of messages for multi-turn conversations. | One of prompt/messages | |
| max_tokens | The maximum number of tokens to generate. | No | |
| temperature | The temperature for generation. | No | |

## Requirements

- `azure-ai-inference` Python package.
