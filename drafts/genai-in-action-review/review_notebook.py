# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "altair>=5.0.0",
#     "pandas>=2.0.0",
#     "numpy>=1.26.0",
# ]
# ///

"""Interactive companion to the blog post reviewing
"Generative AI in Action" by Amit Bahree (Manning).

Five teaching widgets plus a poll. No LLM calls anywhere:
every behavior is simulated so the notebook is reproducible,
runs in WASM, and costs nothing to explore.
"""

import marimo

__generated_with = "0.23.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import altair as alt

    GREEN = "#43B02A"  # Anaconda green, used as the single accent
    GRAY = "#9aa3b2"
    return GRAY, GREEN, alt, mo, np, pd


@app.cell
def _(mo):
    mo.md(r"""
    # Generative AI in Action, interactively

    Companion widgets for my review of **Generative AI in Action** by Amit Bahree
    (Manning). Each one teaches a concept from the book through simulation, not
    through model calls, so everything here is deterministic, free, and
    reproducible.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1 · Model Configuration Playground

    The book treats configuration as a first-class concept: temperature, top_p,
    penalties, and max tokens decide how much unpredictability you ship. Move the
    sliders and watch how the *same* model would behave differently as a product.

    **What you learn:** configuration is a product surface. The chart shows the
    probability distribution for the next token after the prompt
    *"The experiment produced a surprising"*, reshaped by your settings.
    """)
    return


@app.cell
def _(mo):
    temperature = mo.ui.slider(0.0, 2.0, step=0.1, value=0.7, label="temperature")
    top_p = mo.ui.slider(0.05, 1.0, step=0.05, value=1.0, label="top_p")
    presence_penalty = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.0, label="presence penalty")
    frequency_penalty = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.0, label="frequency penalty")
    max_tokens = mo.ui.slider(16, 512, step=16, value=256, label="max tokens")
    fixed_seed = mo.ui.checkbox(value=False, label="fixed seed (when the provider supports it)")

    mo.vstack(
        [
            mo.hstack([temperature, top_p], justify="start", gap=2),
            mo.hstack([presence_penalty, frequency_penalty], justify="start", gap=2),
            mo.hstack([max_tokens, fixed_seed], justify="start", gap=2),
        ]
    )
    return (
        fixed_seed,
        frequency_penalty,
        max_tokens,
        presence_penalty,
        temperature,
        top_p,
    )


@app.cell
def _(np, pd, temperature, top_p):
    # A hand-designed next-token distribution (illustrative, not from a model).
    candidate_tokens = ["result", "pattern", "signal", "outcome", "smell", "melody", "universe", "apology"]
    base_probs = np.array([0.34, 0.22, 0.16, 0.12, 0.07, 0.05, 0.03, 0.01])

    # Temperature rescales log-probabilities. T -> 0 approaches argmax.
    T = max(temperature.value, 1e-3)
    logits = np.log(base_probs)
    scaled = np.exp(logits / T)
    probs = scaled / scaled.sum()

    # top_p (nucleus sampling) keeps the smallest set of tokens whose
    # cumulative probability reaches the threshold; the rest are cut.
    order = np.argsort(probs)[::-1]
    cumulative = np.cumsum(probs[order])
    keep_count = int(np.searchsorted(cumulative, top_p.value) + 1)
    kept_indices = set(order[:keep_count].tolist())

    dist_df = pd.DataFrame(
        {
            "token": candidate_tokens,
            "probability": probs,
            "status": ["sampled from" if i in kept_indices else "cut by top_p" for i in range(len(candidate_tokens))],
        }
    )
    return (dist_df,)


