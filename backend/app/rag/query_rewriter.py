from app.rag.llm import llm


def rewrite_question(
    question: str,
    history_text: str
):
    """
    Rewrites follow-up questions into standalone questions.

    Example:
    ----------
    History:
    User: What is FastAPI?

    Question:
    Why is it used?

    Output:
    Why is FastAPI used?
    """

    # Questions that do not need rewriting
    pronouns = [
        " it ",
        " they ",
        " them ",
        " this ",
        " that ",
        " these ",
        " those ",
        " its ",
        " their "
    ]

    question_lower = f" {question.lower()} "

    needs_rewrite = any(
        pronoun in question_lower
        for pronoun in pronouns
    )

    # If question is already complete,
    # return it unchanged
    if not needs_rewrite:
        return question

    prompt = f"""
You are a query rewriting assistant.

Your job is to convert follow-up questions into standalone questions.

IMPORTANT RULES:

1. Rewrite ONLY when required.

2. If the question already makes sense by itself,
   return it unchanged.

3. Preserve the original meaning.

4. Do NOT answer the question.

5. Do NOT explain anything.

6. Return ONLY the rewritten question.

Examples:

Conversation:
User: What is FastAPI?

Question:
Why is it used?

Output:
Why is FastAPI used?


Conversation:
User: Explain RAG.

Question:
What are its advantages?

Output:
What are the advantages of RAG?


Conversation:
User: What is Python?

Question:
What is FastAPI?

Output:
What is FastAPI?


Conversation History:
{history_text}

Current Question:
{question}

Rewritten Question:
"""

    try:

        response = llm.invoke(prompt)

        rewritten_question = (
            response.content.strip()
        )

        if not rewritten_question:
            return question

        return rewritten_question

    except Exception as e:

        print(
            f"Query Rewriter Error: {e}"
        )

        return question