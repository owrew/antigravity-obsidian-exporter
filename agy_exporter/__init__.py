"""
agy_exporter
============
Synchronizes Google Antigravity conversations to an Obsidian knowledge vault.
"""
from __future__ import annotations
from .config import ExporterConfig
from .models import Step, ToolCall, Turn, ConversationTranscript, ConversationMeta, ConversationIntelligence
from .sync import run_export, export_one, start_watch, ExportState

__version__ = "2.0.0"
