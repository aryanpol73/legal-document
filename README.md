# Legal & Policy Document Grounded QA System

A grounded question-answering system over a fixed corpus of authoritative documents where citation and provenance are as critical as the answer itself.

---

## 🏛️ Pipeline Architecture

```
PDFs ──► Parse (text + page no. + font/heading signals)
     ──► Normalize (dehyphenate, drop headers/footers, fix ligatures)
     ──► Structure detection (Chapter / Section / Clause regex + font heuristics)
     ──► Chunk (clause-level, ~400–800 tokens, 10–15% overlap, never cross a section boundary)
     ──► Embed (bge-base) ──► ChromaDB (vectors + rich metadata)

Query ──► Query preprocessing (expansion, filter extraction)
      ──► Hybrid retrieval: dense top-20 ∪ BM25 top-20 → Reciprocal Rank Fusion
      ──► Cross-encoder rerank → top-5
      ──► Prompt with numbered sources
      ──► LLM answer with inline [S1], [S2] markers
      ──► Citation verifier (drop/flag unsupported claims)
      ──► Response + clickable citations (doc, page, section)
```

## 📁 Project Layout

```text
legal-doc/
├── data/
│   ├── raw_pdfs/        # Source documents (PDFs)
│   └── chroma/          # Persisted vector store (gitignored)
├── src/
│   ├── __init__.py
│   ├── schemas.py       # Shared chunk & query schemas (Contract)
│   ├── ingest.py        # PDF extraction & header/footer normalization
│   ├── chunker.py       # Hierarchical structure-aware chunking
│   ├── store.py         # ChromaDB client & vector persistence
│   ├── retriever.py     # Hybrid dense + BM25 retrieval & reranking
│   ├── answer.py        # LLM generation with strict citation verification
│   └── api.py           # FastAPI backend
├── eval/
│   └── gold_set.jsonl   # Ground truth Q&A evaluation set
├── app.py               # Streamlit web application
├── requirements.txt     # Python project dependencies
├── .env.example         # Example environment configuration
├── .gitignore
└── README.md
```



1. Protect `main`.
2. Use feature branches (e.g., `feat/chunker-sections`, `feat/hybrid-retrieval`).
3. Open small PRs; the other partner reviews each PR thoroughly before merging.
4. Conduct a 20-minute walkthrough after each stage with real intermediate outputs.
5. Swap ownership in Stage 5 so both engineers master the complete pipeline.
