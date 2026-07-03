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


def get_relevant_docs(question):

    vector_docs = retriever.invoke(question)

    # bm25_docs = bm25_search(question)

    # combined = merge_results(
    #     vector_docs,
    #     bm25_docs
    # )

    # return combined
    return retriever.invoke(question)