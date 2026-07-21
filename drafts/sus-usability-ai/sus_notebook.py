# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "altair>=5.0.0",
#     "pandas>=2.0.0",
#     "numpy>=1.26.0",
# ]
# ///

"""Interactive companion to the blog post on the System Usability Scale (SUS)
and why it remains relevant in the era of AI products.

Answer ten questions, watch the score move next to your hand, then simulate
what trust, learnability, and complexity do to an AI product. Runs entirely
in the browser; no model calls, no telemetry.
"""

import marimo

__generated_with = "0.23.11"
app = marimo.App(width="medium", app_title="The System Usability Scale, interactively")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import altair as alt

    # Moss & pine palette, shared with rodrigosf.com and the first post's notebook.
    PINE = "#1e3d2f"
    MOSS = "#2e7d1f"
    SAGE = "#8aa87e"
    TINT = "#eef4ea"
    TINT_BORDER = "#cfdcc8"
    VIOLET = "#6841d8"
    AMBER = "#96610a"
    ROSE = "#c4386b"
    GRAY = "#9aa3b2"
    INK = "#22301f"
    INK_MUTED = "#51604b"
    MONO = "ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, monospace"
    return (
        AMBER, GRAY, INK, INK_MUTED, MONO, MOSS, PINE, ROSE, SAGE,
        TINT, TINT_BORDER, VIOLET, alt, mo, np, pd,
    )


@app.cell
def _(INK_MUTED, MONO, MOSS, PINE, SAGE, TINT_BORDER, mo):
    def section_banner(num, title, subtitle):
        return mo.Html(
            f'<div style="background:linear-gradient(135deg,{PINE} 0%,{MOSS} 100%);'
            f'border-radius:14px;padding:16px 20px;margin:24px 0 10px;">'
            f'<div style="font-family:{MONO};color:#9fd48a;font-size:11.5px;'
            f'letter-spacing:0.12em;text-transform:uppercase;">{num}</div>'
            f'<div style="color:#f2f7ee;font-size:20px;font-weight:750;'
            f'line-height:1.25;margin-top:2px;">{title}</div>'
            f'<div style="color:#cfe3c4;font-size:13.5px;margin-top:5px;'
            f'line-height:1.5;">{subtitle}</div></div>'
        )

    def stat_tile(label, value, note, color=MOSS):
        return (
            f'<div style="flex:1 1 130px;background:#ffffff;border:1px solid {TINT_BORDER};'
            f'border-top:3px solid {color};border-radius:10px;padding:10px 14px;">'
            f'<div style="font-family:{MONO};font-size:10.5px;letter-spacing:0.08em;'
            f'text-transform:uppercase;color:{INK_MUTED};">{label}</div>'
            f'<div style="font-family:{MONO};font-size:24px;font-weight:700;'
            f'color:{color};margin:2px 0;">{value}</div>'
            f'<div style="font-size:11.5px;color:{SAGE};line-height:1.35;">{note}</div></div>'
        )
    return section_banner, stat_tile


@app.cell
def _(MONO, PINE, mo):
    hero_chip = (
        f'display:inline-block;font-family:{MONO};font-size:11.5px;'
        'padding:4px 12px;border-radius:99px;margin:3px 4px 0 0;'
        'background:rgba(255,255,255,0.14);color:#dff0d5;'
    )
    mo.Html(
        f'<div style="background:linear-gradient(150deg,#0f2419 0%,{PINE} 55%,#2e5d24 100%);'
        'border-radius:16px;padding:24px 28px;margin-bottom:6px;">'
        f'<div style="font-family:{MONO};color:#7ee787;font-size:12px;'
        'letter-spacing:0.14em;text-transform:uppercase;">rodrigosf.com · interactive companion</div>'
        '<div style="color:#f5faf1;font-size:28px;font-weight:800;line-height:1.2;'
        'margin:8px 0 6px;">The System Usability Scale, interactively</div>'
        '<div style="color:#cfe3c4;font-size:14.5px;line-height:1.6;max-width:38rem;">'
        'Ten questions, one score, three minutes. A survey from 1986 that still '
        'decides whether AI products get adopted.</div>'
        '<div style="color:#9fd48a;font-size:13.5px;line-height:1.6;max-width:38rem;'
        'margin-top:10px;font-style:italic;">"Technical capability alone does not create '
        'adoption. Users adopt products when they understand them, trust them, and can '
        'confidently accomplish their goals."</div>'
        f'<div style="margin-top:12px;"><span style="{hero_chip}">100% local · zero API calls</span>'
        f'<span style="{hero_chip}">Python running in your browser</span></div></div>'
    )
    return


