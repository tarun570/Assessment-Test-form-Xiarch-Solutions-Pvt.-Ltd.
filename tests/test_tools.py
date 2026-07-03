import os
import json
from unittest.mock import patch

import pytest

import tools


def test_dedupe_results_removes_duplicates():
    results = {
        "query1": [
            {"url": "https://example.com/a", "snippet": "same snippet"},
            {"url": "https://example.com/b", "snippet": "same snippet"},
        ],
        "query2": [
            {"url": "https://example.com/a", "snippet": "same snippet"},
        ],
    }

    deduped = tools.dedupe_results(results)
    assert len(deduped["query1"]) == 1
    assert len(deduped["query2"]) == 0


def test_is_allowed_url():
    assert tools._is_allowed_url("https://example.com/page") is True
    assert tools._is_allowed_url("ftp://example.com") is False
    assert tools._is_allowed_url("https://tiktok.com/video") is False


@patch("tools.requests.head")
@patch("tools.requests.get")
def test_verify_and_filter_sources_filters_and_validates(get_mock, head_mock):
    head_response = type("R", (), {"status_code": 200})
    head_mock.return_value = head_response
    get_mock.return_value = head_response

    urls = [
        "https://example.com/article",
        "https://tiktok.com/content",
        "https://invalid.example.com/fail",
    ]

    verified = tools.verify_and_filter_sources(urls, max_results=5)
    assert "https://example.com/article" in verified
    assert "https://tiktok.com/content" not in verified
    assert "https://invalid.example.com/fail" in verified


def test_memory_save_and_search(tmp_path):
    original_memory_file = tools.MEMORY_FILE
    test_memory = tmp_path / "memory.json"
    tools.MEMORY_FILE = str(test_memory)

    try:
        tools.save_to_memory("Test Topic", {"sources": ["https://example.com"]})
        memory = tools.load_memory()

        assert len(memory) == 1
        assert memory[0]["topic"] == "Test Topic"
        assert "https://example.com" in memory[0]["summary"]["sources"]

        results = tools.search_memory("test")
        assert len(results) == 1
        assert results[0]["topic"] == "Test Topic"
    finally:
        tools.MEMORY_FILE = original_memory_file


def test_export_markdown_creates_file(tmp_path):
    summary = {
        "key_points": ["point 1"],
        "important_findings": ["finding 1"],
        "actionable_insights": ["insight 1"],
        "sources": ["https://example.com"],
    }
    path = tmp_path / "output.md"
    tools.export_markdown("Topic", summary, str(path))

    assert path.exists()
    content = path.read_text()
    assert "Research Summary: Topic" in content
    assert "https://example.com" in content
