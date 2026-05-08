from __future__ import absolute_import, division, print_function

__metaclass__ = type

from plugins.module_utils.ai_inference_common import build_messages


def test_build_messages_one_shot():
    messages = build_messages(prompt="Hello")
    assert len(messages) == 1
    assert messages[0].content == "Hello"


def test_build_messages_multi_turn():
    raw_messages = [
        {"role": "system", "content": "You are a bot"},
        {"role": "user", "content": "Hi"},
    ]
    messages = build_messages(raw_messages=raw_messages)
    assert len(messages) == 2
    assert messages[0].content == "You are a bot"
    assert messages[1].content == "Hi"


def test_build_messages_combined():
    raw_messages = [{"role": "user", "content": "Hi"}]
    messages = build_messages(system_prompt="System", raw_messages=raw_messages, prompt="Final")
    assert len(messages) == 3
    assert messages[0].content == "System"
    assert messages[1].content == "Hi"
    assert messages[2].content == "Final"
