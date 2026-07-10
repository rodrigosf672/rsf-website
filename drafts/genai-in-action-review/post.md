# The Raffle Ticket That Rewired How I Think About AI Products

*A review of Generative AI in Action by Amit Bahree (Manning), from the perspective of someone who builds developer tools.*

> Pull quote: "I expected a book about how language models work. I finished it thinking about orchestration layers, evaluation budgets, and why grounding is a trust decision, not a technical one."

---

## A raffle at PyData Boston

Last December I was at PyData Boston, doing the thing you do between talks: wandering the sponsor tables, half looking for stickers, half looking for conversations. The Anaconda booth had both. Dawn Wages, Daina Bouquin, and Jessica Stefanowicz were running it, and it was one of those booths where you stop for thirty seconds and stay for twenty minutes. We talked about Python packaging, community, and the strange moment the data ecosystem is living through. I dropped my name in their raffle mostly as a formality.

I won a copy of *Generative AI in Action* by Amit Bahree.

I want to be honest about my expectations. Conference raffle books have a certain reputation. They go on the shelf, they collect intentions, they wait. This one did not wait long, and it turned out to be one of the most useful technical books I have read in the past few years. Not because it taught me an API, but because it quietly replaced the mental model I was using for AI products.

This is also a small argument for going to conferences at all. The talks are recorded. The conversations are not. A raffle ticket handed over by a booth team that clearly cares about its community turned into months of thinking. That exchange rate is hard to beat.

## This was not really a book about prompts

The book covers prompts, of course. There is a full chapter on prompt engineering, with system messages, zero-shot and few-shot patterns, chain of thought, and advice about clear syntax. It is good material, and the interactive widgets below borrow from it.

But treating this as a prompt book would be like treating a civil engineering textbook as a book about bricks. The prompt is the visible artifact. The book is about everything around it: the model choices, the retrieval pipelines, the orchestration layer that decides what actually reaches the model, the filters on the way out, the evaluation harness that tells you whether any of it works, and the operational machinery that keeps it working at scale.

Bahree structures the book in three movements. Foundations first: what these models are, how tokens and embeddings and context windows behave, and what the configuration knobs actually do. Then techniques: prompt engineering, retrieval-augmented generation, chatting with your own data, fine-tuning. Then the part that most books skip and most teams need: application architecture, production deployment, evaluations, and responsible AI.

That third movement is where the book earns its title. "In action" turns out to mean "in production, with users, under constraints."

## Thinking like a product builder

I work on developer tools. My daily questions are about workflows, adoption, and trust: will a data scientist trust this output, will this fit how people already work, what happens when it fails. Reading this book, I kept noticing that the same questions govern AI products, just wearing different clothes.

A few shifts stuck with me.

**Model configuration is a product surface, not a tuning detail.** Temperature, top_p, penalties, and max tokens read like implementation trivia until you realize they encode a product decision: how much unpredictability are you willing to ship? The book is refreshingly practical here, down to advice like adjusting temperature or top_p but not both. A support bot and a brainstorming tool might use the same model and be entirely different products because of these numbers.

**Retrieval is a trust architecture.** The RAG chapters frame retrieval not as a clever trick but as the mechanism that lets a general model answer from your data, with provenance. Once you see grounding as the thing that turns "plausible" into "verifiable," a lot of product decisions clarify. Chunking strategy, embedding choice, and vector search stop being infrastructure minutiae and become the difference between an answer a user can check and an answer a user has to believe.

**Adaptation has a cost gradient.** The book is careful about fine-tuning: when it helps, what it costs, and how often prompting or retrieval solves the problem more cheaply. That ordering, prompt first, ground next, fine-tune last, is really a resource allocation argument, the kind product managers make about any feature.

**Operations are where AI products live or die.** The production chapter talks about latency budgets, time to first token, quotas, rate limits, and the pay-as-you-go economics of tokens. None of this is glamorous. All of it decides whether users experience your product as instant and reliable or as a spinner with occasional poetry.

