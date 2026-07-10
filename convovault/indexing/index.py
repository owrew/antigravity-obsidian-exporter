"""
index.py
========
Generates global index files in the Obsidian vault:
- Timeline.md (chronological list)
- Conversations.md (table list with metadata)
- Tags.md (grouped by tags)
- Topics.md (grouped by topics)
"""
from __future__ import annotations
import os
import logging
from collections import defaultdict
from typing import Dict, List
from ..models import ConversationTranscript

log = logging.getLogger(__name__)

def generate_indexes(vault_dir: str, transcripts: Dict[str, ConversationTranscript]):
    """
    Creates/updates Timeline.md, Conversations.md, Tags.md, and Topics.md in vault_dir root.
    """
    os.makedirs(vault_dir, exist_ok=True)
    
    # Sort transcripts by creation date (descending)
    def get_sort_key(t: ConversationTranscript):
        # Fallback to current year if unknown
        date_str = ""
        if t.steps:
            date_str = t.steps[0].created_at
        if not date_str and t.meta and t.meta.created_at:
            from datetime import datetime, timezone
            date_str = datetime.fromtimestamp(t.meta.created_at, tz=timezone.utc).isoformat()
        return date_str or "1970-01-01T00:00:00Z"
        
    sorted_convs = sorted(transcripts.values(), key=get_sort_key, reverse=True)
    
    # --- 1. Timeline.md ---
    timeline_path = os.path.join(vault_dir, "Timeline.md")
    timeline_lines = [
        "# 📅 Conversation Timeline",
        "",
        "Chronological catalog of all Antigravity agent interactions.",
        ""
    ]
    
    current_month = ""
    for c in sorted_convs:
        date_str = get_sort_key(c)[:10]
        title = c.meta.title if c.meta else c.conv_id[:8]
        month = date_str[:7] # YYYY-MM
        if month != current_month:
            current_month = month
            timeline_lines.append(f"\n## 📆 {current_month}")
        timeline_lines.append(f"- **{date_str}**: [[{title}]] (steps: {len(c.steps)})")
        
    try:
        with open(timeline_path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write("\n".join(timeline_lines) + "\n")
        log.info("Timeline.md updated successfully")
    except Exception as e:
        log.error("Failed to write Timeline.md: %s", e)

    # --- 2. Conversations.md ---
    convs_path = os.path.join(vault_dir, "Conversations.md")
    convs_lines = [
        "# 💬 All Conversations",
        "",
        "Comprehensive index of all Antigravity conversations.",
        "",
        "| Conversation Title | Date | Steps | Main Technologies |",
        "| --- | --- | --- | --- |"
    ]
    for c in sorted_convs:
        title = c.meta.title if c.meta else c.conv_id[:8]
        date_str = get_sort_key(c)[:10]
        steps = len(c.steps)
        tech_list = ", ".join(c.intelligence.technologies[:4]) if c.intelligence.technologies else "*None*"
        convs_lines.append(f"| [[{title}]] | {date_str} | {steps} | {tech_list} |")
        
    try:
        with open(convs_path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write("\n".join(convs_lines) + "\n")
        log.info("Conversations.md updated successfully")
    except Exception as e:
        log.error("Failed to write Conversations.md: %s", e)

    # --- 3. Tags.md ---
    tags_path = os.path.join(vault_dir, "Tags.md")
    tag_map = defaultdict(list)
    for c in sorted_convs:
        title = c.meta.title if c.meta else c.conv_id[:8]
        date_str = get_sort_key(c)[:10]
        # Gather all tags from yaml/extracted
        tags = c.intelligence.technologies + ["antigravity", "ai-chat"]
        for tag in set(t.lower().replace(" ", "-") for t in tags):
            tag_map[tag].append((title, date_str))
            
    tags_lines = [
        "# 🏷️ Conversations by Tag",
        "",
        "Filter and discover conversations grouped by technology tags.",
        ""
    ]
    for tag in sorted(tag_map.keys()):
        tags_lines.append(f"\n## #{tag}")
        for title, date in tag_map[tag]:
            tags_lines.append(f"- **{date}** — [[{title}]]")
            
    try:
        with open(tags_path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write("\n".join(tags_lines) + "\n")
        log.info("Tags.md updated successfully")
    except Exception as e:
        log.error("Failed to write Tags.md: %s", e)

    # --- 4. Topics.md ---
    topics_path = os.path.join(vault_dir, "Topics.md")
    topic_map = defaultdict(list)
    for c in sorted_convs:
        title = c.meta.title if c.meta else c.conv_id[:8]
        date_str = get_sort_key(c)[:10]
        for topic in c.intelligence.topics:
            topic_map[topic].append((title, date_str))
            
    topics_lines = [
        "# 🧠 Conversations by Topic",
        "",
        "Discover conversations grouped by analytical topic domains.",
        ""
    ]
    for topic in sorted(topic_map.keys()):
        topics_lines.append(f"\n## 📌 {topic}")
        for title, date in topic_map[topic]:
            topics_lines.append(f"- **{date}** — [[{title}]]")
            
    try:
        with open(topics_path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write("\n".join(topics_lines) + "\n")
        log.info("Topics.md updated successfully")
    except Exception as e:
        log.error("Failed to write Topics.md: %s", e)