@app.cell
def _(GRAY, GREEN, alt, dist_df):
    config_chart = (
        alt.Chart(dist_df)
        .mark_bar(cornerRadiusEnd=4, height=16)
        .encode(
            x=alt.X("probability:Q", axis=alt.Axis(format="%", title="next-token probability", grid=True, gridOpacity=0.25)),
            y=alt.Y("token:N", sort="-x", title=None),
            color=alt.Color(
                "status:N",
                scale=alt.Scale(domain=["sampled from", "cut by top_p"], range=[GREEN, GRAY]),
                legend=alt.Legend(title=None, orient="top"),
            ),
            tooltip=[alt.Tooltip("token:N"), alt.Tooltip("probability:Q", format=".1%"), alt.Tooltip("status:N")],
        )
        .properties(width=560, height=230, title=alt.Title("What the sampler actually sees", fontSize=14))
        .configure_view(strokeOpacity=0)
    )
    config_chart
    return


@app.cell
def _(
    fixed_seed,
    frequency_penalty,
    max_tokens,
    mo,
    presence_penalty,
    temperature,
    top_p,
):
    def temp_reading(t):
        if t <= 0.3:
            return "**Deterministic zone.** Conservative, predictable, repetitive on retries. Right for extraction, classification, and anything a test asserts on."
        if t <= 0.8:
            return "**Balanced zone.** The book's practical default (around 0.7 to 0.8): coherent but not robotic. Right for assistants and summarization."
        if t <= 1.2:
            return "**Creative zone.** More surprising word choices, more variance between runs. Right for brainstorming, risky for facts."
        return "**High-variance zone.** Output gets genuinely unpredictable and hallucination risk climbs. Use with guardrails, or for art."

    def top_p_reading(p):
        if p <= 0.3:
            return "Only the head of the distribution survives (the gray bars are cut). Very predictable, can feel like it repeats itself."
        if p <= 0.9:
            return "A moderate nucleus: unlikely tokens are trimmed, common ones compete. A frequent production compromise."
        return "Nearly the whole distribution is eligible, including the long tail. Variety comes from temperature instead of truncation."

    def penalty_reading(presence, frequency):
        notes = []
        if presence > 0.5:
            notes.append("presence penalty is pushing the model toward **new topics**")
        elif presence < -0.5:
            notes.append("negative presence penalty encourages **staying on topic**, at the risk of loops")
        if frequency > 0.5:
            notes.append("frequency penalty is suppressing **verbatim repetition**")
        elif frequency < -0.5:
            notes.append("negative frequency penalty tolerates repeated phrases")
        return "With these penalties, " + " and ".join(notes) + "." if notes else "Penalties near zero: repetition is governed by the model's own habits."

    seed_note = (
        "Seed fixed: retries reproduce the same sample, which makes demos and tests honest."
        if fixed_seed.value
        else "No seed: every retry may differ, even at identical settings."
    )

    mo.md(
        f"""
    | setting | value | how the output shifts |
    |---|---|---|
    | temperature | `{temperature.value:.1f}` | {temp_reading(temperature.value)} |
    | top_p | `{top_p.value:.2f}` | {top_p_reading(top_p.value)} |
    | penalties | `{presence_penalty.value:+.1f}` / `{frequency_penalty.value:+.1f}` | {penalty_reading(presence_penalty.value, frequency_penalty.value)} |
    | max tokens | `{max_tokens.value}` | Hard stop at {max_tokens.value} tokens, even mid-sentence. Longer caps raise latency and cost. |
    | seed | `{"fixed" if fixed_seed.value else "none"}` | {seed_note} |

    *Book tip worth engraving somewhere: adjust temperature **or** top_p, not both.*
    """
    )
    return


