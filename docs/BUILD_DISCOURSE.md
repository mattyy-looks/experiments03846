# Build discourse

Archived notes from collaborative sessions while shaping this project—why it matters, how to steer scope, and how “local” fits together with optional cloud helpers later.

*May 2026.*

---

## Milestones worth naming

The valuable part is rarely the abstract idea—it is **shipping**: a repo, a Streamlit UI that runs on Windows, clearer PDF-folder handling (quotes from Explorer, explicit “path does not exist”), Git history, and a deliberate **persona** captured in `agent_character_and_skills.md` (including soundtrack-inspired tone notes).

Patting yourself on the back for execution is appropriate. Turning a fuzzy goal into working habits and artifacts is the scarce skill.

---

## “Local,” disk, and the internet

What exists today is intentionally **grounded on your machine**:

- PDFs live on **your drive**.
- Text extraction and the offline **overlap sketch** do not need network access.

When a **large-language-model pass** is added for richer reports (themes, synonyms, tensions written out as narrative), the usual shape is: **your PC sends processed text to an API** when you choose that route—that implies **an internet connection** and **your keys**, unless you later adopt a fully offline model.

Same moral either way: **your corpus stays local**; you decide **who** generates the language layer.

---

## Infinite knobs vs steady progress

There are hundreds of nuanced manipulations you could add—weighting, clustering, glossary extraction, contradiction graphs, exports, audience-specific tones—and that freedom can feel infinite.

A practical guardrail: pick **one deliberate constraint per iteration**—for example, “synonym-first glossary” or “contradiction callouts only”—and ship it. Keep a backlog so possibility stays **optionality**, not chaos.

---

## Ideas, execution, and “being pillaged”

Ideas feel fragile because they are abstract—but delivery is **slow work**: coding, maintenance, taste, and choosing whose problem you solve. Someone copying a headline idea still must **build and sustain**.

A “business mind” is partly learnable (who it is for, pricing, one sharp sentence of value)—and partly orthogonal to whether today’s build deserves pride.

---

## How this file is meant to be used

Treat `BUILD_DISCOURSE.md` as **design folklore**: remind future-you why the agent exists, how scope was negotiated, and what “local-first” actually meant at this stage of the stack.

Append new dated sections when another leap lands worth remembering.
