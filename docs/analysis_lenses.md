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

Append new rows here when you invent another reading strategy—then add a matching entry in `lenses.py`.
