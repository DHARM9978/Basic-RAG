import SourceCard from "./SourceCard";

function MessageBubble({
  role,
  content,
}) {
  const isUser =
    role === "user";

  return (
    <div
      className={`message-row ${
        isUser
          ? "user-row"
          : "assistant-row"
      }`}
    >
      {!isUser && (
        <div className="avatar ai-avatar">
          🤖
        </div>
      )}

      <div
        className={`message ${
          isUser
            ? "user-message"
            : "ai-message"
        }`}
      >
        <p>{content}</p>

        {!isUser && (
          <SourceCard />
        )}
      </div>

      {isUser && (
        <div className="avatar user-avatar">
          👤
        </div>
      )}
    </div>
  );
}

export default MessageBubble;