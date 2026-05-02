# Wiring an LLM (DeepSeek and others)

You need **something the code can call over HTTP**: usually an **API key** for a hosted service, or a **base URL** (and sometimes a key) for an instance you run yourself.

This project uses the **OpenAI Python SDK** with an optional **custom base URL**, which matches:

- **DeepSeek API** (cloud)
- Many **self-hosted** DeepSeek / LLM servers that expose OpenAI-compatible `/v1/chat/completions`
- **Ollama** with OpenAI compatibility (`/v1`)

Configuration is via **`.env`** in the project root (copy from `.env.example`). Never commit `.env`.

---

## 1. DeepSeek (official API)

1. Create a key in the DeepSeek console (API section).
2. In `.env`:

```env
LLM_BASE_URL=https://api.deepseek.com
LLM_API_KEY=sk-xxxxxxxx
LLM_MODEL=deepseek-chat
```

3. Install deps and test from project root:

```powershell
.\.venv\Scripts\python.exe -m pip install openai
.\.venv\Scripts\python.exe -c "from llm_client import chat_completion; print(chat_completion('You are brief.', 'Say hello in 5 words.'))"
```

---

## 2. Your own DeepSeek “instance” (self-hosted)

Depends how you deployed it.

**OpenAI-compatible server** (common for vLLM, Text Generation Inference, some gateways):

```env
LLM_BASE_URL=http://127.0.0.1:PORT/v1
LLM_API_KEY=anything-or-empty-per-your-server
LLM_MODEL=the-model-name-your-server-expects
```

Use the exact **base URL** your stack docs give (often ends with `/v1`). **API key** may be unused locally; some stacks still want a non-empty string — set `LLM_API_KEY=local` if needed.

**Ollama** (example):

```env
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=deepseek-r1:8b
```

(Use whatever model tag you actually pulled.)

---

## 3. Hooking the Streamlit app

`llm_client.chat_completion(...)` is ready for prompts built from extracted PDF text + `docs/agent_character_and_skills.md`. The UI button / lens wiring is the next small step—call this after `extract_folder()` so you pass **truncated** or **chunked** text to stay within context limits and cost.

---

## 4. Keys and safety

- **Cloud APIs:** treat keys like passwords; rotate if leaked.
- **Local instances:** still avoid exposing unauthenticated endpoints on the public internet.

---

## 5. Troubleshooting

| Symptom | Check |
|--------|--------|
| 401 / Unauthorized | `LLM_API_KEY` wrong or missing for that host |
| Connection refused | Wrong host/port; instance not running |
| Model not found | `LLM_MODEL` must match server’s model id exactly |
| Empty reply | Context too long — shorten input or raise limits on server |
