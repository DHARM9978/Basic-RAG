from langchain_chroma import Chroma
from app.rag.embeddings import embedding_model

VECTOR_DB_PATH = "vectorstore"

vectorstore = Chroma(
    persist_directory=VECTOR_DB_PATH,
    embedding_function=embedding_model
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)


def get_relevant_docs(question: str):
    return retriever.invoke(question)