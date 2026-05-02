"""Streamlit UI: PDF folder → extract text → offline overlap sketch (LLM report later)."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from epistemic_hints import epistemic_sketch_markdown
from folder_dialog import pick_folder_path
from lenses import ANALYSIS_LENSES, LENS_ORDER, format_report_preamble
from pdf_extract import extract_folder, overlap_sketch_markdown

from openai import OpenAI
import os
from pathlib import Path
import streamlit as st
from epistemic_hints import epistemic_sketch_markdown
from folder_dialog import pick_folder_path
from lenses import ANALYSIS_LENSES, LENS_ORDER, format_report_preamble
from pdf_extract import extract_folder, overlap_sketch_markdown

import ollama





# Initialize DeepSeek client
@st.cache_resource
def get_deepseek_client():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        st.warning("⚠️ No DEEPSEEK_API_KEY found in environment variables. DeepSeek features disabled.")
        return None
    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

deepseek_client = get_deepseek_client()

def deepseek_analyze(texts: dict[str, str], lens_id: str, query: str = "") -> str:
    """Use DeepSeek to generate intelligent analysis of PDF contents."""
    if not deepseek_client:
        return "⚠️ DeepSeek API key not configured. Set DEEPSEEK_API_KEY environment variable."
    
    # Combine texts (limit to avoid token limits)
    combined = "\n\n---\n\n".join([
        f"FILE: {name}\n\n{body[:3000]}"  # First 3000 chars per file
        for name, body in list(texts.items())[:5]  # First 5 PDFs
    ])
    
    lens_label = ANALYSIS_LENSES.get(lens_id, {}).get("label", lens_id)
    
    system_prompt = """You are a research analysis assistant. Analyze the provided academic PDF extracts.
Be specific, cite evidence from the texts, and identify patterns, contradictions, or gaps.
Use clear academic tone but accessible language. Markdown formatting OK."""
    
    user_prompt = f"""Analysis lens: {lens_label}
{query if query else f"Analyze these research papers focusing on: {lens_label}"}

PDF extracts:
{combined}

Provide detailed analysis with specific references to the texts."""
    
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ DeepSeek error: {str(e)}"

def ollama_analyze(texts: dict[str, str], lens_id: str, query: str = "") -> str:
    """Use local Ollama + DeepSeek for free, offline analysis."""
    if not texts:
        return "⚠️ No text to analyze."
    
    # Limit to save RAM and speed up
    combined = "\n\n---\n\n".join([
        f"📄 FILE: {name}\n\n{body[:2000]}"  # First 2000 chars per file
        for name, body in list(texts.items())[:3]  # First 3 PDFs
    ])
    
    lens_label = ANALYSIS_LENSES.get(lens_id, {}).get("label", lens_id)
    
    prompt = f"""You are a research analyst. Analyze these academic papers.

🔍 Analysis lens: {lens_label}

{f"❓ Question: {query}" if query else f"📋 Task: Provide a detailed analysis focusing on {lens_label}"}

📑 Papers:
{combined}

🎯 Output requirements:
- Be specific and cite evidence from the texts
- Identify patterns, contradictions, or gaps
- Use clear academic tone
- Format with markdown (headings, bullet points)

