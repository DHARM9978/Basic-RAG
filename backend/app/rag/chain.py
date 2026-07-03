from app.rag.llm import llm
from app.rag.retriever import get_relevant_docs
from app.rag.memory import (get_history,add_message)
from app.rag.query_rewriter import rewrite_question


def ask_question(question: str,session_id: str):


    # Get previous conversation
    history = get_history(session_id)

    # Convert history into text
    recent_history = history[-4:]

    history_text = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in recent_history
        ]
    )

    standalone_question = rewrite_question(
    question,
    history_text
    )

    print("\nORIGINAL QUESTION:")
    print(question)

    print("\nREWRITTEN QUESTION:")
    print(standalone_question)



    # Retrieve relevant documents
    docs = get_relevant_docs(standalone_question)

    print("\nQUESTION:", question)
    print("Retrieved Docs Count:", len(docs))


    # Combine retrieved chunks into context
    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Create prompt
    prompt = f"""
        You are a helpful AI assistant.

        Conversation History:
        {history_text}

        Context:
        {context}

        Current Question:
        {standalone_question}

        Rules:
        1. Use conversation history only to understand references such as:
        - it
        - they
        - this
        - that

        2. Do NOT mention conversation history in your answer.

        3. Do NOT say:
        - "According to the conversation history"
        - "Based on previous messages"
        - "From the context above"

        4. Answer directly and concisely.

        5. Use only information from the provided context.

        6. If the answer is not found, say:
        "I could not find that information in the document."

        Answer:
        """

    response = llm.invoke(prompt)

    add_message(
        session_id,
        "user",
        question
    )

    add_message(
        session_id,
        "assistant",
        response.content
    )



    return {
    "answer": response.content,
    "sources": [
        {
            "source": doc.metadata.get("source"),
            "page": doc.metadata.get("page"),
            "preview": doc.page_content[:200]
        }
        for doc in docs
    ]
}