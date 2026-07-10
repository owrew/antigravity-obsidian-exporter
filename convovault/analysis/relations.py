"""
relations.py
============
Detects relations between conversations using shared technologies, topics, files, and commands.
"""
from __future__ import annotations
import logging
from typing import Dict
from ..models import ConversationTranscript

log = logging.getLogger(__name__)


def _score_similarity(c1: ConversationTranscript, c2: ConversationTranscript) -> float:
    score = 0.0

    # 1. Shared files (highly relevant)
    files1 = set(c1.intelligence.files_mentioned)
    files2 = set(c2.intelligence.files_mentioned)
    shared_files = files1.intersection(files2)
    score += len(shared_files) * 2.5

    # 2. Shared technologies
    tech1 = set(c1.intelligence.technologies)
    tech2 = set(c2.intelligence.technologies)
    shared_tech = tech1.intersection(tech2)
    score += len(shared_tech) * 0.5

    # 3. Shared topics
    topics1 = set(c1.intelligence.topics)
    topics2 = set(c2.intelligence.topics)
    shared_topics = topics1.intersection(topics2)
    score += len(shared_topics) * 0.5

    # 4. Shared commands
    cmds1 = set(c1.intelligence.commands_executed)
    cmds2 = set(c2.intelligence.commands_executed)
    shared_cmds = cmds1.intersection(cmds2)
    score += len(shared_cmds) * 1.0

    return score


def find_relations(transcripts: Dict[str, ConversationTranscript], threshold: float = 3.0):
    """
    Computes cross-links between all conversations in-place.
    """
    keys = list(transcripts.keys())
    log.info("Computing cross-relations for %d conversations...", len(keys))

    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            c1 = transcripts[keys[i]]
            c2 = transcripts[keys[j]]

            score = _score_similarity(c1, c2)
            if score >= threshold:
                c1.related_ids.append(c2.conv_id)
                c2.related_ids.append(c1.conv_id)
                log.debug("Link created: %s <-> %s (score: %.1f)", c1.conv_id[:8], c2.conv_id[:8], score)

    # Deduplicate related lists
    for transcript in transcripts.values():
        transcript.related_ids = sorted(list(set(transcript.related_ids)))
