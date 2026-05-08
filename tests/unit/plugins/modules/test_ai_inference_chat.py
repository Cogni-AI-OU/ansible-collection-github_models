from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import MagicMock, patch
from plugins.modules.ai_inference_chat import main


@patch("plugins.modules.ai_inference_chat.AnsibleModule")
def test_ai_inference_chat_check_mode(mock_module_class):
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
    }
    mock_module.check_mode = True
    mock_module_class.return_value = mock_module

    with pytest.raises(SystemExit):
        main()

    mock_module.exit_json.assert_called_once()
    args, kwargs = mock_module.exit_json.call_args
    assert kwargs["changed"] is False
    assert "Check mode" in kwargs["msg"]
