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

Option 2 — Secure coding assistant:

```bash
python secure_coding_agent.py path/to/vulnerable_file.py
```

Option 3 — Internal knowledge execution agent:

```bash
python knowledge_agent.py "Who works on the Research Agent project?"
```

The repository implements:

- **Option 1:** Autonomous research agent with external web search, duplicate filtering, source validation, memory, and Markdown/PDF export.
- **Option 2:** Secure coding assistant that inspects a source file, identifies vulnerabilities, and outputs a patched code file.
- **Option 3:** Internal knowledge execution agent that reads internal JSON knowledge sources, reasons over the data, selects actions, executes them, and logs audits.

The Option 1 agent generates:

- `summary.md` — structured Markdown research summary
- `summary.pdf` — PDF summary when using `--pdf`
- `memory.json` — saved past research runs for future `check_memory` queries

## Repository contents

- `agent.py` — Option 1 autonomous research agent
- `secure_coding_agent.py` — Option 2 secure coding assistant
- `knowledge_agent.py` — Option 3 knowledge execution agent
- `tools.py` — web search, deduplication, verification, memory, and export helpers
- `internal_knowledge.json` — sample internal knowledge source for Option 3
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

## Notes

- This repository implements **Options 1, 2, and 3**.
- `ddgs` is used for DuckDuckGo search; replace the search backend with a more
  robust API for a live demo if needed.
- `estimate_call_cost.py` and `check_cost.py` are optional tools, not required
  for the core agents.
