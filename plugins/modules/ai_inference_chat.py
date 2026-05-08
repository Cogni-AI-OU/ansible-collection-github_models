#!/usr/bin/python

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
import os

DOCUMENTATION = r"""
---
module: ai_inference_chat
short_description: stateless interface for GitHub AI Inference Chat Completions
description:
    - Provides a stateless interface for GitHub AI Inference Chat Completions.
    - Supports one-shot prompts and multi-turn conversations.
extends_documentation_fragment:
    - cogni_ai.github_models.github_models_auth
options:
    model:
        description: The model to use for completion.
        type: str
        default: "deepseek/DeepSeek-R1"
    prompt:
        description: A single user prompt.
        type: str
    system_prompt:
        description: A system prompt to set the context.
        type: str
    messages:
        description: A list of messages for multi-turn conversations.
        type: list
        elements: dict
        suboptions:
            role:
                description: The role of the message sender.
                type: str
                required: true
                choices: ["system", "user", "assistant"]
            content:
                description: The content of the message.
                type: str
                required: true
    max_tokens:
        description: The maximum number of tokens to generate.
        type: int
    temperature:
        description: The temperature for generation.
        type: float
required_one_of:
    - ["prompt", "messages"]
author:
    - Cogni AI
"""

EXAMPLES = r"""
- name: One-shot prompt
  ai_inference_chat:
    prompt: "Hello, how are you?"
    model: "deepseek/DeepSeek-R1"

- name: Multi-turn conversation
  ai_inference_chat:
    messages:
      - role: system
        content: "You are a helpful assistant."
      - role: user
        content: "What is Ansible?"
"""

RETURN = r"""
message:
    description: The generated message content.
    returned: success
    type: str
    sample: "Ansible is an open-source automation tool."
"""

# The import path for collection
try:
    from ansible_collections.cogni_ai.github_models.plugins.module_utils.ai_inference_common import (
        create_client,
        build_messages,
    )
except ImportError:
    # Fallback for local testing
    try:
        from plugins.module_utils.ai_inference_common import create_client, build_messages
    except ImportError:
        from ai_inference_common import create_client, build_messages


def main():
    module = AnsibleModule(
        argument_spec=dict(
            endpoint=dict(type="str", default="https://models.github.ai/inference"),
            token=dict(type="str", no_log=True, required=False),
            model=dict(type="str", default="deepseek/DeepSeek-R1"),
            prompt=dict(type="str", required=False),
            system_prompt=dict(type="str", required=False),
            messages=dict(
                type="list",
                elements="dict",
                required=False,
                options=dict(
                    role=dict(type="str", required=True, choices=["system", "user", "assistant"]),
                    content=dict(type="str", required=True),
                ),
            ),
            max_tokens=dict(type="int", required=False),
            temperature=dict(type="float", required=False),
        ),
        required_one_of=[["prompt", "messages"]],
        supports_check_mode=True,
    )

    messages_dict = []
    if module.params["system_prompt"]:
        messages_dict.append({"role": "system", "content": module.params["system_prompt"]})
    for m in module.params["messages"] or []:
        messages_dict.append(m)
    if module.params["prompt"]:
        messages_dict.append({"role": "user", "content": module.params["prompt"]})

    if module.check_mode:
        module.exit_json(
            changed=False,
            msg="Check mode: no request sent",
            model=module.params["model"],
            messages=messages_dict,
        )

    token = module.params["token"] or os.getenv("GITHUB_TOKEN")
    if not token:
        module.fail_json(msg="token is required or set GITHUB_TOKEN")

    try:
        client = create_client(module.params["endpoint"], token)
        # Use common utility to build SDK message objects
        sdk_messages = build_messages(
            raw_messages=module.params["messages"],
            system_prompt=module.params["system_prompt"],
            prompt=module.params["prompt"],
        )

        kwargs = {
            "messages": sdk_messages,
            "model": module.params["model"],
        }

        if module.params["max_tokens"] is not None:
            kwargs["max_tokens"] = module.params["max_tokens"]

        if module.params["temperature"] is not None:
            kwargs["temperature"] = module.params["temperature"]

        response = client.complete(**kwargs)

        module.exit_json(
            changed=False,
            message=response.choices[0].message.content,
            model=module.params["model"],
            messages=messages_dict,
        )
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
