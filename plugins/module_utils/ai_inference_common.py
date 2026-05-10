from __future__ import absolute_import, division, print_function

__metaclass__ = type


class StaticTokenCredential:
    """
    A static token credential that implements the TokenCredential protocol.
    Used for GitHub tokens which are Bearer tokens.
    """

    def __init__(self, token):
        self.token = token

    def get_token(self, *scopes, **kwargs):
        from azure.core.credentials import AccessToken
        import time

        # Return an AccessToken with a fake expiry (1 hour)
        return AccessToken(self.token, int(time.time()) + 3600)


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


def setup_tracing():
    try:
        from azure.core.settings import settings
        from azure.ai.inference.tracing import AIInferenceInstrumentor

        settings.tracing_implementation = "opentelemetry"
        instrumentor = AIInferenceInstrumentor()
        instrumentor.instrument()
        return instrumentor
    except ImportError:
        # We don't want to fail if tracing dependencies are missing,
        # but the module should have checked if it's required.
        return None


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
