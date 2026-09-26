# RAG Evaluation Results

## Evaluation status

The repository contains a 15-question golden dataset but no recorded scored run, per-question metric output, or reproducible evaluator configuration. Numeric scores and an A/B winner cannot be reported from the available evidence. The previous score table was unsupported and has been withdrawn.

## Run information

| Field | Recorded value |
| --- | --- |
| Evaluation date | No scored run recorded |
| Evaluation framework/version | No run configuration recorded |
| Evaluator model | Not recorded |
| Generator model | No successful evaluation run recorded |
| Embedding implementation | Deterministic local token-hash vectors, 64 dimensions |
| Golden dataset | `golden_dataset.json` (15 questions) |
| Corpus | 3 policy documents and 5 news documents in `data/standardized/` |
| `top_k` | Pipeline default: 5 |
| Threshold | Pipeline default: 0.30; calibration results not recorded |
| Corpus commit | Not recorded for an evaluation run |

Although the indexing module declares `BAAI/bge-m3`, the active `embed_texts()` implementation creates local token-hash vectors. Do not attribute results to BGE-M3.

## Configurations and results

The intended comparison is A: dense retrieval with RRF disabled, versus B: dense plus BM25 fused once with RRF. Both must use the same corpus snapshot, 15 questions, generator, prompt, evaluator, and `top_k=5`.

| Metric | A: dense only | B: hybrid + RRF | Delta (B − A) |
| --- | ---: | ---: | ---: |
| Faithfulness | Not measured | Not measured | — |
| Answer relevance | Not measured | Not measured | — |
| Context recall | Not measured | Not measured | — |
| Context precision | Not measured | Not measured | — |
| Average | Not measured | Not measured | — |

**A/B conclusion:** Undetermined. RRF is implemented, but no comparable scored run establishes whether it improves quality, latency, or cost.

## Data quality note

The golden question “Where are registration notices published?” expects “By the registrar and in the student portal,” but standardized article 01 only says the registrar published registration guidance. The student-portal detail is not supported by the current corpus and should be corrected or sourced before evaluation.

## Next steps

1. Add a versioned runner that evaluates both configurations and saves per-question answers, retrieved contexts, four metrics, and aggregate means.
2. Record model/package versions, run date, corpus commit, threshold calibration, and latency/cost.
3. Check all expected answers against cited source passages and add verifiable corpus provenance.
4. Re-run after fixing dataset and embedding configuration; then fill the score table and analyze the three weakest cases.
