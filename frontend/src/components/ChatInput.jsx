import { Send } from "lucide-react";
import { useState } from "react";
import { askQuestionStream } from "../api/api";

function ChatInput({
  messages,
  setMessages,
}) {
  const sessionId = "user-session-1";

  const [question, setQuestion] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const handleSend = async () => {
    if (
      !question.trim() ||
      loading
    ) {
      return;
    }

    const currentQuestion =
      question;

    const userMessage = {
      role: "user",
      content: currentQuestion,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
      {
        role: "assistant",
        content: "",
        sources: [],
      },
    ]);

    setQuestion("");

    try {
      setLoading(true);

      await askQuestionStream(
        sessionId,
        currentQuestion,
        (partialText) => {
          setMessages((prev) => {
            const updated = [...prev];

            updated[
              updated.length - 1
            ] = {
              ...updated[
                updated.length - 1
              ],
              content:
                partialText,
            };

            return updated;
          });
        }
      );
    } catch (error) {
      console.error(error);

      setMessages((prev) => {
        const updated = [...prev];

        updated[
          updated.length - 1
        ] = {
          role: "assistant",
          content:
            "❌ Error communicating with server.",
          sources: [],
        };

        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (
    e
  ) => {
    if (
      e.key === "Enter" &&
      !e.shiftKey
    ) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-input">
      <input
        type="text"
        value={question}
        placeholder="Ask something about your document..."
        onChange={(e) =>
          setQuestion(
            e.target.value
          )
        }
        onKeyDown={
          handleKeyDown
        }
        disabled={loading}
      />

      <button
        onClick={handleSend}
        disabled={
          loading ||
          !question.trim()
        }
      >
        {loading ? (
          "..."
        ) : (
          <Send size={20} />
        )}
      </button>
    </div>
  );
}

export default ChatInput;