@app.cell
def _(INK, INK_MUTED, MONO, MOSS, TINT_BORDER, mo, section_banner):
    def _pill(text, hl=False):
        style = (
            "display:inline-block;padding:4px 11px;border-radius:7px;font-size:12.5px;"
            + (f"border:1.5px solid {MOSS};background:{MOSS}1c;font-weight:650;color:{INK};"
               if hl else f"border:1px solid {TINT_BORDER};background:#fbfdf9;color:{INK};")
        )
        return f'<span style="{style}">{text}</span>'

    _arrow = f'<span style="color:{MOSS};margin:0 5px;font-weight:700;">&rarr;</span>'
    _label = (
        'display:inline-block;min-width:104px;font-family:' + MONO
        + f';font-size:10.5px;letter-spacing:1px;color:{INK_MUTED};'
    )
    _loops = mo.Html(
        '<div style="display:flex;flex-direction:column;gap:10px;margin:2px 0 4px;">'
        f'<div style="display:flex;align-items:center;flex-wrap:wrap;gap:4px;">'
        f'<span style="{_label}">TRADITIONAL</span>'
        f'{_pill("User action")}{_arrow}{_pill("System response")}</div>'
        f'<div style="display:flex;align-items:center;flex-wrap:wrap;gap:4px;">'
        f'<span style="{_label}">AI PRODUCTS</span>'
        f'{_pill("User intention")}{_arrow}{_pill("AI interpretation")}{_arrow}'
        f'{_pill("Probabilistic output")}{_arrow}{_pill("Human evaluation", hl=True)}</div>'
        f'<div style="font-size:12.5px;color:{INK_MUTED};line-height:1.5;">Every step AI '
        'adds is a usability question benchmarks never see, and the last one, human '
        'evaluation, is quietly handed to the user.</div></div>'
    )

    mo.vstack([
        section_banner(
            "01 · sus in one minute",
            "A benchmark measures the model. SUS measures whether people will use it.",
            "The System Usability Scale (John Brooke, 1986) asks users to rate ten "
            "statements from strongly disagree to strongly agree, then folds the "
            "answers into a single 0-100 score. Simple, fast, technology-independent, "
            "and statistically reliable, which is why it has scored everything from "
            "websites to medical devices for four decades.",
        ),
        _loops,
        mo.accordion(
            {
                "More background & references": mo.md(
                    r"""
    SUS was created at Digital Equipment Corporation because teams needed usability
    measurement fast enough to actually get used: no lab, no specialist. It has
    scored software, websites, medical devices, scientific equipment, and healthcare
    systems, where usability is not cosmetic: it affects **workflow efficiency**,
    **error rates**, **reproducibility**, and **user confidence**. With AI products,
    users must additionally judge correctness, confidence, trust, transparency, and
    recovery from mistakes, which makes the instrument more relevant, not less.

    - Brooke, J. (1996). SUS: A "Quick and Dirty" Usability Scale. In *Usability
      Evaluation in Industry*. Taylor & Francis.
    - Kortum, P., & Peres, S. C. (2015). Evaluation of Home Health Care Devices:
      Remote Usability Assessment. *JMIR Human Factors*, 2(1), e10.
      [humanfactors.jmir.org/2015/1/e10](https://humanfactors.jmir.org/2015/1/e10/)
    """
                )
            }
        ),
    ])
    return


@app.cell
def _(mo, section_banner):
    section_banner(
        "02 · take it yourself",
        "Ten questions, score updates as you click",
        "Rate a system you actually use: an AI assistant, a developer tool, a data "
        "science IDE. 1 = strongly disagree · 5 = strongly agree. Your score and "
        "grade update live in the panel beside the questions.",
    )
    return


