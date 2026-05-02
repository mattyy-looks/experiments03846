"""Streamlit UI: PDF folder → extract text → offline overlap sketch (LLM report later)."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from lenses import ANALYSIS_LENSES, LENS_ORDER, format_report_preamble
from pdf_extract import extract_folder, overlap_sketch_markdown


def parse_folder_input(raw: str) -> Path:
    """Strip whitespace and Explorer-style quotes from pasted paths."""
    s = raw.strip().strip('"').strip("'")
    return Path(s).expanduser()

# Big red primary actions — industrial vibe, high visibility.
st.markdown(
    """
<style>
    div[data-testid="stButton"] button {
        background-color: #b30000 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        padding: 0.65rem 1.25rem !important;
        border: none !important;
        border-radius: 6px !important;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #8f0000 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.set_page_config(
    page_title="PDF Research Agent",
    page_icon="📎",
    layout="wide",
)

st.title("PDF Research Agent")
st.caption(
    "Folder of PDFs → choose an **analysis lens** → extract text → offline structural sketch. "
    "Deeper hermeneutic / epistemic passes = next (LLM). See `docs/analysis_lenses.md`."
)

with st.sidebar:
    st.subheader("Persona")
    persona_path = Path(__file__).resolve().parent / "docs" / "agent_character_and_skills.md"
    if persona_path.is_file():
        st.success(f"Using `{persona_path.name}` on disk.")
        with st.expander("Preview first lines"):
            st.text(persona_path.read_text(encoding="utf-8")[:1200] + "\n…")
    else:
        st.warning("Add `docs/agent_character_and_skills.md` for tone rules.")

default_folder = ""
if "folder_path" not in st.session_state:
    st.session_state["folder_path"] = default_folder

folder_input = st.text_input(
    "PDF folder path",
    value=st.session_state["folder_path"],
    placeholder=r"C:\Users\you\Documents\my-pdfs",
    help="Paste a path to an existing folder on this PC. Quotes from File Explorer are OK.",
)
st.session_state["folder_path"] = folder_input.strip()

lens_id = st.selectbox(
    "Analysis lens",
    options=list(LENS_ORDER),
    format_func=lambda k: ANALYSIS_LENSES[k]["label"],
    index=0,
    help="Interpretive stance for this run. Structural/lexical is live offline; others record intent + preamble until wired.",
)

with st.expander("Path not found? (Windows)"):
    st.markdown(
        """
1. Open the folder in **File Explorer**.
2. Click the **address bar** once (or press **Alt+D**), select all (**Ctrl+A**), copy (**Ctrl+C**).
3. Paste here. If Windows wrapped the path in `"quotes"`, they are stripped automatically.

**Checks:** the drive letter exists (e.g. `D:` USB plugged in), spelling matches, and the folder is on **this** machine (not only in cloud-only placeholders unless synced).
        """
    )

col_a, col_b = st.columns(2)
with col_a:
    run = st.button("RUN ANALYSIS", type="primary", use_container_width=True)
with col_b:
    clear = st.button("CLEAR OUTPUT", use_container_width=True)

if clear:
    st.session_state.pop("last_markdown", None)
    st.session_state.pop("last_texts", None)
    st.session_state.pop("last_lens", None)
    st.rerun()

if run:
    path_str = st.session_state["folder_path"]
    if not path_str:
        st.error("Enter a folder path first.")
    else:
        folder = parse_folder_input(path_str)
        resolved = folder.resolve()
        try:
            with st.spinner("Reading PDFs…"):
                texts = extract_folder(folder)
            if not texts:
                st.warning("No `.pdf` files in that folder.")
            else:
                st.session_state["last_texts"] = texts
                st.session_state["last_lens"] = lens_id
                body = overlap_sketch_markdown(texts)
                st.session_state["last_markdown"] = format_report_preamble(lens_id) + body
        except ValueError as e:
            msg = str(e)
            if "does not exist" in msg:
                st.error(
                    f"**Folder not found:** `{resolved}`\n\n"
                    "Confirm the folder exists on **this PC**, the drive is connected, "
                    "and there are no typos. Use the tips under **Path not found?** above."
                )
            elif "Not a folder" in msg:
                st.error(f"**That path is not a folder:** `{resolved}`")
            else:
                st.error(msg)
        except Exception as e:  # noqa: BLE001
            st.exception(e)

if "last_markdown" in st.session_state:
    st.markdown("---")
    lens_note = ""
    if "last_lens" in st.session_state:
        lens_note = f" — {ANALYSIS_LENSES[st.session_state['last_lens']]['label']}"
    st.subheader(f"Report draft (offline sketch){lens_note}")
    st.markdown(st.session_state["last_markdown"])

    with st.expander("Raw extracted text (per file)"):
        texts = st.session_state.get("last_texts") or {}
        for name, body in texts.items():
            st.markdown(f"**{name}**")
            preview = body if len(body) <= 8000 else body[:8000] + "\n\n… _truncated for UI_ …"
            st.text_area(name, preview, height=220, label_visibility="collapsed")
