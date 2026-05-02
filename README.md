# PDF Research Agent

Analyzes a folder of PDFs, surfaces themes, overlaps, synonyms, and tensions, then drafts a structured report. UI will come after the core pipeline works.

## Open this project in Cursor

1. **Menu:** **File → Open Folder…** (or **Ctrl+K Ctrl+O**).
2. Choose: `C:\Users\user1\projects\pdf-research-agent`.
3. Press **Open**.

That folder becomes your **workspace root** — chat and terminals run from here.

## Optional: pin this folder

Use **File → Add Folder to Workspace…** only if you want multiple roots; for one app, a single open folder is enough.

## Run the Streamlit app (Python 3.10+)

Use **PowerShell** and `cd` to this project folder first, e.g. `C:\Users\user1\projects\pdf-research-agent`.

**Recommended (no `Activate.ps1` — works when execution policy blocks scripts):** use the venv’s `python.exe` and run Streamlit as a **module** so the right environment is always used.

```powershell
# One-time: create venv and install deps
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Every time: start the app
.\.venv\Scripts\python.exe -m streamlit run app.py
```

**The `-r` in `pip install -r requirements.txt` is required:** it tells pip to install *from a requirements file*.  
If you run `pip install requirements.txt` (no `-r`), pip thinks you want a package literally named `requirements.txt` and will complain.

**If `.\.venv\...` is “not found”:** you are not in the project directory, or the venv was never created — run the one-time block from the folder that contains `app.py`.

**Optional — classic activate + `streamlit` on PATH:**

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

If activation fails with *running scripts is disabled*, either keep using `.\.venv\Scripts\python.exe -m ...` above, or (once) run:  
`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

Your browser should open to a local URL (usually `http://localhost:8501`). Set the PDF folder by pasting its **absolute path** or click **Browse…** (opens the Windows folder picker when Streamlit runs on your PC). Then click **RUN ANALYSIS**.

- **Offline sketch:** the app extracts text and lists **cross-document term hooks** (words appearing in 2+ PDFs). This is not yet the full narrative report or synonym detection — that comes with an LLM pass.
- **LLM (optional):** copy `.env.example` → `.env` and set `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`. See **`docs/LLM_SETUP.md`** (DeepSeek cloud + self-hosted). Use `llm_client.chat_completion(...)` from code.

## What to do next (in order)

1. Fill in **`docs/agent_character_and_skills.md`** — your agent’s voice and boundaries.
2. Run **`.\.venv\Scripts\python.exe -m streamlit run app.py`** and test on a small PDF folder.
3. Add **`.env`** + LLM-backed report section when ready.

## Files

| Path | Purpose |
|------|--------|
| `app.py` | Streamlit UI (big red buttons, folder path, report sketch) |
| `pdf_extract.py` | PDF text extraction + offline overlap hints |
| `llm_client.py` | OpenAI-compatible chat helper (`LLM_*` env vars) |
| `folder_dialog.py` | Native folder picker (Tk) for local runs |
| `epistemic_hints.py` | Offline epistemic register counts for the epistemic lens |
| `lenses.py` | Named analysis lenses (labels + preamble for future LLM routing) |
| `requirements.txt` | Python dependencies |
| `docs/agent_character_and_skills.md` | Character, tone, and “skills” the agent should behave as if it has |
| `docs/analysis_lenses.md` | Hermeneutic / terminological / epistemic / discourse lenses — intent & prompts map |
| `docs/BUILD_DISCOURSE.md` | Session notes: local-first scope, philosophy, and how to pace feature work |
