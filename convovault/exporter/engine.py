"""
engine.py
=========
Provider-independent synchronization engine coordinating loaders, analyzers,
renderer, and indexers.
"""
from __future__ import annotations
import os
import logging
from typing import Dict, List, Optional

from ..models import Conversation, ConversationMeta
from ..config.exporter import ExporterConfig
from ..providers import get_provider
from ..analysis.intelligence import generate_intelligence
from ..analysis.relations import find_relations
from ..rendering.conversation import format_conversation
from ..analysis.wikilinks import title_to_filename
from ..indexing.index import generate_indexes
from ..state.state import ExportState, get_content_hash

log = logging.getLogger(__name__)

DEBUG_SUBDIR = ".convovault_debug"

def export_one(
    conv_id: str,
    convo: Conversation,
    config: ExporterConfig,
    meta_index: Dict[str, ConversationMeta],
    state: ExportState,
    all_meta: Dict[str, ConversationMeta]
) -> Optional[bool]:  # True=written, False=skipped, None=error
    meta = meta_index.get(conv_id)
    
    # Check source file modification time
    source_mtime = None
    if convo.source_file and os.path.isfile(convo.source_file):
        try:
            source_mtime = os.path.getmtime(convo.source_file)
        except Exception:
            pass

    # Format Markdown
    try:
        md_content = format_conversation(
            transcript=convo,
            meta=meta,
            all_meta=all_meta,
            config=config
        )
    except Exception as e:
        log.error("Formatting failed for %s: %s", conv_id, e)
        if config.debug:
            _dump_debug(conv_id, convo, config.vault_dir, str(e))
        return None

    # Idempotency check — skip write if content and mtime unchanged
    chash = get_content_hash(md_content)
    if not config.force and not state.needs_update(conv_id, chash, source_mtime):
        log.debug("Up-to-date, skipping: %s", conv_id[:8])
        return False  # sentinel: skipped

    # Filename collision resolver
    title = meta.title if meta else conv_id[:8]
    filename = title_to_filename(title)
    
    existing_path = state.get_note_path(conv_id)
    if existing_path:
        filename = os.path.basename(existing_path)
    else:
        candidate = os.path.join(config.output_chats_dir, filename)
        counter = 1
        while os.path.isfile(candidate):
            try:
                with open(candidate, 'r', encoding='utf-8') as fh:
                    first_lines = fh.read(500)
                if conv_id not in first_lines:
                    stem = filename[:-3]
                    filename = f"{stem} ({counter}).md"
                    candidate = os.path.join(config.output_chats_dir, filename)
                    counter += 1
                else:
                    break
            except Exception:
                break

    os.makedirs(config.output_chats_dir, exist_ok=True)
    note_path = os.path.join(config.output_chats_dir, filename)
    
    try:
        with open(note_path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(md_content)
        log.info("Synced: %s -> %s", conv_id[:8], filename)
    except Exception as e:
        log.error("Failed writing Obsidian note for %s: %s", conv_id, e)
        return None

    state.mark_exported(conv_id, chash, source_mtime, note_path)
    return True  # sentinel: written

def _dump_debug(conv_id: str, convo: Conversation, vault_dir: str, err: str):
    debug_dir = os.path.join(vault_dir, DEBUG_SUBDIR)
    os.makedirs(debug_dir, exist_ok=True)
    out_path = os.path.join(debug_dir, conv_id + ".txt")
    try:
        with open(out_path, 'w', encoding='utf-8') as fh:
            fh.write(f"DECODE ERROR: {err}\n\n")
            fh.write(f"Source file: {convo.source_file}\n")
            fh.write(f"Steps count: {len(convo.steps)}\n\n")
            for step in convo.steps[:20]:
                fh.write(f"--- Step {step.index} Type={step.step_type} ---\n")
                fh.write(step.content[:1000] if step.content else "[empty]")
                fh.write("\n\n")
    except Exception:
        pass

def run_export(config: ExporterConfig) -> dict:
    log.info("Starting ConvoVault -> Obsidian sync engine (provider: %s)", config.provider)
    
    provider = get_provider(config.provider)
    if not provider:
        log.error("Provider '%s' not registered or found.", config.provider)
        return {'written': 0, 'skipped': 0, 'failed': 0, 'total': 0}

    # 1. Load metadata index from provider
    meta_index = provider.load_metadata_index(config)
    
    # 2. Discover conversation IDs
    conv_ids = provider.discover_conversations(config)
    if config.conv_filter:
        conv_ids = [c for c in conv_ids if c in config.conv_filter]

    # Populate missing titles with fallbacks in meta_index
    for cid in conv_ids:
        if cid not in meta_index:
            meta_index[cid] = ConversationMeta(conversation_id=cid, title=cid[:8])

    # 3. Load conversations and run intelligence/relations in memory
    conversations: Dict[str, Conversation] = {}
    stats = {'written': 0, 'skipped': 0, 'failed': 0, 'total': len(conv_ids)}
    
    log.info("Loading and analyzing conversations...")
    for cid in conv_ids:
        try:
            convo = provider.read_conversation(cid, config)
            if convo and convo.steps:
                convo.meta = meta_index.get(cid)
                convo.intelligence = generate_intelligence(convo)
                conversations[cid] = convo
            else:
                log.warning("No conversation data available for %s", cid)
                stats['failed'] += 1
        except Exception as e:
            log.error("Failed loading conversation %s: %s", cid, e, exc_info=True)
            stats['failed'] += 1

    # 4. Cross-link relations
    find_relations(conversations)

    # 5. Export Markdown documents (Idempotent)
    state = ExportState(config.vault_dir)
    
    for cid, convo in conversations.items():
        try:
            res = export_one(
                conv_id=cid,
                convo=convo,
                config=config,
                meta_index=meta_index,
                state=state,
                all_meta=meta_index
            )
            if res is True:
                stats['written'] += 1
            elif res is False:
                stats['skipped'] += 1
            else:  # None = error
                stats['failed'] += 1
        except Exception as e:
            log.error("Failed exporting conversation %s: %s", cid, e, exc_info=True)
            stats['failed'] += 1

    # 6. Save State
    state.save()

    # 7. Generate global index files
    log.info("Rebuilding Timeline, Topics, Tag, and Conversation indexes...")
    generate_indexes(config.vault_dir, conversations)

    log.info(
        "Engine completed. Total=%d  Written=%d  Skipped=%d  Failed=%d",
        stats['total'], stats['written'], stats['skipped'], stats['failed']
    )
    return stats
