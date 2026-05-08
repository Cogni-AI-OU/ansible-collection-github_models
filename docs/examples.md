# Examples for cogni_ai.github_models

## Using ai_inference_chat

### Basic Prompt

```yaml
- name: Ask DeepSeek a question
  cogni_ai.github_models.ai_inference_chat:
    prompt: "Explain Ansible collections in one sentence."
  register: result

- name: Show response
  debug:
    msg: "{{ result.message }}"
```

### Multi-turn Conversation

```yaml
- name: Chat with context
  cogni_ai.github_models.ai_inference_chat:
    system_prompt: "You are a helpful assistant."
    messages:
      - role: user
        content: "What is the capital of France?"
      - role: assistant
        content: "The capital of France is Paris."
      - role: user
        content: "And its population?"
  register: result
```