@app.cell
def _(mo, temperature):
    simulated = (
        "The experiment produced a surprising result, consistent with the model's predictions."
        if temperature.value <= 0.3
        else "The experiment produced a surprising pattern, one the team had not planned to look for."
        if temperature.value <= 1.0
        else "The experiment produced a surprising melody of data, as if the instrument had opinions."
    )
    mo.md(
        f"""**Simulated continuation at this temperature** (illustrative, no model was called):

    > The experiment produced a surprising {simulated.split("surprising ", 1)[1]}"""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2 · Prompt Engineering Explorer

    Chapter 6 catalogs the prompt patterns everyone eventually rediscovers. Switch
    between them to compare the prompt itself and the behavior you should expect.

    **What you learn:** patterns are not magic phrasing. Each one trades effort,
    tokens, and control differently.
    """)
    return


@app.cell
def _(mo):
    prompt_pattern = mo.ui.radio(
        options=["Zero-shot", "Few-shot", "Chain of Thought", "System prompt", "Structured prompt"],
        value="Zero-shot",
        label="pattern",
    )
    prompt_pattern
    return (prompt_pattern,)


@app.cell
def _(mo, prompt_pattern):
    prompt_patterns = {
        "Zero-shot": (
            "Classify the sentiment of this review as positive, negative, or mixed:\n\n"
            '"The install was painless but the docs assume telepathy."',
            "No examples, just the task. Cheapest in tokens and effort. Quality depends entirely on how common the task was in training. Expect confident answers with occasional format drift.",
        ),
        "Few-shot": (
            'Review: "Setup took an afternoon." -> mixed\n'
            'Review: "Crashes on launch, every time." -> negative\n'
            'Review: "Docs are great, works out of the box." -> positive\n\n'
            'Review: "The install was painless but the docs assume telepathy." ->',
            "In-context examples anchor both the labels and the output format. Costs more tokens, buys consistency. The book frames this as in-context learning: the model imitates the pattern you show it.",
        ),
        "Chain of Thought": (
            "Classify the sentiment. Think step by step: first list the positive claims, "
            "then the negative claims, then weigh them before answering.\n\n"
            '"The install was painless but the docs assume telepathy."',
            "Asking for intermediate reasoning improves multi-step tasks. Slower and more verbose, and the reasoning text itself is for the model's benefit, not necessarily a faithful account. Use for logic, not for lookups.",
        ),
        "System prompt": (
            "System: You are a support triage assistant. Always answer with exactly one word: "
            "positive, negative, or mixed. Never explain.\n\n"
            'User: "The install was painless but the docs assume telepathy."',
            "The system role sets persistent rules the user message cannot easily see or edit. This is where products encode identity, tone, and boundaries. Most guardrails start here.",
        ),
        "Structured prompt": (
            "Classify the review below.\n\n"
            "### Review\nThe install was painless but the docs assume telepathy.\n\n"
            "### Output format (JSON)\n{\"sentiment\": \"positive|negative|mixed\", \"confidence\": 0.0}",
            "Clear syntax, delimiters, and an explicit schema make outputs parseable by software, not just readable by humans. The moment another system consumes the output, this stops being optional.",
        ),
    }
    prompt_text, prompt_diff = prompt_patterns[prompt_pattern.value]
    mo.vstack(
        [
            mo.md(f"**The prompt**\n```text\n{prompt_text}\n```"),
            mo.md(f"**What changes:** {prompt_diff}"),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 3 · LLM Product Stack Explorer

    Chapter 10 maps a GenAI application stack the way we once mapped LAMP. Click
    through the layers. The model is two layers from the bottom, which is exactly
    the point.

    **What you learn:** most product risk lives in the middle of the stack, not in
    the model.
    """)
    return


@app.cell
def _(mo):
    stack_layer = mo.ui.radio(
        options=["Application", "Orchestration", "Retrieval", "Embeddings", "Model", "Safety", "Evaluation", "Infrastructure"],
        value="Orchestration",
        label="inspect a layer",
    )
    stack_layer
    return (stack_layer,)


