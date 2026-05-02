# PDF Research Agent

**Offline research paper analysis.** Drop a folder of PDFs → get structural overlaps, term hooks, and optional AI-powered insights (runs locally on your machine).

---

## ⚡ Quick Start (2 min)

### 1. Setup
```powershell
# One time only
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Run
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Your browser opens to `http://localhost:8501`.

### 3. Use it
- **Paste a folder path** (or click Browse…)
- **Pick an analysis lens** (Epistemic, Structural, etc.)
- **Click RUN ANALYSIS**
- See the overlap sketch + optional DeepSeek AI summary (if Ollama is running)

---

## 📋 What You Get

| Feature | Status |
|---------|--------|
| PDF text extraction | ✅ Working |
| Cross-document term overlap | ✅ Working |
| Epistemic register sketch | ✅ Working |
| Local AI analysis (Ollama) | ✅ Working |
| Custom persona/voice | 🔧 Fill in `docs/agent_character_and_skills.md` |

---

## 🤖 Local AI (Optional but Cool)

If you have **Ollama** installed:
1. Download & run [Ollama](https://ollama.ai)
2. Pull the lightweight model: `ollama pull deepseek-r1:1.5b`
3. Leave it running in your system tray
4. The app will auto-detect it and offer AI analysis

**No API keys. No data leaves your PC.** Everything runs offline.

---

## 🎭 Customize the Agent's Voice

Edit **`docs/agent_character_and_skills.md`** to define:
- Who the agent is (name, personality)
- What they're allowed to do (skills, boundaries)
- How they write (tone, style rules)

Then the prompts will adapt to match.

---

## 📁 File Map

```
.
├── app.py                              # Streamlit UI
├── pdf_extract.py                      # PDF → text + overlap detection
├── epistemic_hints.py                  # Epistemic lens logic
├── lenses.py                           # Analysis frameworks
├── folder_dialog.py                    # Native folder picker
├── requirements.txt                    # Dependencies
├── docs/
│   ├── agent_character_and_skills.md   # YOUR AGENT'S VOICE (fill this in)
│   ├── analysis_lenses.md              # What each lens does
│   └── BUILD_DISCOURSE.md              # Dev notes + philosophy
```

---

## 🔧 Troubleshooting

**"Module not found" errors?**
- Make sure you're running from the project folder
- Check `.venv` was created: `ls .\.venv\Scripts\python.exe`

**"Ollama not running"?**
- Open Ollama from Start Menu / Applications
- Refresh the Streamlit app

**Path picker doesn't work?**
- Paste the path manually (it's fine, the picker is optional)
- Windows Explorer → address bar → Ctrl+A → Ctrl+C → paste here

---

## 🚀 Next Steps

1. **Fill in** `docs/agent_character_and_skills.md` (defines your agent's personality)
2. **Test it** on a small PDF folder
3. **Tweak lenses** in `docs/analysis_lenses.md` if you want custom analysis angles
4. **Share vibes** with me if something cool emerges 👀

---

**Made with curiosity + local-first vibes.** No cloud, no API calls (unless you want 'em). Just PDFs and offline smarts.