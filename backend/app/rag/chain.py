from app.rag.llm import llm
from app.rag.retriever import get_relevant_docs
from app.rag.memory import (
    get_history,
    add_message
)
from app.rag.query_rewriter import (
    rewrite_question
)


def prepare_rag_data(
    question: str,
    session_id: str
):
    """
    Shared retrieval pipeline used by both
    normal and streaming responses.
    """

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
    # Rewrite Question
    # -----------------------------
    standalone_question = rewrite_question(
        question,
        history_text
    )

    # -----------------------------
    # Retrieve Documents
    # -----------------------------
    docs = get_relevant_docs(
        standalone_question
    )

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

1. Use conversation history only to resolve references.

2. Do NOT mention conversation history.

3. Do NOT say:
   - According to conversation history
   - Based on previous messages

4. Answer directly.

5. Use only information from context.

6. If answer is unavailable, say:
   "I could not find that information in the document."

Answer:
"""

    # -----------------------------
    # Unique Sources
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

    return {
        "prompt": prompt,
        "sources": unique_sources,
        "question": question
    }


# =====================================
# Normal Response
# =====================================

def ask_question(
    question: str,
    session_id: str
):

    rag_data = prepare_rag_data(
        question,
        session_id
    )

    response = llm.invoke(
        rag_data["prompt"]
    )

    # Save Memory

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
        "sources": rag_data["sources"]
    }


# =====================================
# Streaming Response
# =====================================

def stream_question(
    question: str,
    session_id: str
):

    rag_data = prepare_rag_data(
        question,
        session_id
    )

    full_answer = ""

    for chunk in llm.stream(
        rag_data["prompt"]
    ):

        if chunk.content:

            full_answer += chunk.content

            yield chunk.content

    # Save Memory After Streaming Completes

    add_message(
        session_id,
        "user",
        question
    )

    add_message(
        session_id,
        "assistant",
        full_answer
    )