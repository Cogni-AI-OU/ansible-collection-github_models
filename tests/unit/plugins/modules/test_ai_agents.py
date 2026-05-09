from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import MagicMock, patch
from plugins.modules.ai_agents import main


@patch("plugins.modules.ai_agents.AnsibleModule")
def test_ai_agents_check_mode(mock_module_class):
    mock_module = MagicMock()
    mock_module.params = {
        "endpoint": "https://test.ai",
        "token": "test-token",
        "agent_id": None,
        "thread_id": None,
        "model": "test-model",
        "name": None,
        "instructions": None,
        "prompt": "test-prompt",
        "messages": None,
    }
    mock_module.check_mode = True
    mock_module.exit_json.side_effect = SystemExit
    mock_module_class.return_value = mock_module

    with pytest.raises(SystemExit):
        main()

    mock_module.exit_json.assert_called_once()
    args, kwargs = mock_module.exit_json.call_args
    assert kwargs["changed"] is False
    assert "Check mode" in kwargs["msg"]
    assert kwargs["agent_id"] == "check_mode_agent_id"
    assert kwargs["thread_id"] == "check_mode_thread_id"

@patch("plugins.modules.ai_agents.AnsibleModule")
def test_ai_agents_no_token(mock_module_class):
    mock_module = MagicMock()
    mock_module.params = {
        "endpoint": "https://test.ai",
        "token": None,
        "agent_id": None,
        "thread_id": None,
        "model": "test-model",
        "name": None,
        "instructions": None,
        "prompt": "test-prompt",
        "messages": None,
    }
    mock_module.check_mode = False
    mock_module.fail_json.side_effect = SystemExit
    mock_module_class.return_value = mock_module

    with pytest.raises(SystemExit):
        main()

    mock_module.fail_json.assert_called_once()
    args, kwargs = mock_module.fail_json.call_args
    assert "token is required" in kwargs["msg"]

@patch("plugins.modules.ai_agents.AnsibleModule")
def test_ai_agents_no_model_and_no_agent_id(mock_module_class):
    mock_module = MagicMock()
    mock_module.params = {
        "endpoint": "https://test.ai",
        "token": "test-token",
        "agent_id": None,
        "thread_id": None,
        "model": None,
        "name": None,
        "instructions": None,
        "prompt": "test-prompt",
        "messages": None,
    }
    mock_module.check_mode = False
    mock_module.fail_json.side_effect = SystemExit
    mock_module_class.return_value = mock_module

    with pytest.raises(SystemExit):
        main()

    mock_module.fail_json.assert_called_once()
    args, kwargs = mock_module.fail_json.call_args
    assert "model is required if agent_id is not provided" in kwargs["msg"]
