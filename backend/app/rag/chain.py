from app.rag.llm import llm
from app.rag.retriever import get_relevant_docs
from app.rag.memory import (
    get_history,
    add_message
)
from app.rag.query_rewriter import (
    rewrite_question
)


def ask_question(
    question: str,
    session_id: str
):

    # -----------------------------
    # Conversation History
    # -----------------------------
    history = get_history(session_id)

    recent_history = history[-4:]

    history_text = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in recent_history
        ]
    )

    # -----------------------------
    # Rewrite Follow-up Question
    # -----------------------------
    standalone_question = rewrite_question(
        question,
        history_text
    )

    # For Debugging purpose only

    # print("\n==============================")
    # print("ORIGINAL QUESTION:")
    # print(question)

    # print("\nREWRITTEN QUESTION:")
    # print(standalone_question)

    # -----------------------------
    # Retrieve Documents
    # -----------------------------
    docs = get_relevant_docs(
        standalone_question
    )

    # FOR DEBUGGING PURPOSE ONLY

    # print("\nRETRIEVED DOCUMENTS:")

    # for i, doc in enumerate(
    #     docs,
    #     start=1
    # ):
    #     print(
    #         f"{i}. "
    #         f"Source={doc.metadata.get('source')} "
    #         f"Page={doc.metadata.get('page')}"
    #     )

    # print(
    #     "\nRetrieved Docs Count:",
    #     len(docs)
    # )

    # -----------------------------
    # Build Context
    # -----------------------------
    context = "\n\n".join(
        [
            f"[Page {doc.metadata.get('page', 'Unknown')}]\n"
            f"{doc.page_content}"
            for doc in docs
        ]
    )

    # -----------------------------
    # Prompt
    # -----------------------------
    prompt = f"""
You are a helpful AI assistant.

Conversation History:
{history_text}

Context:
{context}

Current Question:
{standalone_question}

Rules:

1. Use conversation history only to resolve references such as:
   - it
   - they
   - this
   - that

2. Do NOT mention conversation history.

3. Do NOT say:
   - According to the conversation history
   - Based on previous messages
   - From the context above

4. Answer directly and concisely.

5. Use only information from the provided context.

6. If the answer is not found, say:
   "I could not find that information in the document."

Answer:
"""

    # -----------------------------
    # Generate Answer
    # -----------------------------
    response = llm.invoke(prompt)

    # -----------------------------
    # Save Chat History
    # -----------------------------
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

    # -----------------------------
    # Remove Duplicate Sources
    # -----------------------------
    unique_sources = []
    seen = set()

    for doc in docs:

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        key = (source, page)

        if key not in seen:

            seen.add(key)

            unique_sources.append(
                {
                    "source": source,
                    "page": page,
                    "preview": (
                        doc.page_content[:150]
                    )
                }
            )

    # Debugging purpose only

    # print("\nUNIQUE SOURCES:")

    # for source in unique_sources:
    #     print(
    #         source["source"],
    #         "| Page:",
    #         source["page"]
    #     )

    # print("==============================\n")

    # -----------------------------
    # API Response
    # -----------------------------
    return {
        "answer": response.content,
        "sources": unique_sources
    }