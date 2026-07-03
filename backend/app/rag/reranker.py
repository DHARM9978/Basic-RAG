from sentence_transformers import CrossEncoder


# Load once when application starts
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_documents(
    query,
    docs,
    top_k=5
):
    """
    Re-rank retrieved documents based on relevance.
    """

    if not docs:
        return []

    pairs = [
        (query, doc.page_content)
        for doc in docs
    ]

    scores = reranker.predict(pairs)

    ranked_docs = sorted(
        zip(docs, scores),
        key=lambda x: x[1],
        reverse=True
    )

    # For Debugging Purpose

    # print("\n=== RERANKER SCORES ===")

    # for doc, score in ranked_docs:
    #     print(
    #         f"{score:.4f} | "
    #         f"{doc.metadata.get('source')} | "
    #         f"Page {doc.metadata.get('page')}"
    #     )

    return [
        doc
        for doc, score in ranked_docs[:top_k]
    ]