@app.cell
def _(GREEN, mo, stack_layer):
    stack_layers = {
        "Application": "The copilot or product the user touches. Teams must decide: where does AI help versus intrude, what does the empty state teach, how are failures presented, and does the human stay the pilot?",
        "Orchestration": "The traffic control between user, data, tools, and model: prompt assembly, grounding, response filtering, plugin or tool execution. Teams must decide what context the model sees, what it may call, and what is allowed out. Trust is implemented here.",
        "Retrieval": "The RAG pipeline: chunking, search, ranking. Teams must decide chunk strategy, freshness, and provenance, because retrieval quality caps answer quality no matter how good the model is.",
        "Embeddings": "The semantic index under retrieval. Teams must decide which embedding model, at what dimension and cost, and remember embeddings from one provider cannot be read by another. Re-embedding a corpus is a migration, plan for it.",
        "Model": "Foundation models, hosted or your own, large or small. Teams must decide build versus buy, open versus closed, one model or a portfolio, and how to swap without rewriting the product.",
        "Safety": "Content filters, injection defenses, output handling. Teams must decide what gets blocked, logged, or escalated to humans, and treat model output as untrusted input to the rest of the system.",
        "Evaluation": "Offline benchmarks, LLM-as-judge methods, regression suites. Teams must decide what good means, measure it before and after every change, and budget for evals like they budget for tests.",
        "Infrastructure": "Compute, quotas, rate limits, latency budgets, token economics. Teams must decide capacity and cost ceilings, because pay-as-you-go pricing turns every feature decision into a unit-economics decision.",
    }
    stack_rows = []
    for name in ["Application", "Orchestration", "Retrieval", "Embeddings", "Model", "Safety", "Evaluation", "Infrastructure"]:
        selected = name == stack_layer.value
        style = (
            f"border:2px solid {GREEN}; background:{GREEN}18; font-weight:600;"
            if selected
            else "border:1px solid #d5dae2;"
        )
        stack_rows.append(
            f'<div style="padding:8px 14px; margin:4px 0; border-radius:8px; {style} font-family:ui-monospace,monospace; font-size:13px;">{name}</div>'
        )
    mo.hstack(
        [
            mo.Html('<div style="min-width:200px">' + "".join(stack_rows) + "</div>"),
            mo.md(f"**{stack_layer.value}** · what product teams need to think about:\n\n{stack_layers[stack_layer.value]}"),
        ],
        gap=2,
        align="start",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 4 · When should you fine-tune?

    Chapter 9 is careful about model adaptation: prompt first, ground with your
    data next, fine-tune last. Answer five questions and get the book-shaped
    recommendation.

    **What you learn:** fine-tuning is a style and behavior tool, not a knowledge
    tool. Knowledge that changes belongs in retrieval.
    """)
    return


@app.cell
def _(mo):
    q_domain = mo.ui.switch(label="Do you need deep domain behavior (jargon, conventions, task shapes)?")
    q_determinism = mo.ui.switch(label="Do you need highly deterministic, format-exact behavior?")
    q_current = mo.ui.switch(label="Do you need current, frequently changing information?")
    q_documents = mo.ui.switch(label="Do answers need to come from your company documents?")
    q_style = mo.ui.switch(label="Do you want a specific voice or writing style, consistently?")
    mo.vstack([q_domain, q_determinism, q_current, q_documents, q_style])
    return q_current, q_determinism, q_documents, q_domain, q_style


@app.cell
def _(mo, q_current, q_determinism, q_documents, q_domain, q_style):
    reasons = []
    if q_current.value or q_documents.value:
        recommendation = "RAG (retrieval-augmented generation)"
        reasons.append("Fresh or proprietary knowledge belongs in retrieval, where it can be updated and cited without retraining.")
        if q_style.value or q_domain.value:
            reasons.append("Layer fine-tuning on top later if voice or domain behavior still falls short: the two combine well.")
    elif q_style.value or q_domain.value:
        recommendation = "Fine-tuning"
        reasons.append("Consistent style and domain-shaped behavior are what adaptation is actually good at.")
        reasons.append("Budget for dataset curation and evaluation: the book treats data preparation as most of the work.")
    elif q_determinism.value:
        recommendation = "Prompting + configuration (and revisit model selection)"
        reasons.append("Determinism comes from low temperature, structured prompts, and schema-constrained outputs before it comes from training.")
        reasons.append("If a model cannot follow your format reliably, trying a different model is cheaper than tuning this one.")
    else:
        recommendation = "Prompting (start here)"
        reasons.append("No signal yet that you need anything heavier. Well-crafted prompts with a few examples are the cheapest experiment you can run.")

    mo.callout(
        mo.md("**Recommendation: " + recommendation + "**\n\n" + "\n".join("- " + reason for reason in reasons)),
        kind="success",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 5 · Responsible AI checklist

    Chapter 13 reads like a field guide to how these systems fail: hallucination,
    prompt injection, insecure output handling, overreliance. Check what your
    hypothetical product already has.

    **What you learn:** responsibility is operational. Every unchecked box is a
    failure mode from the book with your product's name on it.
    """)
    return


