
from __future__ import annotations

import re
import time
import logging
from collections import Counter
from typing import List

import httpx
import feedparser
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scholarmind")

app = FastAPI(
    title="ScholarMind Tool Service",
    description="Academic search + NLP tools for the ScholarMind multi-agent system.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ARXIV_API = "https://export.arxiv.org/api/query"
HTTP_HEADERS = {
    "User-Agent": "ScholarMind/1.0 (NLP course project; mailto:usmanch7829@gmail.com)"
}


class Paper(BaseModel):
    title: str
    authors: List[str]
    summary: str
    published: str
    pdf_url: str
    arxiv_id: str
    primary_category: str


class SearchResponse(BaseModel):
    query: str
    count: int
    papers: List[Paper]


class KeyphraseRequest(BaseModel):
    text: str = Field(..., description="Raw text to analyse.")
    top_k: int = Field(10, description="How many keyphrases to return.")


class KeyphraseResponse(BaseModel):
    top_k: int
    keyphrases: List[str]


@app.get("/search_papers", response_model=SearchResponse)
def search_papers(query: str, max_results: int = 8, sort_by: str = "relevance"):
    sort_map = {
        "relevance": "relevance",
        "lastUpdatedDate": "lastUpdatedDate",
        "submittedDate": "submittedDate",
    }
    sort_param = sort_map.get(sort_by, "relevance")
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max(1, min(max_results, 25)),
        "sortBy": sort_param,
        "sortOrder": "descending",
    }
    try:
        with httpx.Client(timeout=30.0, headers=HTTP_HEADERS) as client:
            resp = client.get(ARXIV_API, params=params)
            resp.raise_for_status()
    except Exception as exc:
        logger.exception("arXiv request failed")
        raise HTTPException(status_code=502, detail=f"arXiv request failed: {exc}")

    feed = feedparser.parse(resp.text)
    papers: List[Paper] = []
    for entry in feed.entries:
        arxiv_id = entry.get("id", "").split("/abs/")[-1]
        pdf_url = ""
        for link in entry.get("links", []):
            if link.get("type") == "application/pdf":
                pdf_url = link.get("href", "")
        if not pdf_url and arxiv_id:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
        authors = [a.get("name", "") for a in entry.get("authors", [])]
        summary = re.sub(r"\s+", " ", entry.get("summary", "")).strip()
        cat = ""
        if isinstance(entry.get("arxiv_primary_category"), dict):
            cat = entry.get("arxiv_primary_category", {}).get("term", "")
        papers.append(
            Paper(
                title=re.sub(r"\s+", " ", entry.get("title", "")).strip(),
                authors=authors,
                summary=summary,
                published=entry.get("published", ""),
                pdf_url=pdf_url,
                arxiv_id=arxiv_id,
                primary_category=cat,
            )
        )
    return SearchResponse(query=query, count=len(papers), papers=papers)


STOPWORDS = set("""
a an the and or but if while of to in on for with without within into onto from
by at as is are was were be been being this that these those it its their our your
we they he she you i them us not no nor so than then thus also however moreover
which who whom whose what when where why how can could should would may might must
will shall do does did done has have had using used use based via per such other
more most some any all each both few many much one two three new approach
method methods model models result results paper study propose proposed show shows
shown present presents presented
""".split())

WORD_RE = re.compile(r"[A-Za-z][A-Za-z\-]+")


def extract_keyphrases(text: str, top_k: int = 10) -> List[str]:
    tokens = [t.lower() for t in WORD_RE.findall(text)]
    content = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    unigram_freq = Counter(content)
    bigrams = [f"{content[i]} {content[i+1]}" for i in range(len(content) - 1)]
    bigram_freq = Counter(bigrams)
    scores: Counter = Counter()
    for word, freq in unigram_freq.items():
        scores[word] += freq
    for phrase, freq in bigram_freq.items():
        scores[phrase] += freq * 2.5
    return [phrase for phrase, _ in scores.most_common(top_k)]


@app.post("/extract_keyphrases", response_model=KeyphraseResponse)
def extract_keyphrases_endpoint(req: KeyphraseRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text must not be empty")
    phrases = extract_keyphrases(req.text, req.top_k)
    return KeyphraseResponse(top_k=req.top_k, keyphrases=phrases)


@app.get("/health")
def health():
    return {"status": "ok", "service": "scholarmind-tools", "time": time.time()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8900, reload=False)
