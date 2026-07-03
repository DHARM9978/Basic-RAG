from langchain_chroma import Chroma

from app.rag.embeddings import (
    embedding_model
)

from app.rag.bm25 import (
    bm25_search
)

VECTOR_DB_PATH = "vectorstore"

vectorstore = Chroma(
    persist_directory=VECTOR_DB_PATH,
    embedding_function=embedding_model
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)


def merge_results(
    vector_docs,
    bm25_docs
):

    merged = []
    seen = set()

    for doc in vector_docs + bm25_docs:

        key = (
            doc.metadata.get("source"),
            doc.metadata.get("page"),
            doc.page_content[:100]
        )

        if key not in seen:

            seen.add(key)

            merged.append(doc)

    return merged


def get_relevant_docs(
    question: str
):

    vector_docs = retriever.invoke(
        question
    )

    print(
        "\n=== VECTOR SEARCH RESULTS ==="
    )

    for doc in vector_docs:

        print(
            doc.metadata.get(
                "source"
            ),
            "| Page:",
            doc.metadata.get(
                "page"
            )
        )

    bm25_docs = bm25_search(
        question
    )

    print(
        "\n=== BM25 SEARCH RESULTS ==="
    )

    for doc in bm25_docs:

        print(
            doc.metadata.get(
                "source"
            ),
            "| Page:",
            doc.metadata.get(
                "page"
            )
        )

    merged_docs = merge_results(
        vector_docs,
        bm25_docs
    )

    print(
        "\n=== HYBRID RESULTS ==="
    )

    for doc in merged_docs:

        print(
            doc.metadata.get(
                "source"
            ),
            "| Page:",
            doc.metadata.get(
                "page"
            )
        )

    return merged_docs