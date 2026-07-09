"""
test_pb_decoder.py
==================
Tests raw protobuf parsing and decoding components.
"""
from __future__ import annotations
import tempfile
import os
from agy_exporter.sources.pb_summaries import parse_summaries, _decode_fields

def test_decode_fields():
    # Simple length-delimited string protobuf data: tag (1<<3)|2 = 10, length 5, value "hello"
    raw_data = bytes([10, 5, 104, 101, 108, 108, 111])
    fields = _decode_fields(raw_data)
    assert len(fields) == 1
    assert fields[0][0] == 1 # field number
    assert fields[0][1] == 2 # wire type length-delimited
    assert fields[0][2] == b"hello"

def test_parse_summaries_missing():
    res = parse_summaries("nonexistent_file.pb")
    assert res == {}
