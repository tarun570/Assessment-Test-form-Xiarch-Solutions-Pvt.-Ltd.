"""
tools.py
----------------
Concrete capabilities the agent can invoke. The agent (LLM) decides WHEN
and WHY to call these -- this file only implements HOW they work.
No decision-making logic lives here; that is intentional so the "brain"
stays entirely inside agent.py's LLM calls.
"""

import os
import json
import hashlib
import concurrent.futures
from datetime import datetime, timezone
import warnings

# Silence known runtime warning emitted by the legacy `duckduckgo_search` package
warnings.filterwarnings(
    "ignore",
    message=r".*duckduckgo_search.*renamed.*",
    category=RuntimeWarning,
)

DDGS = None
try:
    # the package was renamed from `duckduckgo_search` -> `ddgs`
    from ddgs import DDGS as _DDGS
    DDGS = _DDGS
except Exception:
    try:
        from duckduckgo_search import DDGS as _DDGS
        DDGS = _DDGS
    except Exception:
        DDGS = None
from fpdf import FPDF
import requests
import urllib.parse

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")


# ---------------------------------------------------------------------------
# Web search
# ---------------------------------------------------------------------------
def _single_search(query: str, max_results: int = 5) -> list[dict]:
    """Run one web search query and return normalized results."""
    results = []
    try:
        if DDGS is None:
            raise ImportError(
                "Search backend not available. Install `ddgs` or `duckduckgo-search` package."
            )
        # Temporarily suppress RuntimeWarnings emitted by legacy search packages
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", ""),
                    })
    except Exception as e:
        results.append({
            "title": "ERROR",
            "url": "",
            "snippet": f"Search failed: {e}. Try: pip install -r requirements.txt",
        })
    return results


def search_web(queries: list[str], max_results: int = 5) -> dict:
    """
    Search one or more queries IN PARALLEL (bonus requirement).
    The agent decides how many queries and what they are -- this
    function just executes whatever list it is given.
    """
    output = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(8, len(queries) or 1)) as pool:
        future_map = {pool.submit(_single_search, q, max_results): q for q in queries}
        for future in concurrent.futures.as_completed(future_map):
            q = future_map[future]
            output[q] = future.result()
    return dedupe_results(output)


def dedupe_results(results_by_query: dict) -> dict:
    """Remove duplicate/irrelevant snippets across all queries (by content hash)."""
    seen_hashes = set()
    cleaned = {}
    for query, items in results_by_query.items():
        unique_items = []
        for item in items:
            snippet = item.get("snippet", "").strip()
            if not snippet:
                continue
            key = hashlib.sha256(snippet[:160].encode()).hexdigest()
            if key in seen_hashes:
                continue
            seen_hashes.add(key)
            unique_items.append(item)
        cleaned[query] = unique_items
    return cleaned


# ---------------------------------------------------------------------------
# Source verification / filtering
# ---------------------------------------------------------------------------
def _is_allowed_url(url: str) -> bool:
    if not url:
        return False
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    host = parsed.netloc.lower()
    # quick denylist for noisy/social/personal domains
    deny = [
        "tiktok.com",
        "linkedin.com",
        "medium.com",
        "grokipedia",
        "evytor",
        "t.co",
        "facebook.com",
        "twitter.com",
        "instagram.com",
    ]
    for d in deny:
        if d in host:
            return False
    return True


def verify_and_filter_sources(urls: list[str], max_results: int = 10) -> list[str]:
    """Validate and filter a list of URLs.

    - removes non-http(s) urls
    - removes common social/personal domains via denylist
    - checks each URL returns a 2xx-3xx status (HEAD with fallback to GET)
    - returns up to `max_results` unique URLs
    """
    cleaned = []
    seen = set()
    for url in urls:
        if len(cleaned) >= max_results:
            break
        if not _is_allowed_url(url):
            continue
        if url in seen:
            continue
        try:
            r = requests.head(url, allow_redirects=True, timeout=5)
            status = r.status_code
            if status < 200 or status >= 400:
                # fallback to GET for servers that don't respond to HEAD
                r = requests.get(url, timeout=5)
                status = r.status_code
            if 200 <= status < 400:
                cleaned.append(url)
                seen.add(url)
        except Exception:
            continue
    return cleaned


# ---------------------------------------------------------------------------
# Memory (store previous searches so the agent can recall past research)
# ---------------------------------------------------------------------------
def load_memory() -> list[dict]:
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_to_memory(topic: str, summary: dict) -> None:
    memory = load_memory()
    memory.append({
        "topic": topic,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
    })
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def search_memory(keyword: str) -> list[dict]:
    """Let the agent check if it has researched something similar before."""
    memory = load_memory()
    keyword_lower = keyword.lower()
    return [m for m in memory if keyword_lower in m["topic"].lower()]


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
def export_markdown(topic: str, summary: dict, path: str) -> str:
    lines = [f"# Research Summary: {topic}\n"]
    lines.append(f"_Generated: {datetime.now(timezone.utc).isoformat()} UTC_\n")

    lines.append("## Key Points\n")
    for point in summary.get("key_points", []):
        lines.append(f"- {point}")

    lines.append("\n## Important Findings\n")
    for finding in summary.get("important_findings", []):
        lines.append(f"- {finding}")

    lines.append("\n## Actionable Insights\n")
    for insight in summary.get("actionable_insights", []):
        lines.append(f"- {insight}")

    lines.append("\n## Sources\n")
    for src in summary.get("sources", []):
        lines.append(f"- {src}")

    content = "\n".join(lines)
    with open(path, "w") as f:
        f.write(content)
    return path


def export_pdf(topic: str, summary: dict, path: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, f"Research Summary: {topic}")
    pdf.set_font("Helvetica", "", 10)
    pdf.ln(2)

    def section(title, items):
        pdf.set_font("Helvetica", "B", 13)
        pdf.multi_cell(0, 8, title)
        pdf.set_font("Helvetica", "", 11)
        for item in items:
            safe = item.encode("latin-1", "replace").decode("latin-1")
            pdf.multi_cell(0, 6, f"- {safe}")
        pdf.ln(2)

    section("Key Points", summary.get("key_points", []))
    section("Important Findings", summary.get("important_findings", []))
    section("Actionable Insights", summary.get("actionable_insights", []))
    section("Sources", summary.get("sources", []))

    pdf.output(path)
    return path