@app.cell
def _(mo):
    SUS_QUESTIONS = [
        "I think that I would like to use this system frequently.",
        "I found the system unnecessarily complex.",
        "I thought the system was easy to use.",
        "I think that I would need the support of a technical person to be able to use this system.",
        "I found the various functions in this system were well integrated.",
        "I thought there was too much inconsistency in this system.",
        "I would imagine that most people would learn to use this system very quickly.",
        "I found the system very cumbersome to use.",
        "I felt very confident using this system.",
        "I needed to learn a lot of things before I could get going with this system.",
    ]
    LIKERT = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}

    # mo.ui.array registers the ten radios for reactivity; .elements lets the
    # layout cell place them row by row while values still flow to q_array.value
    q_array = mo.ui.array(
        [mo.ui.radio(options=list(LIKERT), value="3", inline=True) for _ in SUS_QUESTIONS]
    )
    return LIKERT, SUS_QUESTIONS, q_array


@app.cell
def _(LIKERT, q_array):
    # The SUS arithmetic, exactly as Brooke defined it:
    # odd questions (positively worded): contribution = response - 1
    # even questions (negatively worded): contribution = 5 - response
    # SUS = (sum of contributions) * 2.5
    responses = [LIKERT[v] for v in q_array.value]

    def sus_contributions(resp):
        return [r - 1 if i % 2 == 0 else 5 - r for i, r in enumerate(resp)]

    def sus_score(resp):
        return sum(sus_contributions(resp)) * 2.5

    def sus_grade(score):
        if score >= 90: return "A+", "Exceptional"
        if score >= 85: return "A", "Excellent"
        if score >= 80: return "A-", "Very Good"
        if score >= 73: return "B", "Good"
        if score >= 68: return "C", "Average"
        if score >= 51: return "D", "Poor"
        return "F", "Unacceptable"

    contributions = sus_contributions(responses)
    raw_score = sum(contributions)
    final_score = raw_score * 2.5
    your_grade, your_verdict = sus_grade(final_score)
    return (
        contributions, final_score, raw_score, responses,
        sus_grade, sus_score, your_grade, your_verdict,
    )


@app.cell
def _(INK_MUTED, ROSE, alt, final_score, pd):
    GRADE_BANDS = pd.DataFrame(
        [
            {"grade": "F", "lo": 0, "hi": 51, "label": "Unacceptable", "shade": "#dfe7da"},
            {"grade": "D", "lo": 51, "hi": 68, "label": "Poor", "shade": "#c9dbbd"},
            {"grade": "C", "lo": 68, "hi": 73, "label": "Average", "shade": "#a9c896"},
            {"grade": "B", "lo": 73, "hi": 80, "label": "Good", "shade": "#7fae64"},
            {"grade": "A-", "lo": 80, "hi": 85, "label": "Very Good", "shade": "#579339"},
            {"grade": "A", "lo": 85, "hi": 90, "label": "Excellent", "shade": "#3b7a26"},
            {"grade": "A+", "lo": 90, "hi": 100, "label": "Exceptional", "shade": "#245a17"},
        ]
    )
    score_marker_df = pd.DataFrame([{"score": final_score, "name": "Your SUS score"}])

    def grade_scale_chart(width=300, height=56):
        bands = alt.Chart(GRADE_BANDS).mark_bar(height=26, stroke="#ffffff", strokeWidth=2).encode(
            x=alt.X("lo:Q", title=None, scale=alt.Scale(domain=[0, 100]),
                    axis=alt.Axis(values=[0, 51, 68, 80, 90, 100], labelFontSize=10)),
            x2="hi:Q",
            color=alt.Color("shade:N", scale=None),
            tooltip=[alt.Tooltip("grade:N"), alt.Tooltip("label:N"),
                     alt.Tooltip("lo:Q", title="from"), alt.Tooltip("hi:Q", title="to")],
        )
        band_labels = alt.Chart(GRADE_BANDS).mark_text(dy=-24, fontSize=10, color=INK_MUTED).encode(
            x=alt.X("mid:Q", scale=alt.Scale(domain=[0, 100])), text="grade:N",
        ).transform_calculate(mid="(datum.lo + datum.hi) / 2")
        marker = alt.Chart(score_marker_df).mark_point(
            shape="triangle-down", size=140, color=ROSE, filled=True, yOffset=-22,
        ).encode(
            x=alt.X("score:Q", scale=alt.Scale(domain=[0, 100])),
            tooltip=[alt.Tooltip("name:N"), alt.Tooltip("score:Q", format=".1f")],
        )
        rule = alt.Chart(score_marker_df).mark_rule(color=ROSE, strokeWidth=2).encode(x="score:Q")
        return (
            alt.layer(bands, band_labels, rule, marker)
            .properties(width=width, height=height)
            .configure_view(strokeOpacity=0)
            .configure_axis(labelColor=INK_MUTED, grid=False)
        )
    return (grade_scale_chart,)


