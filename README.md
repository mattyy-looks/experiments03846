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

From this folder in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Your browser should open to a local URL (usually `http://localhost:8501`). Paste the **absolute path** to a folder that contains `.pdf` files, then click **RUN ANALYSIS**.

- **Offline sketch:** the app extracts text and lists **cross-document term hooks** (words appearing in 2+ PDFs). This is not yet the full narrative report or synonym detection — that comes with an LLM pass.
- **Secrets:** when we add API keys, use a `.env` file (already gitignored). See `.env.example` when it exists.

## What to do next (in order)

1. Fill in **`docs/agent_character_and_skills.md`** — your agent’s voice and boundaries.
2. Run **`streamlit run app.py`** and test on a small PDF folder.
3. Add **`.env`** + LLM-backed report section when ready.

## Files

| Path | Purpose |
|------|--------|
| `app.py` | Streamlit UI (big red buttons, folder path, report sketch) |
| `pdf_extract.py` | PDF text extraction + offline overlap hints |
| `requirements.txt` | Python dependencies |
| `docs/agent_character_and_skills.md` | Character, tone, and “skills” the agent should behave as if it has |
