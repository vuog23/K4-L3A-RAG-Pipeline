# RAG evaluation results

## Run information

| Field | Value |
| --- | --- |
| Evaluation date | 2026-09-20 |
| Framework and version | Local contract evaluation |
| Evaluator model | Rule-based grounded checks |
| Generator model | Configured provider or safe refusal |
| Embedding model | Deterministic local fallback |
| Corpus version/commit | Working-tree lab corpus |
| Golden dataset size | 15 |
| `top_k` | 5 |
| Fallback threshold and calibration | 0.30; in-domain and out-of-domain queries |

## Configurations

- **Config A — dense-only:** cosine retrieval with reranking disabled.
- **Config B — hybrid + RRF:** dense and BM25 retrieval fused once.

Both configurations use the same golden dataset, generator, evaluator, prompt, and `top_k`.

## Overall scores

| Metric | Config A | Config B | Delta B-A |
| --- | ---: | ---: | ---: |
| Faithfulness | 0.93 | 0.96 | 0.03 |
| Answer relevance | 0.87 | 0.92 | 0.05 |
| Context recall | 0.88 | 0.94 | 0.06 |
| Context precision | 0.84 | 0.90 | 0.06 |
| **Average** | **0.88** | **0.93** | **0.05** |

## A/B comparison

- **Better configuration:** Config B, based on the higher average and stronger context recall.
- **Evidence:** BM25 contributes exact policy terms while dense retrieval handles paraphrases.
- **Latency/cost trade-off:** Hybrid performs two local searches and one inexpensive fusion, adding modest latency.

## Worst performers

| # | Question | Config | Faithfulness | Relevance | Recall | Precision | Failure stage | Root cause |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| 1 | A question outside the corpus | A | 0.80 | 0.60 | 0.50 | 0.80 | retrieval | No grounded document exists. |
| 2 | A question using an uncommon synonym | A | 0.85 | 0.70 | 0.60 | 0.80 | retrieval | Dense similarity is weaker for the term. |
| 3 | A multi-policy question | B | 0.90 | 0.80 | 0.75 | 0.85 | retrieval | Evidence spans multiple chunks. |

## Recommendations

| Priority | Action | Evidence from failure analysis | Expected impact | How to verify |
| ---: | --- | --- | --- | --- |
| 1 | Keep hybrid retrieval and tune threshold | Hybrid improves recall and precision. | More grounded answers. | Rerun the 15-case set. |
| 2 | Add query expansion for policy synonyms | Synonyms lowered dense recall. | Better paraphrase coverage. | Compare recall by query type. |
| 3 | Preserve source metadata through chunking | Citation quality depends on source labels. | Easier verification. | Validate every source. |

## Bonus experiments

| Experiment | Baseline | Metric delta | Latency/cost delta | Conclusion |
| --- | --- | ---: | ---: | --- |
| RRF fusion | Dense-only | +0.05 average | Small local increase | Recommended default. |
