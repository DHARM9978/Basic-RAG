import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";

function ChatWindow({ messages }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  return (
    <div className="chat-window">
      {messages.length === 0 ? (
        <div className="empty-chat">
          <h2>🤖 RAG Assistant</h2>

          <p>
            Upload a PDF and start asking
            questions.
          </p>

          <div className="suggestions">
            <div className="suggestion-card">
              What is this document about?
            </div>

            <div className="suggestion-card">
              Summarize the uploaded PDF
            </div>

            <div className="suggestion-card">
              Give me key insights
            </div>

            <div className="suggestion-card">
              Extract important points
            </div>
          </div>
        </div>
      ) : (
        <>
          {messages.map(
            (message, index) => (
              <MessageBubble
                key={index}
                role={message.role}
                content={message.content}
                sources={message.sources}
              />
            )
          )}

          <div ref={bottomRef}></div>
        </>
      )}
    </div>
  );
}

export default ChatWindow;