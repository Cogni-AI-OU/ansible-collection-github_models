def create_client(endpoint, token):
    try:
        from azure.ai.inference import ChatCompletionsClient
        from azure.core.credentials import AzureKeyCredential
    except ImportError:
        raise ImportError("The 'azure-ai-inference' package is required for this module.")

    return ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )


def build_messages(raw_messages=None, system_prompt=None, prompt=None):
    try:
        from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
    except ImportError:
        # This shouldn't happen if create_client already checked, but for safety
        raise ImportError("The 'azure-ai-inference' package is required for this module.")

    messages = []

    if system_prompt:
        messages.append(SystemMessage(system_prompt))

    for item in raw_messages or []:
        role = item.get("role")
        content = item.get("content")

        if role == "system":
            messages.append(SystemMessage(content))
        elif role == "user":
            messages.append(UserMessage(content))
        elif role == "assistant":
            messages.append(AssistantMessage(content))
        else:
            raise ValueError("Unsupported role: %s" % role)

    if prompt:
        messages.append(UserMessage(prompt))

    return messages
