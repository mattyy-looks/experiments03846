"""Streamlit UI: PDF folder → extract text → offline overlap sketch + optional local LLM analysis (Ollama)."""

from __future__ import annotations

from pathlib import Path
import streamlit as st
import ollama

from epistemic_hints import epistemic_sketch_markdown
from folder_dialog import pick_folder_path
from lenses import ANALYSIS_LENSES, LENS_ORDER, format_report_preamble
from pdf_extract import extract_folder, overlap_sketch_markdown

# ------------------------------------------------------------
# Ollama analysis function (optimised for 8GB RAM)
# ------------------------------------------------------------
def ollama_analyze(texts: dict[str, str], lens_id: str, query: str = "") -> str:
    """Local analysis using Ollama + deepseek-r1:1.5b (lightweight, free)."""
    if not texts:
        return "⚠️ No text to analyze."

    # Limit to 2 PDFs and 1000 chars each – saves RAM
    combined = ""
    count = 0
    for name, body in texts.items():
        if count >= 2:
            break
        combined += f"\n📄 {name}:\n{body[:1000]}\n"
        count += 1

    lens_label = ANALYSIS_LENSES.get(lens_id, {}).get("label", lens_id)

    prompt = f"""Analyse these {count} research paper(s) for: {lens_label}

{combined}

Answer concisely (max 500 words): {query if query else 'What are the main findings?'}"""

    try:
        response = ollama.chat(
            model='deepseek-r1:1.5b',          # smaller model = fits in 8GB
            messages=[{'role': 'user', 'content': prompt}],
            options={
                'temperature': 0.7,
                'num_predict': 800,            # shorter response
                'num_ctx': 2048                # smaller context window
            }
        )
        return response['message']['content']
    except Exception as e:
        return f"❌ Ollama error: {str(e)}\n\n💡 Make sure Ollama is running (system tray)."

# ------------------------------------------------------------
# Original helper functions (unchanged)
# ------------------------------------------------------------
def build_report_markdown(lens_id: str, texts: dict[str, str]) -> str:
    parts: list[str] = [format_report_preamble(lens_id)]
    if lens_id == "epistemic":
        parts.append(epistemic_sketch_markdown(texts))
    parts.append(overlap_sketch_markdown(texts))
    return "\n\n".join(parts)

def parse_folder_input(raw: str) -> Path:
    s = raw.strip().strip('"').strip("'")
    return Path(s).expanduser()

# ------------------------------------------------------------
# Streamlit UI
# ------------------------------------------------------------
st.set_page_config(page_title="PDF Research Agent", page_icon="📎", layout="wide")

# Big red button style
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

st.title("PDF Research Agent")
st.caption(
    "Folder of PDFs → choose an **analysis lens** → extract text → offline structural sketch. "
    "Optional: local AI analysis using Ollama (free, offline)."
)

# Initialize variables with defaults so they're always defined
use_ollama = False
analysis_type = "Quick summary"
custom_query = ""

# ------------------------------------------------------------
# Sidebar (only once, properly indented)
# ------------------------------------------------------------
with st.sidebar:
    st.subheader("Persona")
    persona_path = Path(__file__).resolve().parent / "docs" / "agent_character_and_skills.md"
    if persona_path.is_file():
        st.success(f"Using `{persona_path.name}` on disk.")
        with st.expander("Preview first lines"):
            st.text(persona_path.read_text(encoding="utf-8")[:1200] + "\n…")
    else:
        st.warning("Add `docs/agent_character_and_skills.md` for tone rules.")

    st.divider()
    st.subheader("🤖 Local DeepSeek (Ollama)")
    use_ollama = st.checkbox("Enable AI analysis", value=True,
                             help="Runs locally on your PC - FREE and OFFLINE")

    if use_ollama:
        # Check if Ollama is reachable
        try:
            ollama.list()
            st.success("✅ Ollama connected - DeepSeek ready")
            st.caption("Running completely offline on your machine")
        except:
            st.error("❌ Ollama not running")
            st.info("Open Ollama from Start Menu first, then refresh")

        analysis_type = st.radio(
            "Analysis depth",
            ["Quick summary", "Detailed analysis", "Research gaps", "Custom question"],
            help="More depth = slower but better insights"
        )
        custom_query = ""
        if analysis_type == "Custom question":
            custom_query = st.text_area("What do you want to know about these PDFs?")

