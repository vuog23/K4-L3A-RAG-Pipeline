"""
Task 6 — Lexical search bằng BM25.

Dùng cùng corpus chunks với Task 5. BM25 phù hợp với từ khóa chính xác, mã tài
liệu và tên riêng. Output phải theo SearchResult và sort score giảm dần.
"""


CORPUS: list[dict] = []


def build_bm25_index(corpus: list[dict]):
    """Tạo BM25 index từ cùng corpus chunks của Task 4."""
    # TODO: Tokenize và tạo BM25 index.
    #
    # from rank_bm25 import BM25Okapi
    # tokenized = [item["content"].lower().split() for item in corpus]
    # return BM25Okapi(tokenized)
    try:
        from rank_bm25 import BM25Okapi
        return BM25Okapi([item["content"].lower().split() for item in corpus])
    except ImportError:
        return None


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """Trả về BM25 SearchResult theo score giảm dần."""
    # TODO: Tính BM25 scores và map lại corpus.
    #
    # import numpy as np
    # bm25 = build_bm25_index(CORPUS)
    # scores = bm25.get_scores(query.lower().split())
    # indices = np.argsort(scores)[::-1][:top_k]
    # results = []
    # for index in indices:
    #     if scores[index] <= 0:
    #         continue
    #     item = CORPUS[index]
    #     results.append({
    #         "id": item["id"],
    #         "content": item["content"],
    #         "score": float(scores[index]),
    #         "metadata": item["metadata"],
    #         "retrieval_method": "bm25",
    #     })
    # return results
    if top_k <= 0 or not CORPUS:
        return []
    index = build_bm25_index(CORPUS)
    tokens = query.lower().split()
    if index is not None:
        scores = list(index.get_scores(tokens))
    else:
        scores = [sum(text.lower().split().count(token) for token in tokens) for text in [x["content"] for x in CORPUS]]
    order = sorted(range(len(CORPUS)), key=lambda i: (-scores[i], i))
    return [{"id": CORPUS[i]["id"], "content": CORPUS[i]["content"], "score": float(scores[i]),
             "metadata": CORPUS[i]["metadata"], "retrieval_method": "bm25"} for i in order[:top_k] if scores[i] > 0]


if __name__ == "__main__":
    for result in lexical_search("test query", top_k=3):
        print(result)
