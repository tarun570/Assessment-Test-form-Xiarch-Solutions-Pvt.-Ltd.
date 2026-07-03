# Run and Cleanup Guide (Option 1 only)

This file explains how to run the Autonomous Research Agent (Option 1), run tests, and create a clean submission package containing only the essential files.

## Prerequisites
- Python 3.8+ (3.12 recommended)
- Create and activate a virtual environment (recommended)
- Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Set your OpenAI API key (either in `.env` or environment):

```powershell
$env:OPENAI_API_KEY="sk-..."
# or create a .env file with OPENAI_API_KEY=sk-...
```

On macOS / Linux / WSL use:

```bash
export OPENAI_API_KEY="sk-..."
```

## Quick start (one-line)

From the repository root:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:OPENAI_API_KEY="sk-..."
python -m pytest -q
python agent.py "impact of quantum computing on cryptography"
```

## Run the agent (Option 1)

Run the autonomous research agent and save a Markdown summary:

```powershell
python agent.py "impact of quantum computing on cryptography"
```

Also export a PDF:

```powershell
python agent.py "impact of quantum computing on cryptography" --pdf
```

Outputs created by the run:
- `summary.md` — structured Markdown summary
- `summary.pdf` — PDF summary (when `--pdf` used)
- `memory.json` — saved past research runs (used by `check_memory`)

## Test & validation

Run unit tests:

```powershell
python -m pytest -q
```

Quick syntax check (Option 1 files only):

```powershell
python -m py_compile agent.py tools.py
```

## Files/folders that are safe to remove (optional)

Common items safe to remove to reduce package size:

- `venv/` or any local virtual environment folder
- `.pytest_cache/` and `__pycache__/` directories
- `submission_option1.zip` (old packaged artifact)
- `demo.ps1`, `demo.sh` (optional demo scripts)
- `estimate_call_cost.py`, `check_cost.py` (developer utilities)

Delete them (PowerShell):

```powershell
Remove-Item -Recurse -Force .\venv
Remove-Item -Recurse -Force .\.pytest_cache
Remove-Item -Recurse -Force .\__pycache__
Remove-Item -Force .\submission_option1.zip
Remove-Item -Force .\demo.ps1
Remove-Item -Force .\demo.sh
```

Or (bash):

```bash
rm -rf venv/ .pytest_cache/ __pycache__/ submission_option1.zip demo.ps1 demo.sh
```

Note: Do not delete source files like `agent.py`, `tools.py`, `tests/`, or `README.md` unless you intentionally want to remove functionality.

## Clean package suggestion (Option 1 only)

Create a submission ZIP containing only the essential files for Option 1:

```powershell
# from repo root
Compress-Archive -Path agent.py,tools.py,tests,README.md,RUN.md,requirements.txt -DestinationPath submission_option1.zip
```

Or (bash):

```bash
zip -r submission_option1.zip agent.py tools.py tests README.md RUN.md requirements.txt
```

---

If you'd like, I can:

- create the `submission_option1.zip` now, or
- remove the optional files listed above for a smaller package.
