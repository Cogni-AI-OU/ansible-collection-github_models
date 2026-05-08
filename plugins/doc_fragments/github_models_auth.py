class ModuleDocFragment(object):
    # Standard documentation fragment for GitHub Models authentication
    DOCUMENTATION = r'''
options:
    endpoint:
        description: The endpoint for the AI Inference service.
        type: str
        default: "https://models.github.ai/inference"
    token:
        description:
            - The GitHub token for authentication.
            - If not provided, the C(GITHUB_TOKEN) environment variable will be used.
        type: str
        no_log: true
'''