@app.cell
def _(
    INK,
    MONO,
    SAGE,
    SUS_QUESTIONS,
    final_score,
    grade_scale_chart,
    mo,
    q_array,
    stat_tile,
    your_grade,
    your_verdict,
):
    question_rows = [
        mo.hstack(
            [
                mo.Html(
                    f'<div style="min-width:230px;max-width:390px;font-size:13.5px;'
                    f'line-height:1.4;color:{INK};">'
                    f'<span style="font-family:{MONO};font-weight:700;color:{SAGE};">'
                    f'Q{qi}</span> {qtext}</div>'
                ),
                qw,
            ],
            gap=1,
            align="center",
            wrap=True,
        )
        for qi, (qtext, qw) in enumerate(zip(SUS_QUESTIONS, q_array.elements), start=1)
    ]
    live_panel = mo.vstack(
        [
            mo.Html(
                '<div style="display:flex;gap:8px;flex-wrap:wrap;">'
                + stat_tile("your SUS score", f"{final_score:.1f}", "out of 100")
                + stat_tile("grade", your_grade, your_verdict)
                + "</div>"
            ),
            grade_scale_chart(width=290, height=52),
            mo.md(f"*{final_score - 68:+.1f} points vs the industry average of 68.*"),
        ],
        gap=0.6,
    )
    mo.hstack([mo.vstack(question_rows, gap=0.45), live_panel],
              widths=[1.6, 1], gap=1.5, align="start", wrap=True)
    return


