"""Streamlit UI: PDF folder → extract text → offline overlap sketch (LLM report later)."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from pdf_extract import extract_folder, overlap_sketch_markdown

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
st.caption("Folder of PDFs → extract text → offline overlap sketch. Full narrative report = next step (LLM).")

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
    help="Absolute path to a folder that contains .pdf files.",
)
st.session_state["folder_path"] = folder_input.strip()

col_a, col_b = st.columns(2)
with col_a:
    run = st.button("RUN ANALYSIS", type="primary", use_container_width=True)
with col_b:
    clear = st.button("CLEAR OUTPUT", use_container_width=True)

if clear:
    st.session_state.pop("last_markdown", None)
    st.session_state.pop("last_texts", None)
    st.rerun()

if run:
    path_str = st.session_state["folder_path"]
    if not path_str:
        st.error("Enter a folder path first.")
    else:
        folder = Path(path_str)
        try:
            with st.spinner("Reading PDFs…"):
                texts = extract_folder(folder)
            if not texts:
                st.warning("No `.pdf` files in that folder.")
            else:
                st.session_state["last_texts"] = texts
                st.session_state["last_markdown"] = overlap_sketch_markdown(texts)
        except Exception as e:  # noqa: BLE001
            st.exception(e)

if "last_markdown" in st.session_state:
    st.markdown("---")
    st.subheader("Report draft (offline sketch)")
    st.markdown(st.session_state["last_markdown"])

    with st.expander("Raw extracted text (per file)"):
        texts = st.session_state.get("last_texts") or {}
        for name, body in texts.items():
            st.markdown(f"**{name}**")
            preview = body if len(body) <= 8000 else body[:8000] + "\n\n… _truncated for UI_ …"
            st.text_area(name, preview, height=220, label_visibility="collapsed")
