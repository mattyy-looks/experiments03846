# PDF Research Agent

Analyzes a folder of PDFs, surfaces themes, overlaps, synonyms, and tensions, then drafts a structured report. UI will come after the core pipeline works.

## Open this project in Cursor

1. **Menu:** **File → Open Folder…** (or **Ctrl+K Ctrl+O**).
2. Choose: `C:\Users\user1\projects\pdf-research-agent`.
3. Press **Open**.

That folder becomes your **workspace root** — chat and terminals run from here.

## Optional: pin this folder

Use **File → Add Folder to Workspace…** only if you want multiple roots; for one app, a single open folder is enough.

## What to do next (in order)

1. Fill in **`docs/agent_character_and_skills.md`** — your agent’s voice and boundaries.
2. Add a **`.env`** when we wire the AI (never commit secrets — `.gitignore` will list `.env`).
3. We’ll add Python (or another stack you prefer), PDF extraction, then report generation, then a simple web UI with your big red buttons.

## Files

| Path | Purpose |
|------|--------|
| `docs/agent_character_and_skills.md` | Character, tone, and “skills” the agent should behave as if it has |