@app.cell
def _(
    GRAY,
    INK_MUTED,
    MOSS,
    VIOLET,
    alt,
    contributions,
    final_score,
    mo,
    pd,
    raw_score,
):
    # -- tab 1: the formula --
    formula_tab = mo.md(
        r"""
    $$
    \textbf{SUS} \;=\; 2.5 \times \sum_{i=1}^{10} c_i
    \qquad\text{where}\qquad
    c_i =
    \begin{cases}
    r_i - 1 & i \text{ odd (positively worded)}\\[2pt]
    5 - r_i & i \text{ even (negatively worded)}
    \end{cases}
    $$
    """
        + f"\n**Your answers:** raw score {raw_score} / 40 · × 2.5 · **SUS = {final_score:.1f} / 100**"
    )

    # -- tab 2: favorability chart + dimensions --
    # Favorability = the answer mapped so 5 is always the best possible answer,
    # matching the 1-5 scale readers just clicked (internally, SUS scores it 0-4).
    contrib_df = pd.DataFrame(
        {
            "question": [f"Q{i + 1}" for i in range(10)],
            "favorability": [c + 1 for c in contributions],
            "sus_points": contributions,
            "lost": [4 - c for c in contributions],
            "wording": ["positively worded" if i % 2 == 0 else "negatively worded" for i in range(10)],
        }
    )
    contrib_chart = (
        alt.layer(
            alt.Chart(contrib_df).mark_bar(cornerRadiusEnd=3, width=24, stroke="#ffffff", strokeWidth=1).encode(
                x=alt.X("question:N", sort=None, title=None, axis=alt.Axis(labelAngle=0)),
                y=alt.Y(
                    "favorability:Q",
                    title="answer favorability (5 = best)",
                    scale=alt.Scale(domain=[0, 5]),
                    axis=alt.Axis(values=[1, 2, 3, 4, 5]),
                ),
                color=alt.Color(
                    "wording:N",
                    scale=alt.Scale(domain=["positively worded", "negatively worded"], range=[MOSS, VIOLET]),
                    legend=alt.Legend(title=None, orient="top"),
                ),
                tooltip=[alt.Tooltip("question:N"),
                         alt.Tooltip("favorability:Q", title="favorability (1-5)"),
                         alt.Tooltip("sus_points:Q", title="SUS points (0-4)"),
                         alt.Tooltip("lost:Q", title="points lost")],
            ),
            alt.Chart(contrib_df).mark_rule(color=GRAY, strokeDash=[4, 3]).encode(y=alt.datum(5)),
        )
        .properties(width=500, height=170)
        .configure_view(strokeOpacity=0)
        .configure_axis(labelColor=INK_MUTED, titleColor=INK_MUTED)
    )
    DIMENSIONS = {
        "Adoption intent": [1], "Complexity": [2, 8], "Ease of learning": [3, 7, 10],
        "Need for support": [4], "System integration": [5], "Consistency": [6], "Confidence": [9],
    }
    dim_losses = sorted(
        (
            (dim, 4 * len(qs) - sum(contributions[q - 1] for q in qs), 4 * len(qs))
            for dim, qs in DIMENSIONS.items()
        ),
        key=lambda t: -(t[1] / t[2]),
    )
    dim_table = "\n".join(
        f"| {dim} | {', '.join(f'Q{q}' for q in qs)} | {sum(contributions[q - 1] for q in qs) + len(qs)}/{5 * len(qs)} |"
        for dim, qs in DIMENSIONS.items()
    )
    top_losses = [t for t in dim_losses if t[1] > 0][:3]
    loss_line = (
        "Costing you the most right now: " + ", ".join(f"**{d}** (−{miss})" for d, miss, _ in top_losses) + "."
        if top_losses else "A perfect 100 — nothing is leaking. Try answering honestly."
    )
    dims_tab = mo.vstack([
        contrib_chart,
        mo.md(
            f"""
    Favorability is your answer with the scale always pointing the same way: 5 is
    the best possible answer whether the question is worded positively or
    negatively. The dashed line is a perfect answer; the gap below it is lost
    usability. SUS folds several dimensions into one number:

    | Dimension | Questions | Your answers |
    |---|---|---|
    {dim_table}

    {loss_line}
    """
        ),
    ])

    # -- tab 3: benchmarks --
    bench_df = pd.DataFrame(
        [
            {"name": "Average software product", "score": 68, "kind": "benchmark"},
            {"name": "Good usability", "score": 75, "kind": "benchmark"},
            {"name": "Excellent usability", "score": 85, "kind": "benchmark"},
            {"name": "World-class usability", "score": 90, "kind": "benchmark"},
            {"name": "Your score", "score": round(final_score, 1), "kind": "yours"},
        ]
    )
    bench_chart = (
        alt.Chart(bench_df)
        .mark_bar(cornerRadiusEnd=4, height=18, stroke="#ffffff", strokeWidth=1)
        .encode(
            x=alt.X("score:Q", title="SUS score", scale=alt.Scale(domain=[0, 100])),
            y=alt.Y("name:N", sort=None, title=None),
            color=alt.Color("kind:N", scale=alt.Scale(domain=["benchmark", "yours"], range=[GRAY, MOSS]), legend=None),
            tooltip=[alt.Tooltip("name:N"), alt.Tooltip("score:Q")],
        )
        .properties(width=500, height=150)
        .configure_view(strokeOpacity=0)
        .configure_axis(labelColor=INK_MUTED, titleColor=INK_MUTED)
    )
    bench_tab = mo.vstack([
        bench_chart,
        mo.md(
            "68 is the empirical average across many hundreds of studies, so 68 is a C, "
            "not \"two points from failing\": grades curve against real products, not "
            "against 100. Grading follows the curved scale popularized by Sauro and Lewis."
        ),
    ])

    mo.ui.tabs(
        {
            "How the score is computed": formula_tab,
            "Where your points leak": dims_tab,
            "Benchmarks & grades": bench_tab,
        }
    )
    return


