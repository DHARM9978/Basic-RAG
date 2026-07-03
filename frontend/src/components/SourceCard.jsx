function SourceCard({ sources }) {
  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <div className="source-card">
      <h4>Sources</h4>

      {sources.map((source, index) => (
        <div
          key={index}
          className="source-item"
        >
          📄 {source.source}
          {" "}
          (Page {source.page})
        </div>
      ))}
    </div>
  );
}

export default SourceCard;