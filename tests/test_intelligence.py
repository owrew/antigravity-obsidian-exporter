"""
test_intelligence.py
====================
Tests heuristics for summaries, tech stack mapping, and commands extraction.
"""
from __future__ import annotations
from agy_exporter.models import Step, ConversationTranscript
from agy_exporter.analysis.intelligence import generate_intelligence

def test_generate_intelligence():
    steps = [
        Step(
            index=0,
            source="USER_EXPLICIT",
            step_type="USER_INPUT",
            status="DONE",
            created_at="2026-06-18T14:38:27Z",
            content="Deploy React webapp on Railway using Drizzle ORM."
        )
    ]
    ts = ConversationTranscript(
        conv_id="test_id",
        steps=steps,
        source_file="mock.jsonl"
    )
    intel = generate_intelligence(ts)
    
    assert "React" in intel.technologies
    assert "Drizzle ORM" in intel.technologies
    assert "Railway" in intel.technologies
    assert "Deployment" in intel.topics
    assert "Deploy React webapp on Railway using Drizzle ORM." in intel.summary