Analysis:"""

    try:
        response = ollama.chat(
            model='deepseek-r1:7b',  # or 'deepseek-r1:1.5b' if 7b is too heavy
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.7, 'num_predict': 1500}  # limits response length
        )
        return response['message']['content']
    except Exception as e:
        return f"❌ Ollama error: {str(e)}\n\n💡 Make sure Ollama is running (check system tray)"
        


def build_report_markdown(lens_id: str, texts: dict[str, str]) -> str:
    parts: list[str] = [format_report_preamble(lens_id)]
    if lens_id == "epistemic":
        parts.append(epistemic_sketch_markdown(texts))
    parts.append(overlap_sketch_markdown(texts))
    return "\n\n".join(parts)


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
    "Epistemic lens = offline register sketch + overlap; other lenses = overlap until wired. See `docs/analysis_lenses.md`."
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

with st.sidebar:
    st.subheader("Persona")
    persona_path = Path(__file__).resolve().parent / "docs" / "agent_character_and_skills.md"
    if persona_path.is_file():
        st.success(f"Using `{persona_path.name}` on disk.")
        with st.expander("Preview first lines"):
            st.text(persona_path.read_text(encoding="utf-8")[:1200] + "\n…")
    else:
        st.warning("Add `docs/agent_character_and_skills.md` for tone rules.")

    with st.sidebar:
    st.subheader("Persona")
    persona_path = Path(__file__).resolve().parent / "docs" / "agent_character_and_skills.md"
    if persona_path.is_file():
        st.success(f"Using `{persona_path.name}` on disk.")
        with st.expander("Preview first lines"):
            st.text(persona_path.read_text(encoding="utf-8")[:1200] + "\n…")
    else:
        st.warning("Add `docs/agent_character_and_skills.md` for tone rules.")
    
    # ========== ADD THIS DEEPSEEK SECTION ==========
    st.divider()
    st.subheader("🤖 Local DeepSeek (Ollama)")
    use_ollama = st.checkbox("Enable AI analysis", value=True, help="Runs locally on your PC - FREE and OFFLINE")
    
    if use_ollama:
        # Check if Ollama is running
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
    # ========== END DEEPSEEK SECTION ==========
    
    # ========== ADD THIS DEEPSEEK SECTION HERE ==========
    st.divider()  # adds a nice line separator
    st.subheader("🤖 DeepSeek AI Analysis")
    use_deepseek = st.checkbox("Enable DeepSeek analysis (requires API key)")
    
    if use_deepseek and not deepseek_client:
        st.error("⚠️ Set DEEPSEEK_API_KEY in environment variables")
        st.code("""# Windows PowerShell:
$env:DEEPSEEK_API_KEY="your-key-here"

# Mac/Linux:
export DEEPSEEK_API_KEY="your-key-here"

# Or create .env file and use python-dotenv
""")
    
    if use_deepseek and deepseek_client:
        analysis_type = st.radio(
            "Analysis type",
            ["Summary & synthesis", "Key claims & evidence", "Research gaps", "Custom query"]
        )
        custom_query = ""
        if analysis_type == "Custom query":
            custom_query = st.text_area("Your question about these PDFs:")
    # ========== END OF DEEPSEEK SECTION ==========


default_folder = ""
if "folder_path" not in st.session_state:
    st.session_state["folder_path"] = default_folder

path_col, browse_col = st.columns([1, 0.22])
with path_col:
    folder_input = st.text_input(
        "PDF folder path",
        value=st.session_state["folder_path"],
        placeholder=r"C:\Users\you\Documents\my-pdfs",
        help="Paste a path, or click Browse to choose a folder on this PC. Quotes from Explorer are OK.",
    )
    st.session_state["folder_path"] = folder_input.strip()
with browse_col:
    st.markdown(
        "<div style='padding-top: 1.65rem;'></div>",
        unsafe_allow_html=True,
    )
    if st.button(
        "Browse…",
        key="browse_pdf_folder",
        use_container_width=True,
        help="Opens your system folder picker (only when the app runs on this computer).",
    ):
        chosen = pick_folder_path()
        if chosen:
            st.session_state["folder_path"] = chosen
            st.rerun()

lens_id = st.selectbox(
    "Analysis lens",
    options=list(LENS_ORDER),
    format_func=lambda k: ANALYSIS_LENSES[k]["label"],
    index=0,
    help="Structural = overlap only. Epistemic = register heuristic + overlap. Others = overlap + planned preamble until wired.",
)

with st.expander("Path not found? (Windows)"):
    st.markdown(
        """
Try **Browse…** next to the path field first—it fills in the exact folder path.

Manual copy:

1. Open the folder in **File Explorer**.
2. Click the **address bar** once (or press **Alt+D**), select all (**Ctrl+A**), copy (**Ctrl+C**).
3. Paste here. If Windows wrapped the path in `"quotes"`, they are stripped automatically.

**Checks:** the drive letter exists (e.g. `D:` USB plugged in), spelling matches, and the folder is on **this** machine (not only in cloud-only placeholders unless synced).

**Remote deploy:** Browse uses your PC only when Streamlit runs locally; on a headless server there is no mouse picker—paste paths instead.
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
                st.session_state["last_markdown"] = build_report_markdown(lens_id, texts)
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
