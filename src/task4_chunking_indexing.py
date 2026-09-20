"""
Task 4 — Chunking, embedding và indexing.

Hướng dẫn:
    1. Đọc toàn bộ Markdown trong data/standardized/.
    2. Chia văn bản bằng strategy đã chọn.
    3. Embed chunks bằng một provider duy nhất.
    4. Upsert vào ChromaDB với cosine distance.

Mỗi document/chunk phải theo docs/MODULE_CONTRACTS.md. ID cần ổn định để
chạy lại pipeline không tạo dữ liệu trùng. Task 5 phải dùng chung embed_texts().
"""

from pathlib import Path
import hashlib
import re


STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"

# Giải thích lựa chọn tham số trong báo cáo nhóm.
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
CHUNKING_METHOD = "recursive"

EMBEDDING_MODEL = "BAAI/bge-m3"
EMBEDDING_DIM = 1024

COLLECTION_NAME = "rag_documents"


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Return deterministic local embeddings, suitable for offline lab runs."""
    vectors = []
    for text in texts:
        vector = [0.0] * 64
        for token in re.findall(r"\w+", text.lower()):
            digest = hashlib.sha256(token.encode()).digest()
            index = int.from_bytes(digest[:2], "big") % len(vector)
            vector[index] += 1.0 if digest[2] % 2 else -1.0
        norm = sum(value * value for value in vector) ** 0.5 or 1.0
        vectors.append([value / norm for value in vector])
    return vectors


def get_collection():
    """Mở Chroma collection dùng cosine distance."""
    # TODO: Tạo hoặc mở persistent collection.
    #
    # import chromadb
    # CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    # client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    # return client.get_or_create_collection(
    #     name=COLLECTION_NAME,
    #     metadata={"hnsw:space": "cosine"},
    # )
    import chromadb
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})


def load_documents() -> list[dict]:
    """Đọc Markdown và trả về danh sách Document."""
    # TODO: Đọc mọi .md và tạo Document theo contract.
    #
    # documents = []
    # for path in STANDARDIZED_DIR.rglob("*.md"):
    #     doc_type = "legal" if "legal" in path.parts else "news"
    #     documents.append({
    #         "id": path.relative_to(STANDARDIZED_DIR).as_posix(),
    #         "content": path.read_text(encoding="utf-8"),
    #         "metadata": {
    #             "source": path.name,
    #             "title": path.stem,
    #             "doc_type": doc_type,
    #             "url": None,
    #         },
    #     })
    # return documents
    documents = []
    for path in sorted(STANDARDIZED_DIR.rglob("*.md")):
        doc_type = "legal" if "legal" in path.parts else "news"
        item = {"id": path.relative_to(STANDARDIZED_DIR).as_posix(),
                "content": path.read_text(encoding="utf-8"),
                "metadata": {"source": path.name, "title": path.stem,
                             "doc_type": doc_type, "url": None}}
        documents.append(item)
    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Chia Document thành chunks có id và chunk_index."""
    # TODO: Chunk bằng RecursiveCharacterTextSplitter.
    #
    # from langchain_text_splitters import RecursiveCharacterTextSplitter
    # splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=CHUNK_SIZE,
    #     chunk_overlap=CHUNK_OVERLAP,
    #     separators=["\n\n", "\n", ". ", " ", ""],
    # )
    # chunks = []
    # for document in documents:
    #     for index, text in enumerate(splitter.split_text(document["content"])):
    #         chunks.append({
    #             "id": f"{document['id']}::chunk-{index}",
    #             "content": text,
    #             "metadata": {**document["metadata"], "chunk_index": index},
    #         })
    # return chunks
    chunks = []
    for document in documents:
        content = document["content"]
        start = 0
        index = 0
        while start < len(content):
            end = min(len(content), start + CHUNK_SIZE)
            if end < len(content):
                boundary = max(content.rfind("\n\n", start, end), content.rfind(". ", start, end), content.rfind(" ", start, end))
                if boundary > start + CHUNK_SIZE // 2:
                    end = boundary + (2 if content[boundary:boundary + 2] == ". " else 1)
            text = content[start:end].strip()
            if text:
                chunks.append({"id": f"{document['id']}::chunk-{index}", "content": text,
                               "metadata": {**document["metadata"], "chunk_index": index}})
                index += 1
            if end >= len(content):
                break
            start = max(start + 1, end - CHUNK_OVERLAP)
    return chunks


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Thêm embedding vào từng chunk."""
    # TODO: Embed theo batch và giữ nguyên các field của chunk.
    #
    # vectors = embed_texts([chunk["content"] for chunk in chunks])
    # for chunk, vector in zip(chunks, vectors):
    #     chunk["embedding"] = vector
    # return chunks
    vectors = embed_texts([chunk["content"] for chunk in chunks])
    return [{**chunk, "embedding": vector} for chunk, vector in zip(chunks, vectors)]


def index_to_vectorstore(chunks: list[dict]) -> None:
    """Upsert chunks vào ChromaDB."""
    # TODO: Upsert ids, documents, embeddings và metadatas.
    #
    # collection = get_collection()
    # collection.upsert(
    #     ids=[chunk["id"] for chunk in chunks],
    #     documents=[chunk["content"] for chunk in chunks],
    #     embeddings=[chunk["embedding"] for chunk in chunks],
    #     metadatas=[chunk["metadata"] for chunk in chunks],
    # )
    if not chunks:
        return
    get_collection().upsert(ids=[c["id"] for c in chunks], documents=[c["content"] for c in chunks],
                            embeddings=[c["embedding"] for c in chunks], metadatas=[c["metadata"] for c in chunks])


def run_pipeline() -> None:
    """Chạy load, chunk, embed và index."""
    documents = load_documents()
    chunks = chunk_documents(documents)
    embedded_chunks = embed_chunks(chunks)
    index_to_vectorstore(embedded_chunks)
    print(f"Indexed {len(embedded_chunks)} chunks")


if __name__ == "__main__":
    run_pipeline()
