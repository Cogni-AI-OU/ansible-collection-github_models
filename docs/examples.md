# Examples for cogni_ai.github_models

## Using ai_inference_chat

### Basic Prompt

```yaml
- name: Ask DeepSeek a question
  cogni_ai.github_models.ai_inference_chat:
    prompt: "Explain Ansible collections in one sentence."
  register: result

## Example Playbooks

You can find complete example playbooks in the `playbooks/` directory:

- `example_one_shot.yml`: Basic single prompt example.
- `example_multi_turn.yml`: Multi-turn conversation example.
- `example_persistent_history.yml`: Demonstrates how to maintain state between tasks.

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

## Example Playbooks

You can find complete example playbooks in the `playbooks/` directory:

- `example_one_shot.yml`: Basic single prompt example.
- `example_multi_turn.yml`: Multi-turn conversation example.
- `example_persistent_history.yml`: Demonstrates how to maintain state between tasks.
```
