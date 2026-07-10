# Deliverables — "Generative AI in Action" review

| File | What it is |
|---|---|
| `post.md` | Complete markdown article |
| `review_notebook.py` | marimo notebook: article companion with all 6 interactive widgets (validated: runs in script mode, passes `marimo check`) |

Run the notebook: `/opt/anaconda3/bin/python -m marimo run review_notebook.py`
Publish as a static interactive page: `marimo export html-wasm review_notebook.py -o out/` (all widgets are simulation-only, so it is WASM-friendly: no API calls, no file IO).

## Publication metadata

**SEO title** (58 chars):
`Generative AI in Action Review: Thinking in AI Systems`

**Meta description** (155 chars):
`A developer-tooling perspective on Amit Bahree's Generative AI in Action: why the book's real lesson is architecture, evaluation, and trust, not prompts.`

**Suggested URL slug:**
`generative-ai-in-action-review`

**Estimated reading time:** 8 minutes (1,639 words), ~12 minutes with the interactive widgets.

**Social preview text:**
`I won a book in an Anaconda raffle at PyData Boston and it quietly replaced my mental model of AI products. My review of Generative AI in Action, with interactive marimo explainers for temperature, RAG, the GenAI stack, and more.`

**Pull quote (top of article):**
> "I expected a book about how language models work. I finished it thinking about orchestration layers, evaluation budgets, and why grounding is a trust decision, not a technical one."

## Suggested illustrations to generate

1. **Hero:** a raffle ticket morphing into a layered architecture diagram, flat minimal style, Anaconda green (#43B02A) accent on off-white.
2. **Section 2:** a prompt shown as the visible tip of an iceberg; beneath the waterline: orchestration, retrieval, evals, infrastructure.
3. **Section 4 (stack):** clean 8-layer stack diagram with the orchestration layer highlighted, "trust is implemented here" annotation.
4. **Evals section:** a balance scale weighing "generation (cheap)" against "judgment (scarce)".
5. **Footer:** small line drawing of a conference booth with a fishbowl of raffle tickets.

## Interactive widgets (in `review_notebook.py`)

1. **Model Configuration Playground** — temperature/top_p/penalties/max-tokens/seed sliders; live Altair chart of the next-token distribution (kept vs. cut by top_p); per-parameter intuition table; simulated continuations. No LLM calls.
2. **Prompt Engineering Explorer** — zero-shot / few-shot / chain of thought / system prompt / structured prompt, each with the prompt text and expected behavioral differences.
3. **LLM Product Stack Explorer** — clickable 8-layer stack (Application → Infrastructure); each layer expands with what product teams need to think about.
4. **When should you fine-tune?** — five-question decision helper recommending Prompting / RAG / Fine-tuning / Model selection, following the book's prompt-first ordering.
5. **Responsible AI Checklist** — seven controls with a production-readiness score.
6. **Poll** — "What book should I review next?" (client-side only).

## Fact-grounding notes

All book claims trace to the PDF: model configuration and the "temperature or top_p, not both" advice (ch. 2.8); penalties and randomness (ch. 3); prompt patterns (ch. 6); RAG, chunking, and provider-incompatible embeddings (ch. 7 and 2.8); adaptation ordering (ch. 9); Software 2.0, copilots, LAMP analogy, GenAI app stack, orchestration/grounding/response filtering (ch. 10); latency, quotas, PAYGO (ch. 11); BLEU/ROUGE/BERTScore, G-Eval, HELM (ch. 12); hallucination, prompt injection, insecure output handling, overreliance (ch. 13).
