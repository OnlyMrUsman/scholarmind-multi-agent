# ScholarMind — Multi-Agent Academic Research Assistant

ScholarMind is a multi-agent academic research assistant built on the Dify platform. Given a research question, five cooperating agents plan a search strategy, retrieve real papers from arXiv, analyze them, synthesize findings across the literature, and produce a cited mini literature review.

This project was developed as a final project for an NLP course. It demonstrates a collaborative multi-agent pipeline with a clear division of labor, real external tool use, and grounded, citation-backed output.

## What it does

Ask a question like *"What are recent advances in graph neural networks for drug discovery?"* and ScholarMind returns a structured literature review with an introduction, thematic discussion, points of agreement and contradiction across papers, identified research gaps, and a reference list with arXiv IDs, all grounded in papers retrieved live from arXiv.

## Architecture

The system is implemented as a Dify Chatflow composed of five cooperating agents plus supporting logic nodes:

```mermaid
.
├── dify-export/     Dify DSL export (ScholarMind.yml) - import to recreate the full app
├── tools/           FastAPI tool service (app.py, requirements, Dockerfile)
├── report/          Written project report
├── ppt/             Presentation slides
├── screenshots/     Screenshots of the working pipeline
└── docs/            Additional notes and documentation
## Recreating the system

The entire multi-agent app is captured in the Dify DSL export. To recreate it:

1. Install and run Dify (self-hosted).
2. Configure a DeepSeek API key under Settings then Model Provider.
3. In Dify Studio, choose Import DSL and select dify-export/ScholarMind.yml.
4. Publish the app and start a conversation.

## Limitations and future work

- Retrieval is currently limited to arXiv; adding other sources (Semantic Scholar, PubMed) would broaden coverage.
- A vector knowledge base could be reintroduced to support retrieval over a persistent corpus in addition to live search.
- Models can be over-confident on out-of-domain claims; adding a verification agent is a natural next step.

## Author

Muhammad Usman Kazim — Yunnan University

## Acknowledgements

Built on the open-source Dify platform, using the arXiv API for paper retrieval and DeepSeek for language model inference.