@app.cell
def _(mo, section_banner):
    section_banner(
        "03 · ai product simulator",
        "Same model, different products",
        "Three sliders stand in for design decisions: trust communication, "
        "learnability, workflow complexity. The simulator maps them onto the ten SUS "
        "questions and scores the result, live, right below.",
    )
    return


@app.cell
def _(mo):
    scenario = mo.ui.radio(
        options=["A · Powerful AI, Poor Trust", "B · Trusted AI Workflow"],
        value="A · Powerful AI, Poor Trust",
        label="load a scenario, then adjust",
    )
    return (scenario,)


@app.cell
def _(mo, scenario):
    SCENARIOS = {
        "A · Powerful AI, Poor Trust": {
            "blurb": "An AI assistant produces impressive outputs but users are unsure when to trust the results.",
            "trust": 3, "learn": 5, "complexity": 6,
        },
        "B · Trusted AI Workflow": {
            "blurb": "An AI platform clearly communicates limitations, integrates into workflows, and helps users accomplish tasks.",
            "trust": 9, "learn": 8, "complexity": 2,
        },
    }
    preset = SCENARIOS[scenario.value]
    # Picking a scenario recreates the sliders at its presets; then they're yours.
    sim_trust = mo.ui.slider(0, 10, step=1, value=preset["trust"], label="trust & confidence signals")
    sim_learn = mo.ui.slider(0, 10, step=1, value=preset["learn"], label="learnability")
    sim_complexity = mo.ui.slider(0, 10, step=1, value=preset["complexity"], label="workflow complexity (higher = worse)")
    return SCENARIOS, preset, sim_complexity, sim_learn, sim_trust


@app.cell
def _(np, sim_complexity, sim_learn, sim_trust, sus_score):
    def simulate_responses(trust, learn, complexity):
        """Map three product qualities (0-10) onto the ten SUS responses (1-5).

        Trust drives Q9 (confidence) and Q6 (consistency); learnability drives
        Q4, Q7, Q10; complexity drives Q2, Q3, Q8. Weights are illustrative:
        the lesson is the direction of the arrows, not the decimals.
        """
        ease = 10 - complexity
        blend = (trust + learn + ease) / 3
        raw = [
            1 + 4 * blend / 10,                                    # Q1  use frequently
            1 + 4 * complexity / 10,                               # Q2  unnecessarily complex
            1 + 4 * (0.5 * ease + 0.5 * learn) / 10,               # Q3  easy to use
            5 - 4 * learn / 10,                                    # Q4  need support
            1 + 4 * (0.6 * ease + 0.4 * trust) / 10,               # Q5  well integrated
            5 - 4 * trust / 10,                                    # Q6  inconsistency
            1 + 4 * learn / 10,                                    # Q7  learn quickly
            1 + 4 * (0.8 * complexity + 0.2 * (10 - trust)) / 10,  # Q8  cumbersome
            1 + 4 * trust / 10,                                    # Q9  felt confident
            5 - 4 * (0.7 * learn + 0.3 * ease) / 10,               # Q10 much to learn
        ]
        return [int(np.clip(round(v), 1, 5)) for v in raw]

    sim_responses = simulate_responses(sim_trust.value, sim_learn.value, sim_complexity.value)
    sim_score = sus_score(sim_responses)
    return sim_score, simulate_responses


