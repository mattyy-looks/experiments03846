"""Offline epistemic-flavored sketch: vocabulary markers, not a full model."""

from __future__ import annotations

import re

# Lightweight lexical registers — crude proxies for “ways of knowing” talk.
_EPISTEMIC_VOCAB: dict[str, list[str]] = {
    "empirical / data-oriented": [
        "data",
        "study",
        "studies",
        "evidence",
        "empirical",
        "observed",
        "observation",
        "measure",
        "measured",
        "sample",
        "experiment",
        "experimental",
        "results",
        "finding",
        "findings",
        "statistics",
        "statistical",
        "survey",
        "hypothesis",
        "replicate",
        "dataset",
    ],
    "inferential / logical": [
        "therefore",
        "thus",
        "hence",
        "follows",
        "implies",
        "infer",
        "inference",
        "premise",
        "conclusion",
        "proves",
        "proof",
        "argument",
        "valid",
        "invalid",
        "necessary",
        "sufficient",
        "contradiction",
        "if and only if",
        "syllogism",
        "entails",
    ],
    "authority / testimony": [
        "according",
        "cites",
        "cited",
        "citation",
        "source",
        "sources",
        "author",
        "authors",
        "expert",
        "reports",
        "claims",
        "argues",
        "writes",
        "states",
        "testimony",
        "witness",
        "reference",
        "references",
    ],
    "hedging / doubt": [
        "may",
        "might",
        "could",
        "perhaps",
        "possibly",
        "unclear",
        "uncertain",
        "uncertainty",
        "likely",
        "unlikely",
        "plausible",
        "speculative",
        "limitation",
        "limitations",
        "caveat",
        "assumption",
        "assumes",
        "tentative",
        "preliminary",
        "qualify",
    ],
    "definitional / axiomatic": [
        "definition",
        "define",
        "defined",
        "axiom",
        "axiomatic",
        "necessarily",
        "always",
        "never",
        "must",
        "cannot",
        "principle",
        "law",
        "theorem",
        "lemma",
        "postulate",
        "tautology",
        "by definition",
    ],
}


def _word_tokens(text: str) -> int:
    return len(re.findall(r"[A-Za-z]+", text))


def _count_hits(text: str, words: list[str]) -> int:
    lower = text.lower()
    total = 0
    for w in words:
        if " " in w:
            total += len(re.findall(re.escape(w), lower))
        else:
            total += len(re.findall(rf"\b{re.escape(w.lower())}\b", lower))
    return total


def epistemic_sketch_markdown(texts: dict[str, str]) -> str:
    """Markdown section: per-file register counts + which file leads each register."""
    lines: list[str] = [
        "## Epistemic vocabulary sketch (offline heuristic)",
        "",
        "_Keyword counts in coarse registers — **not** a philosophical verdict on your corpus. "
        "Use for **relative** emphasis between files; rates are hits per 10,000 word-like tokens._",
        "",
    ]

    per_file: dict[str, dict[str, float]] = {}

    for fname, body in texts.items():
        if body.startswith("[EXTRACTION FAILED"):
            lines.append(f"### `{fname}`")
            lines.append("")
            lines.append("_Skipped — extraction failed._")
            lines.append("")
            continue

        tokens = _word_tokens(body)
        if tokens == 0:
            lines.append(f"### `{fname}`")
            lines.append("")
            lines.append("_No extractable words._")
            lines.append("")
            continue

        scale = 10000.0 / tokens
        rates: dict[str, float] = {}
        lines.append(f"### `{fname}`")
        lines.append("")
        lines.append("| Register | Hits | Per 10k words |")
        lines.append("|----------|------|----------------|")
        for cat, vocab in _EPISTEMIC_VOCAB.items():
            hits = _count_hits(body, vocab)
            rate = hits * scale
            rates[cat] = rate
            lines.append(f"| {cat} | {hits} | {rate:.1f} |")
        lines.append("")
        per_file[fname] = rates

    if len(per_file) < 2:
        lines.append(
            "*Add more PDFs to compare emphasis across files; with one readable file, "
            "the table above still gives raw rates.*"
        )
        return "\n".join(lines)

    lines.append("### Which file pushes each register hardest (relative)")
    lines.append("")
    lines.append(
        "_Among successfully extracted files — highest **per-10k** rate wins; ties listed together._"
    )
    lines.append("")

    categories = list(_EPISTEMIC_VOCAB.keys())
    best_rate: dict[str, float] = {}
    leaders: dict[str, list[str]] = {}

    for cat in categories:
        best = -1.0
        for fname, rates in per_file.items():
            r = rates.get(cat, 0.0)
            if r > best + 1e-9:
                best = r
                leaders[cat] = [fname]
            elif abs(r - best) <= 1e-9:
                leaders[cat].append(fname)
        best_rate[cat] = best

    for cat in categories:
        names = leaders.get(cat, [])
        rate = best_rate.get(cat, 0.0)
        if not names:
            continue
        pretty = ", ".join(f"`{n}`" for n in sorted(names))
        lines.append(f"- **{cat}** → {pretty} (~{rate:.1f} per 10k words)")

    lines.append("")
    lines.append(
        "*Next step when you want depth: LLM pass using `docs/analysis_lenses.md` epistemic prompts "
        "+ `agent_character_and_skills.md` — requires API configuration.*"
    )

    return "\n".join(lines)
