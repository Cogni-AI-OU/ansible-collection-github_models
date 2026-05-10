#!/usr/bin/python

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule, env_fallback

DOCUMENTATION = r"""
---
module: ai_agents
short_description: stateless and stateful interface for AI Agents using Azure AI Agents SDK
description:
    - Provides an interface for creating and interacting with AI Agents via the azure-ai-agents SDK.
    - Can act like create_and_process handles agent creation, thread creation,
      sending messages, and waiting for the response.
    - This can be implemented universally to support stateful conversation by providing thread_id and agent_id.
extends_documentation_fragment:
    - cogni_ai.github_models.github_models_auth
options:
    agent_id:
        description: The ID of an existing agent. If not provided, a new agent will be created.
        type: str
    thread_id:
        description: The ID of an existing thread. If not provided, a new thread will be created.
        type: str
    model:
        description:
            - The model to use when creating a new agent.
            - If agent_id is not provided, this model is used.
        type: str
        default: "phi-4-mini-reasoning"
    name:
        description: The name of the agent to create.
        type: str
    instructions:
        description: The instructions for the agent to follow.
        type: str
    prompt:
        description: A single user prompt to send to the agent.
        type: str
    messages:
        description: A list of messages to add to the thread.
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
author:
    - Cogni AI
"""

EXAMPLES = r"""
- name: Create and process a run
  ai_agents:
    model: "phi-4-mini-reasoning"
    instructions: "You are a helpful assistant."
    prompt: "What is Ansible?"

- name: Continue conversation with existing thread and agent
  ai_agents:
    agent_id: "agent_123"
    thread_id: "thread_456"
    prompt: "Tell me more."
"""

RETURN = r"""
message:
    description: The generated message content from the agent.
    returned: success
    type: str
    sample: "Ansible is an open-source automation tool."
agent_id:
    description: The ID of the agent used or created.
    returned: success
    type: str
thread_id:
    description: The ID of the thread used or created.
    returned: success
    type: str
"""


# The import path for collection
try:
    from ansible_collections.cogni_ai.github_models.plugins.module_utils.ai_inference_common import (
        StaticTokenCredential,
    )
except ImportError:
    # Fallback for local testing
    try:
        from plugins.module_utils.ai_inference_common import StaticTokenCredential
    except ImportError:
        try:
            from ai_inference_common import StaticTokenCredential
        except ImportError:
            StaticTokenCredential = None

if not StaticTokenCredential:
    # Define inline fallback if import failed
    class StaticTokenCredential:
        def __init__(self, token):
            self.token = token

        def get_token(self, *scopes, **kwargs):
            from azure.core.credentials import AccessToken
            import time

            return AccessToken(self.token, int(time.time()) + 3600)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            endpoint=dict(type="str", default="https://models.inference.ai.azure.com"),
            token=dict(type="str", no_log=True, required=False, fallback=(env_fallback, ["GITHUB_TOKEN", "GH_TOKEN"])),
            agent_id=dict(type="str", required=False),
            thread_id=dict(type="str", required=False),
            model=dict(type="str", required=False, default="phi-4-mini-reasoning"),
            name=dict(type="str", required=False),
            instructions=dict(type="str", required=False),
            prompt=dict(type="str", required=False),
            messages=dict(
                type="list",
                elements="dict",
                required=False,
                options=dict(
                    role=dict(type="str", required=True, choices=["system", "user", "assistant"]),
                    content=dict(type="str", required=True),
                ),
            ),
        ),
        mutually_exclusive=[["prompt", "messages"]],
        required_one_of=[["prompt", "messages"]],
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(
            changed=False,
            msg="Check mode: no request sent",
            agent_id=module.params["agent_id"] or "check_mode_agent_id",
            thread_id=module.params["thread_id"] or "check_mode_thread_id",
            message="Check mode message",
        )

    token = module.params["token"]
    if not token:
        module.fail_json(msg="token is required or set GITHUB_TOKEN or GH_TOKEN")

    try:
        from azure.ai.agents import AgentsClient
    except ImportError:
        module.fail_json(msg="The 'azure-ai-agents' package is required for this module.")

    try:
        client = AgentsClient(endpoint=module.params["endpoint"], credential=StaticTokenCredential(token))

        with client:
            # 1. Setup Agent
            agent_id = module.params["agent_id"]
            if not agent_id:
                kwargs = {
                    "model": module.params["model"],
                }
                if module.params["name"]:
                    kwargs["name"] = module.params["name"]
                if module.params["instructions"]:
                    kwargs["instructions"] = module.params["instructions"]

                agent = client.create_agent(**kwargs)
                agent_id = agent.id

            # 2. Setup Thread
            thread_id = module.params["thread_id"]
            if not thread_id:
                thread = client.threads.create()
                thread_id = thread.id

            # 3. Add messages to Thread
            if module.params["prompt"]:
                client.messages.create(thread_id=thread_id, role="user", content=module.params["prompt"])

            if module.params["messages"]:
                for m in module.params["messages"]:
                    client.messages.create(thread_id=thread_id, role=m["role"], content=m["content"])

            # 4. Create and Process Run
            run = client.runs.create_and_process(thread_id=thread_id, agent_id=agent_id)

            # 5. Fetch response
            if run.status == "failed":
                error_details = getattr(run, "last_error", "Unknown error")
                module.fail_json(
                    msg="Run failed: %s" % error_details,
                    agent_id=agent_id,
                    thread_id=thread_id,
                    run_id=run.id,
                    run_status=run.status,
                    error=error_details,
                )

            # Get messages
            messages = client.messages.list(thread_id=thread_id, order="desc")
    except Exception as exc:
        # Check if it's an Azure core error with more details
        error_msg = str(exc)
        if hasattr(exc, "response") and hasattr(exc.response, "json"):
            try:
                details = exc.response.json()
                if "error" in details:
                    error_msg = "%s: %s" % (details["error"].get("code", "Error"), details["error"].get("message", error_msg))
            except Exception:
                pass
        module.fail_json(msg=error_msg)

    # Process messages (outside the try/except if we want to separate logic, but here it's fine)
    try:
        # Extract the latest assistant message
        response_message = ""
        for msg in messages:
            role = getattr(msg, "role", "")
            if str(role).lower() in ["assistant", "agent"]:
                if hasattr(msg, "text_messages") and msg.text_messages:
                    response_message = "\n".join([m.text.value for m in msg.text_messages])
                elif hasattr(msg, "content"):
                    blocks = []
                    for c in msg.content:
                        if getattr(c, "type", None) == "text" and hasattr(c, "text"):
                            blocks.append(c.text.value)
                    response_message = "\n".join(blocks)
                break

        module.exit_json(
            changed=True, message=response_message, agent_id=agent_id, thread_id=thread_id, run_status=run.status
        )
    except Exception as exc:
        module.fail_json(msg="Error processing response: %s" % str(exc))


if __name__ == "__main__":
    main()
