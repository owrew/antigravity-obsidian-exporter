"""
test_markdown.py
================
Tests formatting steps, YAML frontmatter tags, turns output format.
"""
from __future__ import annotations
from agy_exporter.models import Step, ConversationTranscript, ConversationMeta
from agy_exporter.render.conversation import format_conversation

def test_format_conversation():
    steps = [
        Step(
            index=0,
            source="USER_EXPLICIT",
            step_type="USER_INPUT",
            status="DONE",
            created_at="2026-06-18T14:38:27Z",
            content="Hello assistant."
        )
    ]
    ts = ConversationTranscript(
        conv_id="convo_123",
        steps=steps,
        source_file="mock.jsonl"
    )
    meta = ConversationMeta(conversation_id="convo_123", title="Test Title")
    
    md = format_conversation(ts, meta, all_meta={"convo_123": meta})
    
    assert "title: \"Test Title\"" in md
    assert "id: \"convo_123\"" in md
    assert "# Test Title" in md
    assert "User — Turn 1" in md
    assert "Hello assistant." in md
