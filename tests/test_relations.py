"""
test_relations.py
=================
Tests relational matches between conversations.
"""
from __future__ import annotations
from agy_exporter.models import ConversationTranscript, ConversationIntelligence, ConversationMeta
from agy_exporter.analysis.relations import find_relations

def test_find_relations():
    c1 = ConversationTranscript(
        conv_id="c1",
        steps=[],
        source_file="mock.jsonl",
        meta=ConversationMeta(conversation_id="c1", title="Docker Setup"),
        intelligence=ConversationIntelligence(
            files_mentioned=["drizzle.config.ts", "schema.ts"],
            technologies=["Docker", "TypeScript"],
            topics=["Deployment"]
        )
    )
    c2 = ConversationTranscript(
        conv_id="c2",
        steps=[],
        source_file="mock.jsonl",
        meta=ConversationMeta(conversation_id="c2", title="Drizzle Migration"),
        intelligence=ConversationIntelligence(
            files_mentioned=["schema.ts", "package.json"],
            technologies=["Drizzle ORM", "TypeScript"],
            topics=["Database Migration"]
        )
    )
    
    transcripts = {"c1": c1, "c2": c2}
    # Score details:
    # schema.ts matches: +2.5
    # TypeScript matches: +0.5
    # Total score: 3.0 (matches threshold 3.0)
    find_relations(transcripts, threshold=3.0)
    
    assert "c2" in c1.related_ids
    assert "c1" in c2.related_ids
