import { Send } from "lucide-react";
import { useState } from "react";
import API from "../api/api";



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
    )
      return;

    const currentQuestion =
      question;

    const userMessage = {
      role: "user",
      content: currentQuestion,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
    ]);

    setQuestion("");

    try {
      setLoading(true);

      const response =
        await API.post("/query", {
          session_id: sessionId,
          message: currentQuestion,
        });

      const botMessage = {
        role: "assistant",
        content:
          response.data.answer ||
          "No response received.",
        sources:
          response.data.sources ||
          [],
      };

      setMessages((prev) => [
        ...prev,
        botMessage,
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "❌ Error communicating with server.",
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (
    e
  ) => {
    if (e.key === "Enter") {
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
      />

      <button
        onClick={handleSend}
        disabled={loading}
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