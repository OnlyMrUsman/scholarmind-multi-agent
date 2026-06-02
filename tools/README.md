# ScholarMind Tool Service

FastAPI service backing the ScholarMind multi-agent system.

Endpoints:
- GET  /search_papers       -> search the public arXiv API
- POST /extract_keyphrases  -> hand-written NLP keyphrase extractor
- GET  /health              -> liveness check

## Run (WSL2 Ubuntu)
    cd ~/projects/scholarmind-multi-agent/tools
    python3 -m venv .venv-tools
    source .venv-tools/bin/activate
    pip install -r requirements.txt
    python app.py

Service runs on http://0.0.0.0:8900
From Dify Docker containers it is reachable at http://host.docker.internal:8900