@app.cell
def _(mo):
    checklist = mo.ui.array(
        [
            mo.ui.checkbox(label="Human review for consequential outputs"),
            mo.ui.checkbox(label="Monitoring and alerting in production"),
            mo.ui.checkbox(label="Evaluation suite that runs on every change"),
            mo.ui.checkbox(label="Content filtering on inputs and outputs"),
            mo.ui.checkbox(label="Grounding with citations (RAG)"),
            mo.ui.checkbox(label="Prompt injection protection"),
            mo.ui.checkbox(label="Logging without storing sensitive data"),
        ],
        label="",
    )
    checklist
    return (checklist,)


@app.cell
def _(GREEN, checklist, mo):
    score = sum(1 for checked in checklist.value if checked)
    total = len(checklist.value)
    pct = round(100 * score / total)
    verdict = (
        "Ship-a-demo ready, not production ready." if pct < 45
        else "Respectable. Now pressure-test the unchecked rows." if pct < 90
        else "Production-serious. The book would still ask who reviews the reviewers."
    )
    bar = (
        f'<div style="background:#e7eaef;border-radius:99px;height:14px;max-width:420px">'
        f'<div style="background:{GREEN};width:{pct}%;height:14px;border-radius:99px"></div></div>'
    )
    mo.vstack(
        [
            mo.md(f"**Production readiness score: {pct}%** ({score}/{total})"),
            mo.Html(bar),
            mo.md(verdict),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## What book should I review next?

    The raffle gods chose this book. You get to choose the next one.
    """)
    return


@app.cell
def _(mo):
    poll = mo.ui.radio(
        options=[
            "AI Engineering",
            "Designing Machine Learning Systems",
            "Build",
            "Software Engineering at Google",
            "Building LLM Applications",
        ],
        label="cast your vote",
    )
    poll
    return (poll,)


@app.cell
def _(mo, poll):
    poll_reactions = {
        "AI Engineering": "Chip Huyen's newer one. Bold choice, very on-brand for this blog.",
        "Designing Machine Learning Systems": "A systems classic. The evals chapter of this review would like a word with it.",
        "Build": "Tony Fadell, for the product soul. The terminal aesthetic may need a hardware section.",
        "Software Engineering at Google": "Flamingo book! Testing culture at scale, my old stomping ground.",
        "Building LLM Applications": "Straight back into the stack. The orchestration layer appreciates your loyalty.",
    }
    poll_result = (
        mo.callout(mo.md(f"**Vote registered (locally, in your browser, with zero telemetry).** {poll_reactions[poll.value]}"), kind="success")
        if poll.value
        else mo.md("*Pick one. The poll is client-side only, this notebook phones nobody.*")
    )
    poll_result
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    *Built with [marimo](https://marimo.io). Won at PyData Boston 2025, thanks to
    Dawn Wages, Daina Bouquin, and Jessica Stefanowicz at the Anaconda booth, and
    to Amit Bahree for writing the book.*
    """)
    return


if __name__ == "__main__":
    app.run()
