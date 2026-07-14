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
"Generative AI in Action" by Amit Bahree (Manning, 2024).

Six teaching widgets plus a poll. No LLM calls anywhere:
every behavior is simulated so the notebook is reproducible,
runs in WASM, and costs nothing to explore.
"""

import marimo

__generated_with = "0.23.11"
app = marimo.App(width="medium", app_title="Generative AI in Action, interactively")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import altair as alt

    # Moss & pine palette, tuned to match rodrigosf.com.
    # Categorical order (validated for CVD separation and contrast on light):
    # moss -> violet -> amber -> rose.
    PINE = "#1e3d2f"
    MOSS = "#2e7d1f"
    LEAF = "#43B02A"
    SAGE = "#8aa87e"
    TINT = "#eef4ea"
    TINT_BORDER = "#cfdcc8"
    VIOLET = "#6841d8"
    VIOLET_TINT = "#f1edfb"
    AMBER = "#96610a"
    ROSE = "#c4386b"
    GRAY = "#9aa3b2"
    INK = "#22301f"
    INK_MUTED = "#51604b"
    MONO = "ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, monospace"
    return (
        AMBER, GRAY, INK, INK_MUTED, LEAF, MONO, MOSS, PINE, ROSE, SAGE,
        TINT, TINT_BORDER, VIOLET, VIOLET_TINT, alt, mo, np, pd,
    )


@app.cell
def _(INK_MUTED, MONO, MOSS, PINE, SAGE, TINT, TINT_BORDER, VIOLET, VIOLET_TINT, mo):
    def section_banner(num, title, subtitle):
        return mo.Html(
            f'<div style="background:linear-gradient(135deg,{PINE} 0%,{MOSS} 100%);'
            f'border-radius:14px;padding:18px 22px;margin:26px 0 10px;">'
            f'<div style="font-family:{MONO};color:#9fd48a;font-size:11.5px;'
            f'letter-spacing:0.12em;text-transform:uppercase;">{num}</div>'
            f'<div style="color:#f2f7ee;font-size:21px;font-weight:750;'
            f'line-height:1.25;margin-top:2px;">{title}</div>'
            f'<div style="color:#cfe3c4;font-size:14px;margin-top:6px;'
            f'line-height:1.5;">{subtitle}</div></div>'
        )

    def lens_cards(learn, tpmm):
        card = (
            'flex:1 1 260px;border-radius:10px;padding:12px 16px;'
            'font-size:13.5px;line-height:1.55;'
        )
        return mo.Html(
            f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin:2px 0 10px;">'
            f'<div style="{card}background:{TINT};border:1px solid {TINT_BORDER};">'
            f'<span style="font-family:{MONO};font-size:11px;letter-spacing:0.08em;'
            f'text-transform:uppercase;color:{MOSS};font-weight:700;">What you learn</span>'
            f'<div style="color:{INK_MUTED};margin-top:4px;">{learn}</div></div>'
            f'<div style="{card}background:{VIOLET_TINT};border:1px solid #ddd3f4;">'
            f'<span style="font-family:{MONO};font-size:11px;letter-spacing:0.08em;'
            f'text-transform:uppercase;color:{VIOLET};font-weight:700;">Product lens</span>'
            f'<div style="color:#4a4460;margin-top:4px;">{tpmm}</div></div></div>'
        )

    def stat_tile(label, value, note, color=MOSS):
        return (
            f'<div style="flex:1 1 150px;background:#ffffff;border:1px solid {TINT_BORDER};'
            f'border-top:3px solid {color};border-radius:10px;padding:12px 16px;">'
            f'<div style="font-family:{MONO};font-size:11px;letter-spacing:0.08em;'
            f'text-transform:uppercase;color:{INK_MUTED};">{label}</div>'
            f'<div style="font-family:{MONO};font-size:25px;font-weight:700;'
            f'color:{color};margin:2px 0;">{value}</div>'
            f'<div style="font-size:12px;color:{SAGE};line-height:1.4;">{note}</div></div>'
        )
    return lens_cards, section_banner, stat_tile


@app.cell
def _(MONO, PINE, mo):
    chip_style = (
        f'display:inline-block;font-family:{MONO};font-size:11.5px;'
        'padding:4px 12px;border-radius:99px;margin:3px 4px 0 0;'
        'background:rgba(255,255,255,0.14);color:#dff0d5;'
    )
    mo.Html(
        f'<div style="background:linear-gradient(150deg,#0f2419 0%,{PINE} 55%,#2e5d24 100%);'
        'border-radius:16px;padding:26px 28px;margin-bottom:6px;">'
        f'<div style="font-family:{MONO};color:#7ee787;font-size:12px;'
        'letter-spacing:0.14em;text-transform:uppercase;">rodrigosf.com · interactive book review</div>'
        '<div style="color:#f5faf1;font-size:29px;font-weight:800;line-height:1.2;'
        'margin:8px 0 6px;">Generative AI in Action, interactively</div>'
        '<div style="color:#cfe3c4;font-size:14.5px;line-height:1.6;max-width:38rem;">'
        'Six teaching widgets built for my review of '
        '<a href="https://www.manning.com/books/generative-ai-in-action" '
        'style="color:#9fd48a;font-weight:600;">Generative AI in Action</a>. '
        'Every behavior is simulated with plain NumPy, so the concepts stay honest, '
        'deterministic, and free to explore.</div>'
        f'<div style="margin-top:12px;"><span style="{chip_style}">100% simulated · zero API calls</span>'
        f'<span style="{chip_style}">Python running in your browser</span>'
        f'<span style="{chip_style}">reproducible by design</span></div>'
        f'<div style="font-family:{MONO};color:#8fa887;font-size:11.5px;margin-top:14px;">'
        'Bahree, A. (2024). <i>Generative AI in Action</i>. Manning Publications. '
        'ISBN 9781633436947.</div></div>'
    )
    return


@app.cell
def _(lens_cards, mo, section_banner):
    mo.vstack([
        section_banner(
            "section 01 · sampling & configuration",
            "Model Configuration Playground",
            "Chapter 3 (pp. 57-95) treats configuration as a first-class concept: "
            "temperature (section 3.2.4, p. 71), top_p (3.2.5, p. 74), and the presence "
            "and frequency penalties (3.3.3, p. 80) decide how much unpredictability you "
            "ship. Every control below visibly reshapes the simulated continuation.",
        ),
        lens_cards(
            "Configuration is a product surface. The same model becomes a different "
            "product when these numbers change.",
            "A support bot and a brainstorming tool can share a model and differ only "
            "in this panel. Ask which knobs your product exposes, and to whom.",
        ),
    ])
    return


@app.cell
def _(mo):
    temperature = mo.ui.slider(0.0, 2.0, step=0.1, value=0.7, label="temperature")
    top_p = mo.ui.slider(0.05, 1.0, step=0.05, value=1.0, label="top_p")
    presence_penalty = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.0, label="presence penalty")
    frequency_penalty = mo.ui.slider(-2.0, 2.0, step=0.1, value=0.0, label="frequency penalty")
    max_tokens = mo.ui.slider(16, 256, step=8, value=120, label="max tokens")
    fixed_seed = mo.ui.checkbox(value=False, label="fixed seed")
    regenerate = mo.ui.button(label="↻ regenerate", value=0, on_click=lambda v: v + 1)
    return (
        fixed_seed, frequency_penalty, max_tokens, presence_penalty,
        regenerate, temperature, top_p,
    )


@app.cell
def _(
    fixed_seed,
    frequency_penalty,
    max_tokens,
    np,
    presence_penalty,
    regenerate,
    temperature,
    top_p,
):
    # Hand-designed token pools (illustrative, not from a model). The words are
    # ordered sensible-to-strange, so temperature and top_p have legible effects.
    NOUN_POOL = [
        ("result", 0.34), ("pattern", 0.22), ("signal", 0.16), ("outcome", 0.12),
        ("smell", 0.07), ("melody", 0.05), ("universe", 0.03), ("apology", 0.01),
    ]
    LINK_POOL = [
        (", consistent with", 0.48), (", echoing", 0.22), (", defying", 0.16),
        (", serenading", 0.09), (", apologizing to", 0.05),
    ]
    REF_POOL = [
        ("the model's predictions", 0.42), ("last quarter's baseline", 0.28),
        ("the team's assumptions", 0.16), ("the intern's horoscope", 0.09),
        ("the office ficus", 0.05),
    ]
    VERB_POOL = [
        ("repeated the analysis", 0.40), ("checked the pipeline", 0.30),
        ("opened a ticket", 0.15), ("wrote a poem", 0.10), ("blamed the moon", 0.05),
    ]
    WHY_POOL = [
        ("to confirm the effect", 0.50), ("to rule out noise", 0.30),
        ("to appease the reviewers", 0.15), ("out of pure superstition", 0.05),
    ]
    DRIFT_POOL = [
        ("the product roadmap", 0.38), ("customer onboarding", 0.25),
        ("the pricing page", 0.17), ("an unrelated haiku", 0.12), ("lunch", 0.08),
    ]
    ADJ_POOL = [
        ("promising", 0.40), ("measurable", 0.30), ("inevitable", 0.15),
        ("luminous", 0.10), ("forgivable", 0.05),
    ]

    SIM_PROMPT = "The experiment produced a surprising"

    def simulate_generation(temp, nucleus, presence, frequency, max_toks, seed):
        rng = np.random.default_rng(seed)
        used_counts = {}

        greedy = temp <= 0.05  # temperature ~0 means greedy decoding: pure argmax

        def sample(pool):
            words = [w for w, _ in pool]
            weights = np.array([wt for _, wt in pool], dtype=float)
            for i, w in enumerate(words):
                # frequency penalty reweights words already used
                # (x2 so the effect is unmistakable at slider extremes)
                weights[i] *= float(np.exp(-2.0 * frequency * used_counts.get(w, 0)))
            if greedy:
                choice = words[int(np.argmax(weights))]
                used_counts[choice] = used_counts.get(choice, 0) + 1
                return choice
            weights = weights ** (1.0 / temp)
            weights = weights / weights.sum()
            order = np.argsort(weights)[::-1]
            cum = np.cumsum(weights[order])
            keep = order[: int(np.searchsorted(cum, min(nucleus, 0.999)) + 1)]
            kept_w = weights[keep] / weights[keep].sum()
            choice = words[int(rng.choice(keep, p=kept_w))]
            used_counts[choice] = used_counts.get(choice, 0) + 1
            return choice

        first_noun = sample(NOUN_POOL)
        text = f"{first_noun}{sample(LINK_POOL)} {sample(REF_POOL)}."
        second_noun = sample(NOUN_POOL)
        text += (
            f" A second {second_noun} appeared in the follow-up run, "
            f"so the team {sample(VERB_POOL)} {sample(WHY_POOL)}."
        )
        # presence penalty raises the odds of drifting to a brand-new topic;
        # the decision goes through temperature too, so temp ~0 stays deterministic
        p_drift = float(np.clip(0.10 + 0.45 * presence, 0.0, 1.0))
        drifted = p_drift > 0.5 if greedy else bool(rng.random() < p_drift)
        if drifted:
            text += (
                f" By Friday the discussion had drifted to {sample(DRIFT_POOL)}, "
                f"which everyone agreed was {sample(ADJ_POOL)}."
            )
        else:
            text += (
                f" The {sample(NOUN_POOL)} stayed stable across reruns, "
                f"and so did the {sample(NOUN_POOL)}."
            )

        words_out = text.split(" ")
        budget = max(int(max_toks / 1.3), 3)
        truncated = len(words_out) > budget
        if truncated:
            words_out = words_out[:budget]
        final_text = " ".join(words_out)
        token_estimate = round(len(words_out) * 1.3)
        return final_text, first_noun, drifted, truncated, token_estimate

    BASE_SEED = 20241029  # the book's publication date
    active_seed = BASE_SEED if fixed_seed.value else BASE_SEED + 7919 * regenerate.value
    sim_text, sim_first_noun, sim_drifted, sim_truncated, sim_tokens = simulate_generation(
        temperature.value,
        top_p.value,
        presence_penalty.value,
        frequency_penalty.value,
        max_tokens.value,
        active_seed,
    )
    return NOUN_POOL, SIM_PROMPT, active_seed, sim_drifted, sim_text, sim_tokens, sim_truncated


@app.cell
def _(
    AMBER,
    INK,
    INK_MUTED,
    MONO,
    MOSS,
    PINE,
    SAGE,
    SIM_PROMPT,
    TINT_BORDER,
    active_seed,
    fixed_seed,
    frequency_penalty,
    max_tokens,
    mo,
    presence_penalty,
    regenerate,
    sim_drifted,
    sim_text,
    sim_tokens,
    sim_truncated,
    temperature,
    top_p,
):
    meta_chip = (
        f'display:inline-block;font-family:{MONO};font-size:11px;'
        'padding:2px 10px;border-radius:99px;margin-right:6px;margin-top:8px;'
        f'background:#f1f5ee;color:{INK_MUTED};border:1px solid {TINT_BORDER};'
    )
    cut_marker = (
        f' <span style="color:{AMBER};font-weight:700;">⏹ [cut off: max_tokens reached]</span>'
        if sim_truncated else ""
    )
    drift_note = "drifted to a new topic" if sim_drifted else "stayed on topic"
    seed_note = f"seed {active_seed} ({'fixed' if fixed_seed.value else 'new on each ↻'})"

    sample_card = mo.Html(
        f'<div style="background:#fbfdf9;border:1.5px solid {TINT_BORDER};'
        f'border-left:5px solid {MOSS};border-radius:12px;padding:16px 18px;min-width:260px;">'
        f'<div style="font-family:{MONO};font-size:11px;letter-spacing:0.1em;'
        f'text-transform:uppercase;color:{SAGE};margin-bottom:8px;">'
        'simulated completion · no model was called</div>'
        f'<div style="font-family:{MONO};font-size:14px;line-height:1.75;color:{INK};">'
        f'<span style="color:{PINE};font-weight:700;">{SIM_PROMPT}</span> '
        f'{sim_text}{cut_marker}</div>'
        f'<div><span style="{meta_chip}">≈{sim_tokens} tokens</span>'
        f'<span style="{meta_chip}">{drift_note}</span>'
        f'<span style="{meta_chip}">{seed_note}</span></div></div>'
    )
    controls = mo.vstack(
        [
            temperature, top_p, presence_penalty, frequency_penalty, max_tokens,
            mo.hstack([fixed_seed, regenerate], justify="start", gap=1),
        ],
        gap=0.5,
    )
    mo.hstack([controls, sample_card], widths=[1, 1.5], gap=1.5, align="start", wrap=True)
    return


@app.cell
def _(mo):
    mo.md(
        """
    **Try these experiments.** Drop temperature to 0 and the text locks onto the most
    likely words (regenerating changes nothing). Raise it past 1.2 and the strange
    vocabulary surfaces. Push frequency penalty negative and watch the same noun
    repeat; push presence penalty up and the text abandons the experiment for the
    product roadmap. Drag max tokens down and the completion is chopped mid-sentence,
    which is exactly how a real truncation bug reads in production. Fix the seed and
    the regenerate button becomes honest: same settings, same output.
    """
    )
    return


@app.cell
def _(NOUN_POOL, np, pd, temperature, top_p):
    # First-slot distribution as the sampler sees it (temperature + top_p only).
    candidate_tokens = [w for w, _ in NOUN_POOL]
    base_probs = np.array([wt for _, wt in NOUN_POOL])
    T = max(temperature.value, 1e-3)
    scaled = np.exp(np.log(base_probs) / T)
    probs = scaled / scaled.sum()
    order = np.argsort(probs)[::-1]
    cumulative = np.cumsum(probs[order])
    keep_count = int(np.searchsorted(cumulative, top_p.value) + 1)
    kept_indices = set(order[:keep_count].tolist())
    dist_df = pd.DataFrame(
        {
            "token": candidate_tokens,
            "probability": probs,
            "status": [
                "sampled from" if i in kept_indices else "cut by top_p"
                for i in range(len(candidate_tokens))
            ],
        }
    )
    return (dist_df,)


@app.cell
def _(GRAY, INK_MUTED, MOSS, alt, dist_df, mo):
    config_chart = (
        alt.Chart(dist_df)
        .mark_bar(cornerRadiusEnd=4, height=15, stroke="#ffffff", strokeWidth=1)
        .encode(
            x=alt.X(
                "probability:Q",
                axis=alt.Axis(format="%", title="probability for the first blank", grid=True, gridOpacity=0.2),
            ),
            y=alt.Y("token:N", sort="-x", title=None),
            color=alt.Color(
                "status:N",
                scale=alt.Scale(domain=["sampled from", "cut by top_p"], range=[MOSS, GRAY]),
                legend=alt.Legend(title=None, orient="top"),
            ),
            tooltip=[
                alt.Tooltip("token:N"),
                alt.Tooltip("probability:Q", format=".1%"),
                alt.Tooltip("status:N"),
            ],
        )
        .properties(
            width=540,
            height=220,
            title=alt.Title(
                "What the sampler actually sees",
                subtitle="temperature reshapes the distribution; top_p cuts the tail (penalties act later, on reuse)",
                fontSize=14,
                subtitleColor=INK_MUTED,
                subtitleFontSize=11.5,
            ),
        )
        .configure_view(strokeOpacity=0)
        .configure_axis(labelColor=INK_MUTED, titleColor=INK_MUTED)
    )
    mo.vstack([config_chart, mo.md(
        "*Book tip worth engraving somewhere: adjust temperature **or** top_p, "
        "not both (the book says it twice, pp. 49 and 75).*"
    )])
    return


@app.cell
def _(lens_cards, mo, section_banner):
    mo.vstack([
        section_banner(
            "section 02 · prompt engineering",
            "Prompt Pattern Explorer",
            "Chapter 6 (pp. 155-182) catalogs the prompt patterns everyone eventually "
            "rediscovers. Switch between them to compare the prompt itself and the "
            "behavior you should expect.",
        ),
        lens_cards(
            "Patterns are not magic phrasing. Each one trades effort, tokens, and "
            "control differently.",
            "Prompt choices are cost and reliability choices. Few-shot examples are "
            "paid for on every request; a system prompt is where product identity lives.",
        ),
    ])
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
def _(INK, MONO, PINE, SAGE, TINT_BORDER, mo, prompt_pattern):
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
            "In-context examples anchor both the labels and the output format. Costs more tokens, buys consistency. The book frames this as in-context learning (pp. 161-162): the model imitates the pattern you show it.",
        ),
        "Chain of Thought": (
            "Classify the sentiment. Think step by step: first list the positive claims, "
            "then the negative claims, then weigh them before answering.\n\n"
            '"The install was painless but the docs assume telepathy."',
            "Asking for intermediate reasoning improves multi-step tasks (p. 170). Slower and more verbose, and the reasoning text itself is for the model's benefit, not necessarily a faithful account. Use for logic, not for lookups.",
        ),
        "System prompt": (
            "System: You are a support triage assistant. Always answer with exactly one word: "
            "positive, negative, or mixed. Never explain.\n\n"
            'User: "The install was painless but the docs assume telepathy."',
            "The system role sets persistent rules the user message cannot easily see or edit (p. 163). This is where products encode identity, tone, and boundaries. Most guardrails start here; prompt injection (section 6.6, p. 176) is the attack that tests them.",
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
            mo.Html(
                f'<div style="background:#fbfdf9;border:1.5px solid {TINT_BORDER};'
                f'border-left:5px solid {PINE};border-radius:12px;padding:14px 18px;">'
                f'<div style="font-family:{MONO};font-size:11px;letter-spacing:0.1em;'
                f'text-transform:uppercase;color:{SAGE};margin-bottom:8px;">the prompt</div>'
                f'<pre style="font-family:{MONO};font-size:13px;line-height:1.6;color:{INK};'
                f'white-space:pre-wrap;margin:0;">{prompt_text}</pre></div>'
            ),
            mo.md(f"**What changes:** {prompt_diff}"),
        ]
    )
    return


@app.cell
def _(lens_cards, mo, section_banner):
    mo.vstack([
        section_banner(
            "section 03 · architecture",
            "LLM Product Stack Explorer",
            "Chapter 10 (pp. 283-320) maps a GenAI application stack (pp. 286-292) and "
            "compares it to LAMP itself (p. 286). The eight layers here are adapted and "
            "expanded from the book's four-layer stack (figure 10.2, p. 287), breaking "
            "retrieval, embeddings, safety, and evaluation out into their own rows. "
            "The model is two layers from the bottom, which is exactly the point.",
        ),
        lens_cards(
            "Most product risk lives in the middle of the stack, not in the model. "
            "The orchestration layer is where trust is implemented.",
            "Layer ownership is a strategy question: which layers does your product "
            "own, which does it buy, and which does it merely observe?",
        ),
    ])
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
def _(MONO, MOSS, TINT_BORDER, mo, stack_layer):
    stack_layers = {
        "Application": "The copilot or product the user touches (the era of copilots and the book's airplane analogy, pp. 285-286). Teams must decide: where does AI help versus intrude, what does the empty state teach, how are failures presented, and does the human stay the pilot?",
        "Orchestration": "The traffic control between user, data, tools, and model: prompt assembly, grounding, response filtering, plugin or tool execution (section 10.3, pp. 293-307). Teams must decide what context the model sees, what it may call, and what is allowed out. Trust is implemented here.",
        "Retrieval": "The RAG pipeline: chunking, search, ranking (chunking gets pp. 195-212). Teams must decide chunk strategy, freshness, and provenance, because retrieval quality caps answer quality no matter how good the model is.",
        "Embeddings": "The semantic index under retrieval (embeddings and vector management, pp. 310-311). Teams must decide which embedding model, at what dimension and cost, and remember embeddings from one provider cannot be read by another. Re-embedding a corpus is a migration, plan for it.",
        "Model": "Foundation models, hosted or your own, large or small (model layer and ensembles, pp. 312-318). Teams must decide build versus buy, open versus closed, one model or a portfolio, and how to swap without rewriting the product.",
        "Safety": "Content filters, injection defenses, output handling (response filtering, pp. 318-320; content safety, pp. 411-421). Teams must decide what gets blocked, logged, or escalated to humans, and treat model output as untrusted input to the rest of the system.",
        "Evaluation": "Offline benchmarks, LLM-as-judge methods, regression suites (ch. 12, pp. 357-383). Teams must decide what good means, measure it before and after every change, and budget for evals like they budget for tests.",
        "Infrastructure": "Compute, quotas, rate limits, latency budgets, token economics (ch. 11, pp. 321-356). Teams must decide capacity and cost ceilings, because pay-as-you-go pricing turns every feature decision into a unit-economics decision.",
    }
    stack_rows = [
        (
            f'<div style="padding:8px 14px;margin:4px 0;border-radius:8px;'
            + (
                f'border:2px solid {MOSS};background:{MOSS}1c;font-weight:650;'
                if layer_name == stack_layer.value
                else f'border:1px solid {TINT_BORDER};'
            )
            + f'font-family:{MONO};font-size:13px;">{layer_name}</div>'
        )
        for layer_name in stack_layers
    ]
    mo.hstack(
        [
            mo.Html('<div style="min-width:200px">' + "".join(stack_rows) + "</div>"),
            mo.md(
                f"**{stack_layer.value}** · what product teams need to think about:\n\n"
                f"{stack_layers[stack_layer.value]}"
            ),
        ],
        gap=2,
        align="start",
    )
    return


@app.cell
def _(lens_cards, mo, section_banner):
    mo.vstack([
        section_banner(
            "section 04 · enterprise adoption",
            "Token Economics Calculator",
            "Chapter 11 (pp. 321-356) keeps returning to a blunt truth: "
            "pay-as-you-go pricing (PAYGO, p. 333) turns every AI feature into a "
            "unit-economics decision. Model a rollout, from pilot to enterprise, "
            "and watch the monthly bill move.",
        ),
        lens_cards(
            "Latency budgets, quotas, rate limits, and token prices decide whether an "
            "AI feature is still a good idea when the invoice arrives. Caching is a product decision.",
            "This is the product conversation: cost per user versus what the seat sells "
            "for, and which levers (context size, caching, model tier) protect margin.",
        ),
    ])
    return


@app.cell
def _(mo):
    rollout_stage = mo.ui.radio(
        options=["Pilot (50 users)", "Department (500 users)", "Organization (5,000 users)", "Enterprise (25,000 users)"],
        value="Department (500 users)",
        label="rollout stage",
    )
    requests_per_day = mo.ui.slider(1, 100, step=1, value=20, label="requests per user per workday")
    tokens_in = mo.ui.slider(200, 8000, step=100, value=1500, label="avg input tokens per request (prompt + retrieved context)")
    tokens_out = mo.ui.slider(50, 4000, step=50, value=400, label="avg output tokens per request")
    price_in = mo.ui.slider(0.1, 15.0, step=0.1, value=3.0, label="price per 1M input tokens ($)")
    price_out = mo.ui.slider(0.5, 75.0, step=0.5, value=15.0, label="price per 1M output tokens ($)")
    cache_rate = mo.ui.slider(0, 90, step=5, value=30, label="prompt cache hit rate (%)")
    seat_price = mo.ui.slider(5, 100, step=5, value=30, label="what the AI seat sells for ($/user/month)")

    mo.vstack(
        [
            rollout_stage,
            mo.hstack([requests_per_day, cache_rate], justify="start", gap=2, wrap=True),
            mo.hstack([tokens_in, tokens_out], justify="start", gap=2, wrap=True),
            mo.hstack([price_in, price_out], justify="start", gap=2, wrap=True),
            seat_price,
        ],
        gap=0.5,
    )
    return (
        cache_rate, price_in, price_out, requests_per_day,
        rollout_stage, seat_price, tokens_in, tokens_out,
    )


@app.cell
def _(
    cache_rate,
    pd,
    price_in,
    price_out,
    requests_per_day,
    rollout_stage,
    seat_price,
    tokens_in,
    tokens_out,
):
    stage_users = {
        "Pilot (50 users)": 50,
        "Department (500 users)": 500,
        "Organization (5,000 users)": 5000,
        "Enterprise (25,000 users)": 25000,
    }
    n_users = stage_users[rollout_stage.value]
    monthly_requests = n_users * requests_per_day.value * 21  # workdays
    m_tokens_in = monthly_requests * tokens_in.value / 1e6
    m_tokens_out = monthly_requests * tokens_out.value / 1e6

    cache_frac = cache_rate.value / 100
    # cached input tokens billed at 10% of list price (a common discount shape)
    input_cost_nocache = m_tokens_in * price_in.value
    input_cost_cache = m_tokens_in * price_in.value * (1 - cache_frac + 0.1 * cache_frac)
    output_cost = m_tokens_out * price_out.value

    total_nocache = input_cost_nocache + output_cost
    total_cache = input_cost_cache + output_cost
    cost_per_user = total_cache / n_users
    margin_per_user = seat_price.value - cost_per_user
    peak_rps = n_users * requests_per_day.value / (8 * 3600)

    cost_df = pd.DataFrame(
        [
            {"scenario": "without caching", "component": "input tokens", "cost": input_cost_nocache},
            {"scenario": "without caching", "component": "output tokens", "cost": output_cost},
            {"scenario": f"with {cache_rate.value}% cache hits", "component": "input tokens", "cost": input_cost_cache},
            {"scenario": f"with {cache_rate.value}% cache hits", "component": "output tokens", "cost": output_cost},
        ]
    )
    return cost_df, cost_per_user, margin_per_user, n_users, peak_rps, total_cache, total_nocache


@app.cell
def _(
    AMBER,
    MOSS,
    ROSE,
    cost_per_user,
    margin_per_user,
    mo,
    n_users,
    peak_rps,
    seat_price,
    stat_tile,
    total_cache,
    total_nocache,
):
    def money(x):
        return f"${x:,.0f}" if x >= 100 else f"${x:,.2f}"

    margin_color = MOSS if margin_per_user > 0 else ROSE
    savings = total_nocache - total_cache
    mo.vstack([
        mo.Html(
            '<div style="display:flex;gap:10px;flex-wrap:wrap;margin:6px 0;">'
            + stat_tile("monthly model bill", money(total_cache), f"{n_users:,} users · caching applied")
            + stat_tile("cost per user / month", money(cost_per_user), f"seat sells for ${seat_price.value}/month")
            + stat_tile(
                "margin per seat",
                money(abs(margin_per_user)) + ("" if margin_per_user >= 0 else " under"),
                "unit economics " + ("hold" if margin_per_user >= 0 else "are underwater"),
                color=margin_color,
            )
            + stat_tile("caching saves", money(savings), "per month vs no cache", color=AMBER)
            + stat_tile("peak load", f"{peak_rps:.1f} rps", "mind quotas and rate limits", color=AMBER)
            + "</div>"
        ),
        mo.md(
            "*Assumptions you can argue with: 21 workdays per month, peak load spread "
            "over an 8-hour day, and cached input tokens billed at 10% of list price. "
            "That last one varies by provider (some discount 50%, some 90%), so treat "
            "the caching tile as a shape, not a quote.*"
        ),
    ])
    return


@app.cell
def _(INK_MUTED, MOSS, VIOLET, alt, cost_df, mo):
    cost_chart = (
        alt.Chart(cost_df)
        .mark_bar(cornerRadiusEnd=4, height=26, stroke="#ffffff", strokeWidth=2)
        .encode(
            x=alt.X("cost:Q", axis=alt.Axis(format="$,.0f", title="monthly cost", grid=True, gridOpacity=0.2)),
            y=alt.Y("scenario:N", title=None, sort=None),
            color=alt.Color(
                "component:N",
                scale=alt.Scale(domain=["input tokens", "output tokens"], range=[MOSS, VIOLET]),
                legend=alt.Legend(title=None, orient="top"),
            ),
            order=alt.Order("component:N"),
            tooltip=[
                alt.Tooltip("scenario:N"),
                alt.Tooltip("component:N"),
                alt.Tooltip("cost:Q", format="$,.0f"),
            ],
        )
        .properties(
            width=540,
            height=110,
            title=alt.Title(
                "Where the money goes",
                subtitle="input is volume, output is price: long contexts and long answers are different problems",
                fontSize=14,
                subtitleColor=INK_MUTED,
                subtitleFontSize=11.5,
            ),
        )
        .configure_view(strokeOpacity=0)
        .configure_axis(labelColor=INK_MUTED, titleColor=INK_MUTED)
    )
    cost_chart
    return


@app.cell
def _(mo):
    mo.md(
        """
    **What the book would have you check before scaling a stage.** Quotas and rate
    limits at peak load, not average (pp. 333-336). Time to first token, because
    perceived speed is a retention feature (table 11.3, p. 327). Caching, which the
    book treats as an architecture decision, complete with Redis key design advice
    (pp. 349-352). An evaluation gate between each rollout stage, so quality
    regressions are caught at 500 users instead of 25,000 (ch. 12, pp. 357-383;
    DeepEval on p. 377). And a fallback model strategy, because in an enterprise
    rollout the model is a dependency like any other. Chapter 11 closes with a
    production deployment checklist (pp. 354-356); every line of it decides
    whether the pilot survives procurement.
    """
    )
    return


@app.cell
def _(lens_cards, mo, section_banner):
    mo.vstack([
        section_banner(
            "section 05 · model adaptation",
            "When should you fine-tune?",
            "Chapter 9 (pp. 242-282) is careful about model adaptation: prompt first, "
            "ground with your data next, fine-tune last (When to fine-tune an LLM, "
            "pp. 247-248; the chapter summary calls the combination working in a "
            "stacked manner, p. 280). Answer five questions and get the book-shaped recommendation.",
        ),
        lens_cards(
            "Fine-tuning is a style and behavior tool, not a knowledge tool. "
            "Knowledge that changes belongs in retrieval.",
            "Adaptation is a resource-allocation argument: the cheapest experiment "
            "that could work goes first. Treat fine-tuning like a feature with a budget.",
        ),
    ])
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
def _(MOSS, TINT, TINT_BORDER, mo, q_current, q_determinism, q_documents, q_domain, q_style):
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

    reason_items = "".join(f'<li style="margin:4px 0;">{r}</li>' for r in reasons)
    mo.Html(
        f'<div style="background:{TINT};border:1.5px solid {TINT_BORDER};'
        f'border-left:5px solid {MOSS};border-radius:12px;padding:14px 18px;">'
        f'<div style="font-weight:750;color:{MOSS};font-size:15.5px;">'
        f'Recommendation: {recommendation}</div>'
        f'<ul style="margin:8px 0 0;padding-left:20px;font-size:14px;line-height:1.55;">'
        f'{reason_items}</ul></div>'
    )
    return


@app.cell
def _(lens_cards, mo, section_banner):
    mo.vstack([
        section_banner(
            "section 06 · responsible ai",
            "Responsible AI Checklist",
            "Chapter 13 (pp. 384-422) reads like a field guide to how these systems "
            "fail: hallucination (p. 387), prompt injection (p. 389), insecure output "
            "handling (p. 394), overreliance (p. 397), plus a responsible AI lifecycle "
            "(pp. 399-405) and red-teaming (pp. 406-410). Check what your hypothetical product already has.",
        ),
        lens_cards(
            "Responsibility is operational. Every unchecked box is a failure mode "
            "from the book with your product's name on it.",
            "In enterprise deals this list is the security questionnaire. Products "
            "that can answer it up front close faster.",
        ),
    ])
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
def _(LEAF, MONO, MOSS, checklist, mo):
    score = sum(1 for checked in checklist.value if checked)
    total = len(checklist.value)
    pct = round(100 * score / total)
    verdict = (
        "Ship-a-demo ready, not production ready." if pct < 45
        else "Respectable. Now pressure-test the unchecked rows." if pct < 90
        else "Production-serious. The book would still ask who reviews the reviewers."
    )
    bar = (
        '<div style="background:#e7ece3;border-radius:99px;height:16px;max-width:420px">'
        f'<div style="background:linear-gradient(90deg,{MOSS},{LEAF});width:{pct}%;'
        'height:16px;border-radius:99px;transition:width 0.2s"></div></div>'
    )
    mo.vstack(
        [
            mo.Html(
                f'<div style="font-family:{MONO};font-weight:700;font-size:15px;">'
                f'Production readiness: <span style="color:{MOSS}">{pct}%</span> ({score}/{total})</div>'
            ),
            mo.Html(bar),
            mo.md(verdict),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    **Reference.** Bahree, A. (2024). *Generative AI in Action*. Manning Publications.
    464 pp. ISBN 9781633436947. [manning.com/books/generative-ai-in-action](https://www.manning.com/books/generative-ai-in-action)
    · [companion code repo](https://github.com/bahree/GenAIBook) (documented in the book's own appendix A, p. 423)

    *Built with [marimo](https://marimo.io). The copy reviewed here was won at
    PyData Boston 2025, thanks to Dawn Wages, Daina Bouquin, and Jessica Stefanowicz
    at the Anaconda booth, and to Amit Bahree for writing the book. Read the full
    review at [rodrigosf.com](https://rodrigosf.com/blog/generative-ai-in-action-review.html).*
    """)
    return


if __name__ == "__main__":
    app.run()
