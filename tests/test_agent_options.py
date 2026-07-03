import os

import pytest

from agent import run_agent


def test_agent_run_requires_openai_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(SystemExit):
        run_agent("test query")
