from langchain_core.documents import Document
from app.rag.vectorstore import get_vectorstore


def ingest_chunks(chunks, filename):

    vectorstore = get_vectorstore()

    documents = [
        Document(
            page_content=chunk["content"],
            metadata={
                "source": filename,
                "page": chunk["page"],
                "chunk_id": idx
            }
        )
        for idx, chunk in enumerate(chunks)
    ]

    vectorstore.add_documents(documents)

    return len(documents)