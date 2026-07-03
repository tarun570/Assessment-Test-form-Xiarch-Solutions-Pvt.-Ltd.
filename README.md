# Autonomous Research Agent

This repository contains the submission for **Assessment Option 1 — Autonomous Research Agent**.
The project implements an autonomous research agent that gathers external information, analyzes it, and produces a structured, actionable summary. The code includes tools for web search, deduplication, source verification, memory, and export (Markdown/PDF).

The design keeps the model in control. The Python code provides tools for
search, memory lookup, source verification, secure code analysis, patch
execution, and internal knowledge access, while the LLM decides what to do next.

## Setup

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Set your OpenAI API key in the environment or in a `.env` file:

```bash
export OPENAI_API_KEY="sk-..."
```

## Run

```bash
python agent.py "impact of quantum computing on cryptography"
python agent.py "latest trends in agentic AI" --pdf
```

The repository implements Option 1 (Autonomous Research Agent).

The Option 1 agent generates:

- `summary.md` — structured Markdown research summary
- `summary.pdf` — PDF summary when using `--pdf`
- `memory.json` — saved past research runs for future `check_memory` queries

The Option 1 agent generates:

- `summary.md` — structured Markdown research summary
- `summary.pdf` — PDF summary when using `--pdf`
- `memory.json` — saved past research runs for future `check_memory` queries

## Repository contents

- `agent.py` — Option 1 autonomous research agent
- `tools.py` — web search, deduplication, verification, memory, and export helpers
- `tests/` — unit tests for core behavior
- `.github/workflows/python-app.yml` — CI workflow
- `estimate_call_cost.py`, `check_cost.py` — optional developer utilities

## How it works

1. User provides a research topic.
2. The model receives the topic and the available tool schema.
3. Each turn, the model chooses to:
   - call `search_web` with one or more queries,
   - call `check_memory` for prior research,
   - or call `finalize_summary` when it is ready.
4. Search queries execute in parallel.
5. The final summary is verified, saved, and exported.

The agent loop is not hardcoded; the model chooses the next action each turn.

## Assessment alignment

- The agent uses an LLM to decide queries, memory checks, and stopping.
- The system collects information from external web sources.
- The summary is structured with key points, findings, actions, and sources.
- The repository includes tests and CI for submission readiness.

## Submission checklist

Include the following files in your submission ZIP or GitHub repo:

- `agent.py`
- `tools.py`
- `tests/`
- `README.md`
- `RUN.md`
- `requirements.txt`

Notes:

- Remove any `.env` or files containing secrets before sharing.
- Tests: run `python -m pytest -q` (local result: `6 passed`).
- For a live demo ensure `OPENAI_API_KEY` is set in the environment.

## Notes

- This repository implements **Option 1 only**.
- `ddgs` is used for DuckDuckGo search; replace the search backend with a more robust API for a live demo if needed.
- `estimate_call_cost.py` and `check_cost.py` are optional developer utilities.