# ------------------------------------------------------------
# Folder input row
# ------------------------------------------------------------
default_folder = ""
if "folder_path" not in st.session_state:
    st.session_state["folder_path"] = default_folder

path_col, browse_col = st.columns([1, 0.22])
with path_col:
    folder_input = st.text_input(
        "PDF folder path",
        value=st.session_state["folder_path"],
        placeholder=r"C:\Users\you\Documents\my-pdfs",
        help="Paste a path, or click Browse to choose a folder on this PC.",
    )
    st.session_state["folder_path"] = folder_input.strip()
with browse_col:
    st.markdown("<div style='padding-top: 1.65rem;'></div>", unsafe_allow_html=True)
    if st.button("Browse…", key="browse_pdf_folder", use_container_width=True):
        chosen = pick_folder_path()
        if chosen:
            st.session_state["folder_path"] = chosen
            st.rerun()

# Lens selection
lens_id = st.selectbox(
    "Analysis lens",
    options=list(LENS_ORDER),
    format_func=lambda k: ANALYSIS_LENSES[k]["label"],
    index=0,
)

with st.expander("Path not found? (Windows)"):
    st.markdown(
        """
Try **Browse…** next to the path field first – it fills in the exact folder path.

Manual copy:
1. Open the folder in **File Explorer**.
2. Click the address bar (or press **Alt+D**), select all (**Ctrl+A**), copy (**Ctrl+C**).
3. Paste here. Quotes are stripped automatically.
        """
    )

# Run / Clear buttons
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

# ------------------------------------------------------------
# Main analysis logic
# ------------------------------------------------------------
if run:
    path_str = st.session_state["folder_path"]
    if not path_str:
        st.error("Enter a folder path first.")
    else:
        folder = parse_folder_input(path_str)
        try:
            with st.spinner("📄 Reading PDFs..."):
                texts = extract_folder(folder)
            if not texts:
                st.warning("No `.pdf` files in that folder.")
            else:
                st.session_state["last_texts"] = texts
                st.session_state["last_lens"] = lens_id

                # Always generate the structural sketch
                base_report = build_report_markdown(lens_id, texts)

                if use_ollama:
                    with st.spinner("🧠 DeepSeek analysing (may take 10-30 sec on 8GB RAM)..."):
                        # Map analysis type to a query
                        if analysis_type == "Quick summary":
                            query = "Provide a brief 2-3 paragraph summary."
                        elif analysis_type == "Detailed analysis":
                            query = "Provide a thorough analysis of arguments, evidence, and conclusions."
                        elif analysis_type == "Research gaps":
                            query = "Identify contradictions, unanswered questions, and future research directions."
                        else:  # Custom question
                            query = custom_query

                        ai_analysis = ollama_analyze(texts, lens_id, query)

                        final_report = f"""{base_report}

---

## 🧠 DeepSeek AI Analysis ({analysis_type})

{ai_analysis}

---
*Analysis ran 100% locally on your machine using Ollama + DeepSeek. No data left your computer.*
"""
                        st.session_state["last_markdown"] = final_report
                else:
                    st.session_state["last_markdown"] = base_report

        except Exception as e:
            st.exception(e)

# ------------------------------------------------------------
# Display results
# ------------------------------------------------------------
if "last_markdown" in st.session_state:
    st.markdown("---")
    lens_note = ""
    if "last_lens" in st.session_state:
        lens_note = f" — {ANALYSIS_LENSES[st.session_state['last_lens']]['label']}"
    st.subheader(f"Report draft{lens_note}")
    st.markdown(st.session_state["last_markdown"])

    with st.expander("Raw extracted text (per file)"):
        texts = st.session_state.get("last_texts") or {}
        for name, body in texts.items():
            st.markdown(f"**{name}**")
            preview = body if len(body) <= 8000 else body[:8000] + "\n\n… _truncated for UI_ …"
            st.text_area(name, preview, height=220, label_visibility="collapsed")
