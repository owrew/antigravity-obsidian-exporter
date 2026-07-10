"""
test_wikilinks.py
=================
Tests WikiLinks matching and tag classification patterns.
"""
from __future__ import annotations
from convovault.analysis.wikilinks import extract_topics, slugify, title_to_filename

def test_extract_topics():
    text = "We configured PostgreSQL and deployed on Docker container."
    wiki, tags = extract_topics(text)
    
    assert "PostgreSQL" in wiki
    assert "Docker" in wiki
    assert "postgresql" in tags
    assert "docker" in tags
    assert "convovault" in tags

def test_slugify():
    assert slugify("Hello, World! @2026") == "Hello-World-2026"

def test_title_to_filename():
    assert title_to_filename("Fixing EAS: CLI Issue?") == "Fixing EAS CLI Issue.md"
