"""Named analysis lenses: interpretive stance, future prompt routing, UI labels."""

from __future__ import annotations

from typing import Literal

LensId = Literal[
    "lexical_overlap",
    "terminological",
    "epistemic",
    "hermeneutic",
    "discourse",
]

# Order shown in the Streamlit select box.
LENS_ORDER: tuple[LensId, ...] = (
    "lexical_overlap",
    "terminological",
    "epistemic",
    "hermeneutic",
    "discourse",
)

ANALYSIS_LENSES: dict[str, dict[str, str]] = {
    "lexical_overlap": {
        "label": "Structural — lexical hooks",
        "short": "Cross-document word overlap after light tokenization (current offline engine).",
        "status": "live",
    },
    "terminological": {
        "label": "Terminological — concepts & naming",
        "short": "Maps how each text names and stabilizes concepts; hunt synonymy, equivocation, and definitional drift.",
        "status": "planned",
    },
    "epistemic": {
        "label": "Epistemic — ways of knowing",
        "short": "Offline **vocabulary-register sketch** (evidence / logic / authority / hedging / axioms) plus structural overlap. LLM layer optional later.",
        "status": "hybrid",
    },
    "hermeneutic": {
        "label": "Hermeneutic — horizons & sense-making",
        "short": "Foregrounds fore-conceptions, interpretive circles, and how texts read *each other* or past traditions.",
        "status": "planned",
    },
    "discourse": {
        "label": "Discourse / archive — conditions of sayability",
        "short": "Asks what can be said within each text’s regime: silences, tacit rules, formation of objects of knowledge.",
        "status": "planned",
    },
}


def lens_label(lens_id: str) -> str:
    return ANALYSIS_LENSES[lens_id]["label"]


def format_report_preamble(lens_id: str) -> str:
    """Markdown block prefixed to whatever the current engine outputs."""
    meta = ANALYSIS_LENSES.get(lens_id, ANALYSIS_LENSES["lexical_overlap"])
    lines = [
        f"## Active lens: {meta['label']}",
        "",
        meta["short"],
        "",
    ]
    status = meta["status"]
    if status == "hybrid":
        lines.extend(
            [
                "*This lens runs an **offline epistemic vocabulary heuristic** (see first section below), "
                "then the usual **structural overlap** substrate. A deeper interpretive synthesis still "
                "needs an LLM when you wire `OPENAI_API_KEY` (future).*",
                "",
            ]
        )
    elif status != "live":
        lines.extend(
            [
                "*Engine note: this lens is not yet wired to its own model pass or retrieval strategy — "
                "the section below still uses the **offline lexical sketch**. Prompt templates for this lens "
                "live in `docs/analysis_lenses.md`.*",
                "",
            ]
        )
    return "\n".join(lines)
