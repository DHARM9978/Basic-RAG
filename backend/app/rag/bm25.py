from rank_bm25 import BM25Okapi
from langchain_core.documents import Document
from app.rag.vectorstore import get_vectorstore


def bm25_search(
    query: str,
    top_k: int = 5
):

    vectorstore = get_vectorstore()

    data = vectorstore.get()

    documents = data["documents"]
    metadatas = data["metadatas"]

    if not documents:
        return []

    tokenized_docs = [
        doc.lower().split()
        for doc in documents
    ]

    bm25 = BM25Okapi(
        tokenized_docs
    )

    scores = bm25.get_scores(
        query.lower().split()
    )

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]

    results = []

    for idx in ranked_indices:

        results.append(
            Document(
                page_content=documents[idx],
                metadata=metadatas[idx]
            )
        )

    return results