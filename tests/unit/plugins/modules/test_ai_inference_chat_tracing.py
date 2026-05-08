from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import MagicMock, patch
from plugins.modules.ai_inference_chat import main


@patch("plugins.modules.ai_inference_chat.AnsibleModule")
@patch("plugins.modules.ai_inference_chat.create_client")
@patch("plugins.modules.ai_inference_chat.setup_tracing")
def test_ai_inference_chat_with_tracing(mock_setup_tracing, mock_create_client, mock_module_class):
    mock_module = MagicMock()
    mock_module.params = {
        "endpoint": "https://test.ai",
        "token": "test-token",
        "model": "test-model",
        "prompt": "test-prompt",
        "system_prompt": None,
        "messages": None,
        "max_tokens": None,
        "temperature": None,
        "tracing": True,
    }
    mock_module.check_mode = False
    mock_module.exit_json.side_effect = SystemExit
    mock_module_class.return_value = mock_module

    mock_instrumentor = MagicMock()
    mock_setup_tracing.return_value = mock_instrumentor

    mock_client = MagicMock()
    mock_create_client.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "test-response"
    mock_client.complete.return_value = mock_response

    with pytest.raises(SystemExit):
        main()

    mock_setup_tracing.assert_called_once()
    mock_instrumentor.uninstrument.assert_called_once()
    mock_module.exit_json.assert_called_once()
    args, kwargs = mock_module.exit_json.call_args
    assert kwargs["message"] == "test-response"