@app.cell
def _(
    AMBER,
    INK_MUTED,
    MONO,
    MOSS,
    ROSE,
    SAGE,
    SCENARIOS,
    TINT_BORDER,
    alt,
    final_score,
    mo,
    pd,
    preset,
    scenario,
    sim_complexity,
    sim_learn,
    sim_score,
    sim_trust,
    simulate_responses,
    stat_tile,
    sus_grade,
    sus_score,
):
    preset_scores = {
        name: sus_score(simulate_responses(p["trust"], p["learn"], p["complexity"]))
        for name, p in SCENARIOS.items()
    }
    sim_grade, sim_verdict = sus_grade(sim_score)
    sim_df = pd.DataFrame(
        [
            {"name": "Scenario A preset", "score": preset_scores["A · Powerful AI, Poor Trust"], "who": "poor trust"},
            {"name": "Scenario B preset", "score": preset_scores["B · Trusted AI Workflow"], "who": "trusted workflow"},
            {"name": "Your sliders", "score": sim_score, "who": "yours"},
        ]
    )
    sim_chart = (
        alt.Chart(sim_df)
        .mark_bar(cornerRadiusEnd=4, height=18, stroke="#ffffff", strokeWidth=1)
        .encode(
            x=alt.X("score:Q", title=None, scale=alt.Scale(domain=[0, 100])),
            y=alt.Y("name:N", sort=None, title=None),
            color=alt.Color(
                "who:N",
                scale=alt.Scale(domain=["poor trust", "trusted workflow", "yours"], range=[ROSE, MOSS, AMBER]),
                legend=None,
            ),
            tooltip=[alt.Tooltip("name:N"), alt.Tooltip("score:Q", format=".1f")],
        )
        .properties(width=290, height=90)
        .configure_view(strokeOpacity=0)
        .configure_axis(labelColor=INK_MUTED, titleColor=INK_MUTED)
    )
    scenario_card = mo.Html(
        f'<div style="background:#fbfdf9;border:1.5px solid {TINT_BORDER};'
        f'border-left:5px solid {MOSS};border-radius:12px;padding:10px 14px;">'
        f'<div style="font-family:{MONO};font-size:10.5px;letter-spacing:0.1em;'
        f'text-transform:uppercase;color:{SAGE};margin-bottom:4px;">scenario {scenario.value[0]}</div>'
        f'<div style="font-size:13px;line-height:1.5;color:{INK_MUTED};font-style:italic;">'
        f'"{preset["blurb"]}"</div></div>'
    )
    left_col = mo.vstack(
        [scenario, scenario_card, sim_trust, sim_learn, sim_complexity],
        gap=0.6,
    )
    right_col = mo.vstack(
        [
            mo.Html(
                '<div style="display:flex;gap:8px;flex-wrap:wrap;">'
                + stat_tile("simulated SUS", f"{sim_score:.1f}", sim_grade + " · " + sim_verdict, color=AMBER)
                + stat_tile("vs your score", f"{sim_score - final_score:+.1f}", "simulator minus your answers")
                + "</div>"
            ),
            sim_chart,
        ],
        gap=0.6,
    )
    mo.vstack([
        mo.hstack([left_col, right_col], widths=[1.2, 1], gap=1.5, align="start", wrap=True),
        mo.md(
            "*Try it: load Scenario A, then raise only the trust slider. The distance "
            "the score travels before you touch complexity is the usability value of "
            "honest confidence communication, the cheapest feature an AI product can ship.*"
        ),
    ])
    return


@app.cell
def _(mo, section_banner):
    mo.vstack([
        section_banner(
            "04 · what the number means",
            "Capability is necessary. Usability is what gets adopted.",
            "A high SUS score does not mean a better model, more parameters, more "
            "features, or higher benchmark performance. It means users understand "
            "the system, trust the workflow, and can achieve their goals.",
        ),
        mo.md(
            r"""
    > **Technical excellence + Human usability = Adoption**
    """
        ),
    ])
    return


@app.cell
def _(MONO, PINE, mo):
    mo.Html(
        f'<div style="background:linear-gradient(150deg,#0f2419 0%,{PINE} 60%,#2e5d24 100%);'
        'border-radius:16px;padding:22px 26px;margin-top:22px;">'
        '<div style="color:#f5faf1;font-size:19px;font-weight:750;line-height:1.45;max-width:36rem;">'
        '"Great technology creates possibilities. Great usability turns those '
        'possibilities into adoption."</div>'
        f'<div style="font-family:{MONO};color:#8fa887;font-size:11.5px;margin-top:12px;line-height:1.7;">'
        'Built with <a href="https://marimo.io" style="color:#9fd48a;">marimo</a>. '
        'Runs entirely in your browser; nothing is sent anywhere. '
        'More at <a href="https://rodrigosf.com/blog/" style="color:#9fd48a;">rodrigosf.com/blog</a>.'
        '</div></div>'
    )
    return


if __name__ == "__main__":
    app.run()
