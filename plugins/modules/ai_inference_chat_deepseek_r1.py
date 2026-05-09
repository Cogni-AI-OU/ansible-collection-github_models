#!/usr/bin/python

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule, env_fallback

DOCUMENTATION = r"""
---
module: ai_inference_chat_deepseek_r1
short_description: stateless interface for deepseek/deepseek-r1
description:
    - Provides a stateless interface for deepseek/deepseek-r1.
    - Supports one-shot prompts and multi-turn conversations.
extends_documentation_fragment:
    - cogni_ai.github_models.github_models_auth
options:
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
        default: 10000
    temperature:
        description: The temperature for generation.
        type: float
        default: 1.0
    top_p:
        description: The top-p for generation.
        type: float
        default: 1.0
    tracing:
        description:
            - Whether to enable tracing using OpenTelemetry.
            - Requires C(opentelemetry-sdk) and C(azure-ai-inference) tracing support.
        type: bool
        default: false
required_one_of:
    - ["prompt", "messages"]
author:
    - Cogni AI
"""

EXAMPLES = r"""
- name: One-shot prompt
  ai_inference_chat_deepseek_r1:
    prompt: "Hello, how are you?"

- name: Multi-turn conversation
  ai_inference_chat_deepseek_r1:
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
        setup_tracing,
    )
except ImportError:
    # Fallback for local testing
    try:
        from plugins.module_utils.ai_inference_common import create_client, build_messages, setup_tracing
    except ImportError:
        from ai_inference_common import create_client, build_messages, setup_tracing


def main():
    module = AnsibleModule(
        argument_spec=dict(
            endpoint=dict(type="str", default="https://models.inference.ai.azure.com"),
            token=dict(type="str", no_log=True, required=False, fallback=(env_fallback, ["GITHUB_TOKEN"])),
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
            max_tokens=dict(type="int", default=10000),
            temperature=dict(type="float", default=1.0),
            top_p=dict(type="float", default=1.0),
            tracing=dict(type="bool", default=False),
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
            model="deepseek/deepseek-r1",
            messages=messages_dict,
        )

    token = module.params["token"]
    if not token:
        module.fail_json(msg="token is required or set GITHUB_TOKEN")

    instrumentor = None
    if module.params["tracing"]:
        instrumentor = setup_tracing()
        if not instrumentor:
            module.warn(
                "Tracing enabled but dependencies (opentelemetry, etc.) are missing. Proceeding without tracing."
            )

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
            "model": "deepseek/deepseek-r1",
        }

        if module.params["max_tokens"] is not None:
            kwargs["max_tokens"] = module.params["max_tokens"]

        if module.params["temperature"] is not None:
            kwargs["temperature"] = module.params["temperature"]

        if module.params["top_p"] is not None:
            kwargs["top_p"] = module.params["top_p"]

        response = client.complete(**kwargs)

        if instrumentor:
            instrumentor.uninstrument()

        module.exit_json(
            changed=False,
            message=response.choices[0].message.content,
            model="deepseek/deepseek-r1",
            messages=messages_dict,
        )
    except Exception as exc:
        if instrumentor:
            instrumentor.uninstrument()
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()
