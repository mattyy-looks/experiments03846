"""PDF text extraction and lightweight cross-document overlap hints (no LLM)."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

import fitz

# Minimal English stopwords — enough for rough overlap; expand later if needed.
_STOP = frozenset(
    "a an the and or but if then else for while with from to of in on at by as is was were "
    "are be been being have has had having do does did doing will would could should may "
    "might must can cannot not no yes so such this that these those it its they them their "
    "we our you your he she his her they them who what which when where why how all any "
    "each every both few more most other some such than too very just also only own same "
    "into through during before after above below between under again further once here there "
    "when where why how off out up down over under again further once".split()
)


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z]+", text.lower())
    return [w for w in words if len(w) > 2 and w not in _STOP]


def extract_pdf(path: Path) -> str:
    doc = fitz.open(path)
    try:
        return "\n".join(page.get_text() for page in doc)
    finally:
        doc.close()


def extract_folder(folder: Path) -> dict[str, str]:
    folder = folder.expanduser().resolve()
    if not folder.exists():
        raise ValueError(f"Path does not exist: {folder}")
    if not folder.is_dir():
        raise ValueError(f"Not a folder (maybe a file?): {folder}")

    out: dict[str, str] = {}
    pdfs = sorted(folder.glob("*.pdf"))
    for p in pdfs:
        try:
            out[p.name] = extract_pdf(p)
        except Exception as exc:  # noqa: BLE001 — surface bad PDFs in UI
            out[p.name] = f"[EXTRACTION FAILED: {exc}]"
    return out


def _word_doc_sets(texts: dict[str, str]) -> dict[str, set[str]]:
    return {name: set(tokenize(body)) for name, body in texts.items()}


def words_across_docs(word_sets: dict[str, set[str]]) -> dict[str, int]:
    """How many distinct documents contain each word (>=2 => cross-document hook)."""
    counts: dict[str, int] = defaultdict(int)
    for words in word_sets.values():
        for w in words:
            counts[w] += 1
    return dict(counts)


def overlap_sketch_markdown(texts: dict[str, str], max_terms: int = 40) -> str:
    """Offline sketch: corpus stats + terms appearing in multiple PDFs."""
    if not texts:
        return "_No PDFs found in this folder._"

    lines: list[str] = []
    lines.append("## Corpus snapshot\n")
    total_chars = 0
    for name, body in texts.items():
        n = len(body)
        total_chars += n
        bad = body.startswith("[EXTRACTION FAILED")
        flag = " **(failed)**" if bad else ""
        lines.append(f"- **{name}** — {n:,} characters{flag}")
    lines.append(f"\n**Total:** {total_chars:,} characters across {len(texts)} file(s).\n")

    word_sets = _word_doc_sets(texts)
    cross = words_across_docs(word_sets)
    multi = [(w, c) for w, c in cross.items() if c >= 2]
    multi.sort(key=lambda x: (-x[1], x[0]))

    lines.append("\n## Cross-document term hooks (offline)\n")
    lines.append(
        "_Words that appear in **2+** PDFs (after simple tokenization). "
        "Not synonyms — raw overlap hints until an LLM pass exists._\n"
    )
    if not multi:
        lines.append("_No overlapping terms found (very short corpus or different vocabularies)._")
        return "\n".join(lines)

    for w, c in multi[:max_terms]:
        lines.append(f"- `{w}` — in **{c}** document(s)")
    if len(multi) > max_terms:
        lines.append(f"\n_Showing {max_terms} of {len(multi)} overlapping terms._")

    return "\n".join(lines)
