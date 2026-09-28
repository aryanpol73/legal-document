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

---

## 👥 Team Split & Responsibilities

### **Person A: Ingestion Pipeline ("How documents become searchable")**
- `src/ingest.py`: PyMuPDF parsing, page numbers, header/footer cleanup
- `src/chunker.py`: Heading detection, section-aware chunking
- `src/store.py`: Embeddings, ChromaDB persistence, metadata management
- *Later iterations*: OCR fallback for scanned PDFs, table extraction, version/effective_from tracking

### **Person B: Query Pipeline ("How questions become cited answers")**
- `src/retriever.py`: Dense search, BM25 keyword search, Reciprocal Rank Fusion (RRF), Cross-Encoder reranker
- `src/answer.py`: Prompt synthesis, numbered sources, `[S1]` inline citations, abstention rules, citation verifier
- `src/api.py`: FastAPI service endpoints
- `app.py`: Streamlit interactive UI

### **Together (Shared Ownership)**
- `src/schemas.py`: The chunk metadata contract (strictly agreed upon before building)
- `eval/gold_set.jsonl`: 50–100 ground-truth questions and evaluation harness

---

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

---

## 🔄 Delivery Stages

| Stage | Person A (Ingestion) | Person B (Query) |
|---|---|---|
| **1. Dense-only prototype** | Parse one PDF, split naively by size, store in Chroma | Query Chroma, build prompt, call LLM, print answer with `[S1]` markers |
| **2. Real structure** | Structure-aware chunking (chapter/section/clause detection) | BM25 + Reciprocal Rank Fusion (RRF) |
| **3. Harder documents** | Tables, OCR fallback, version metadata | Cross-encoder reranker, relevance floor for safe abstention |
| **4. Trust** | Eval harness (Recall@k, MRR) | Citation verifier & FastAPI endpoints |
| **5. Polish** | Streamlit UI (*ownership swapped*) | Ablations & results write-up (*ownership swapped*) |

---

## 🌿 Git & Collaboration Workflow

1. Protect `main`.
2. Use feature branches (e.g., `feat/chunker-sections`, `feat/hybrid-retrieval`).
3. Open small PRs; the other partner reviews each PR thoroughly before merging.
4. Conduct a 20-minute walkthrough after each stage with real intermediate outputs.
5. Swap ownership in Stage 5 so both engineers master the complete pipeline.
