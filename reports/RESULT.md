# RAG Evaluation Results

## Evaluation status

No scored evaluation run is present in this repository. The repository contains a 15-question golden set, but it does not contain a recorded run artifact, metric calculation output, or a reproducible evaluator configuration. Therefore, this report does not claim numeric scores or an A/B winner. The earlier numeric figures in this file had no supporting run output and have been removed.

## Available evaluation inputs

| Field | Recorded value |
| --- | --- |
| Golden dataset | `group_project/evaluation/golden_dataset.json` |
| Dataset size | 15 questions |
| Corpus | 3 policy Markdown documents and 5 news Markdown documents under `data/standardized/` |
| Retrieval top-k | Pipeline default is 5 |
| Dense implementation | Deterministic local token-hash embeddings (64 dimensions) with cosine similarity |
| Sparse implementation | BM25 when `rank-bm25` is installed; token-count fallback otherwise |
| Hybrid implementation | Reciprocal Rank Fusion over dense and sparse result lists |
| Generator/evaluator | No successful evaluation run or fixed model/version recorded |
| Evaluation date / corpus commit | Not recorded |

The configured string `BAAI/bge-m3` in the indexing module is not the embedding model used by the current implementation: `embed_texts()` generates deterministic local token-hash vectors. The results must not be described as BGE-M3 results.

## Required comparison protocol

Run both configurations over the same 15 questions, corpus snapshot, generation prompt, generator, evaluator, and `top_k=5`:

- **A — dense only:** use dense retrieval with RRF disabled.
- **B — hybrid + RRF:** retrieve dense and BM25 candidates and fuse them once with RRF.

Record per-question faithfulness, answer relevance, context recall, and context precision, along with model names/versions, package versions, run date, corpus commit, threshold, and latency/cost. Report arithmetic means and `B − A` for each metric. Keep the per-question outputs so the three weakest cases and their failure stages can be checked. An out-of-domain refusal case should be assessed separately from answerable questions.

## Results

| Metric | A: dense only | B: hybrid + RRF | Delta (B − A) |
| --- | ---: | ---: | ---: |
| Faithfulness | Not measured | Not measured | — |
| Answer relevance | Not measured | Not measured | — |
| Context recall | Not measured | Not measured | — |
| Context precision | Not measured | Not measured | — |
| Average | Not measured | Not measured | — |

**A/B conclusion:** Undetermined; no comparable scored run is available. Do not infer that hybrid is better from the implementation alone.

## Known limitations and next steps

1. Add and run a versioned evaluation script that exports per-question results and aggregate metric means for both configurations.
2. Record the actual embedding implementation and model configuration; the current local hash vectors are a lightweight offline baseline, not a semantic embedding model.
3. Check the golden set against the source documents before scoring. The question “Where are registration notices published?” has an expected answer mentioning a student portal, while article 01 only says that the registrar published guidance; the extra portal detail is not supported by the supplied corpus.
4. Record source URLs and provenance for the corpus before treating it as a production knowledge base; current standardized files do not include URLs.

## Bonus experiments

No bonus experiment has a recorded measurement. RRF is implemented, but implementation by itself is not evidence of a metric improvement.
