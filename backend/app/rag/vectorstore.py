from langchain_chroma import Chroma

from app.rag.embeddings import (
    embedding_model
)

VECTOR_DB_PATH = "vectorstore"


def get_vectorstore():

    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embedding_model
    )