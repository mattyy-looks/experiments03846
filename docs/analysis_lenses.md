# Analysis lenses

This project treats your PDF corpus as a **textual node**: many readings pass through it—different questions, different vocabularies, different theories of knowledge. Each **lens** is a deliberate stance for how the agent (and, later, the model passes behind it) organizes attention.

The sky is large academically; in software we still ship **one constraint per release**. This file is the map; `lenses.py` is the switchboard.

---

## Why multiple lenses?

Hermeneutics, terminology, epistemology, and discourse analysis are not interchangeable—they ask **different questions** of the same strings:

| Lens | Primary question | What often surfaces |
|------|------------------|---------------------|
| **Structural / lexical** | Which language-forms recur across files? | Shared tokens, rough overlap (current offline engine) |
| **Terminological** | How are concepts **named**, stabilized, or blurred? | Synonymy, equivocation, definitional drift |
| **Epistemic** | What counts as **evidence**, authority, proof, or doubt here? | Clashes between ways of knowing |
| **Hermeneutic** | How do texts construct **meaning** in relation to tradition or prior readings? | Horizons, pre-understandings, interpretive circles |
| **Discourse / archive** | What is **sayable** or unsayable under implicit rules? | Silences, formations, conditions of possibility for statements |

None of these replaces careful reading; they **compress attention** so you can compare corpora at scale and then return to the page.

---

## Lens catalog (for prompts & UI)

### Structural — lexical hooks *(live)*

- **Use when:** you want a cheap, honest map of cross-document vocabulary overlap.
- **Limit:** not synonyms or concepts—statistics over tokens after stopword stripping.

### Terminological — concepts & naming *(planned LLM / retrieval pass)*

- **Guiding questions:** Do two texts use different words for the same construct? Does one term split into incompatible senses?
- **Output shape:** candidate glossary, “same term / different definition” table, drift notes.

### Epistemic — ways of knowing *(planned)*

- **Guiding questions:** What modalities appear—empirical, testimonial, deductive, revelatory? Where do texts disagree about *what would count* as settling a dispute?
- **Output shape:** per-document epistemic stance sketch; friction matrix between sources.

### Hermeneutic — horizons & sense-making *(planned)*

- **Guiding questions:** What fore-conceptions must a reader bring? How does each text position itself toward predecessors or interlocutors?
- **Output shape:** fusion-of-horizons sketch (always provisional), lineage of readings—not “the” meaning.

### Discourse / archive — conditions of sayability *(planned)*

- **Guiding questions:** What objects exist as thinkable in each text? What is excluded, minimized, or taken for granted?
- **Output shape:** silences / emphases map; careful language about power—surface patterns, not final moral verdicts.

---

## Epistemic humility (non-negotiable)

The agent should **surface candidate readings and tensions**, attribute claims to **sources**, and mark **SOURCE UNCLEAR** when the corpus does not justify a leap. Heavy interpretive lenses need explicit hedging and invitation back to the primary text.

---

## Implementation notes

- **Today:** the Streamlit control records **which lens you intend**; only `lexical_overlap` has a dedicated offline engine. Others prepend the same sketch plus an honest “not wired yet” note until each lens gets its retrieval + prompt stack.
- **Next:** per-lens system prompts (pulling from `agent_character_and_skills.md`), optional separate chunking or citation anchoring, and exports per lens.

---

## Split of duties: persona vs lenses vs masks

| Layer | File / code | Answers |
|-------|-------------|--------|
| **Persona** | `docs/agent_character_and_skills.md` | *How* the agent speaks: cadence, industrial tone, honesty rules, soundtrack vibe. |
| **Lens** | This doc + `lenses.py` | *What kind of analysis* (terminological, epistemic, discourse, …). |
| **Reader mask** | This doc (catalog) + future `reader_masks` in code | *Which heuristic questions* to foreground—e.g. Foucauldian vs Kantian *angles*, without claiming authority from the dead. |

**Rule of thumb:** keep **voice** in the persona file; keep **methodological presets and philosopher combinations** here so they stay versioned and reproducible.

---

## Reader masks (“as if” a philosopher)

**Intent:** alternate readings of the same corpus **as if** organized by a named style or figure—e.g. a **Foucauldian** pass foregrounding genealogy, institutions, and conditions of truth; slots for other figures or traditions.

This must **not** be ventriloquism. Treat masks as **heuristics**: ordering of questions, salience of tensions. Frame outputs as **interpretive experiments** tied to citations, not as what the philosopher would have concluded off-page.

### Mix and match

You are not limited to one figure.

1. **Sequential passes (recommended first):** same corpus → **Pass A** (mask 1) → **Pass B** (mask 2), clearly labeled sections. Preserves clarity; avoids mush.
2. **Blended constraint card (advanced):** one pass with an explicit prompt that merges **short** bullet constraints from two or more named masks (e.g. Foucault + dialogics). Higher risk of vague synthesis—require section labels that state *which tension comes from which heuristic*.
3. **Custom supplement (open field):** a future UI text area — *“Additional interpretive instructions”* — appends your free-text to the chosen preset(s). Use for one-off experiments; **named presets** stay in this doc or code so runs stay reproducible.

**Implementation sketch (later):** optional **`reader_mask`** (single), **`reader_masks`** (ordered list), or **`reader_mask` + `reader_mask_notes` (open field)** alongside the analysis lens. System prompt = constraint card(s) + **`agent_character_and_skills.md`** (voice only). Offline lexical sketch stays substrate until LLM passes exist.

**Guardrails:** no implied endorsement by historical figures; mark speculation; prefer **SOURCE UNCLEAR** over clever reconstruction.

---

Append new rows here when you invent another reading strategy—then add a matching entry in `lenses.py`.