**Evaluation is testing with a different accent.** BLEU, ROUGE, and BERTScore on one side; LLM-based approaches like G-Eval and broad benchmarks like HELM on the other. What struck me is how familiar the underlying discipline is. You define what good means, you measure it continuously, you distrust single numbers. I have spent years arguing for thoughtful testing in software. Evaluations are the same argument relocated.

## The chapter that changed my perspective

Chapter 10, on application architecture, is the one I keep returning to.

It opens with two framings: Karpathy's "Software 2.0," where learned behavior replaces handwritten logic, and the copilot pattern, where AI augments a human who stays in charge. Then it does something genuinely useful: it lays out a GenAI application stack, layer by layer, the way we once talked about the LAMP stack. Infrastructure at the bottom, foundation models above it, then an orchestration layer that handles grounding, response filtering, and plugin execution, and finally the application the user actually touches.

Why did this change my perspective? Because it made AI legible as software infrastructure. Before reading it, I mentally filed most AI products as "a model with a UI." Afterward, I could not unsee the middle: the orchestration layer is where the interesting engineering and most of the product risk lives. It decides what context the model sees, what tools it may call, and what is allowed out. It is also, not coincidentally, where trust is implemented.

The evaluations chapter is a close second, for a personal reason. I gave a talk this year about testing in the age of AI-generated code, and the book's treatment of evals reads like the missing appendix to that argument. If generation is cheap, judgment becomes the scarce resource. Evals are how you industrialize judgment.

## Things I immediately wanted to experiment with

I think best by building, and I write and prototype in marimo notebooks these days, so the book turned into a to-do list.

The first thing I built is the set of interactive explainers embedded in this post: a model configuration playground that shows how temperature and top_p reshape a token distribution, a prompt pattern explorer, a clickable version of the application stack, a fine-tuning decision helper, and a responsible AI checklist. None of them call a model. That is deliberate. The concepts are about distributions, structures, and tradeoffs, and you can teach those with careful simulation, reproducibly, in the browser.

There is something fitting about using a reactive notebook for this. The book's deepest theme is that AI systems are systems, with dependencies and dataflow and failure modes. A notebook where every cell declares its dependencies and updates deterministically is a small, honest model of the discipline the book asks for at production scale. Reproducibility is not a garnish here. It is the point.

It also left me with product questions I am still chewing on for the notebook and IDE world I work in. What does grounding look like inside an exploratory data analysis session? Where does an evaluation harness live when the "application" is a scientist's notebook? Which layer of the stack should a tool like a data science IDE own, and which should it merely observe?

## Why I would recommend it

Not because it will teach you the latest API. Books cannot win that race, and this one knows it. Model names age; the chapters on architecture, evaluation, deployment, and risk do not.

I would recommend it because it helps people think clearly about AI systems, and clear thinking is the actual bottleneck right now. Developers will get a map of the whole stack instead of a pile of snippets. Product managers and TPMMs will get the vocabulary to interrogate architecture decisions instead of accepting them. Developer advocates will find honest framings that do not oversell. Data scientists will find the bridge between experimentation and production that their organizations keep asking them to cross.

The book treats generative AI as infrastructure with tradeoffs rather than magic with a rate card, and that stance is worth the cover price on its own. Or, in my case, worth one extremely lucky raffle ticket.

Thank you, Amit Bahree, for writing a book that respects both the technology and the reader. And thank you Dawn Wages, Daina Bouquin, and Jessica Stefanowicz, and the Anaconda crew at PyData Boston, for the conversation, the community, and the ticket. Conferences are made of talks, but they are remembered for exchanges like that one.

## What book should I review next?

There is a small poll at the end of the interactive notebook. Current candidates: *AI Engineering*, *Designing Machine Learning Systems*, *Build*, *Software Engineering at Google*, and *Building LLM Applications*. Vote, and if you have a dark horse, my inbox is open.

---

*Rodrigo Silva Ferreira builds open source tools, studies how developers adopt AI, and translates technical innovation into products developers trust and love to use. He speaks regularly at Python and data science conferences.*
