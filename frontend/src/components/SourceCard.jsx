function SourceCard({
  sources = [],
}) {
  if (sources.length === 0) {
    return null;
  }

  return (
    <div className="source-card">
      <h4>📚 Sources</h4>

      {sources.map(
        (source, index) => (
          <div
            key={index}
            className="source-item"
          >
            📄 Page {source}
          </div>
        )
      )}
    </div>
  );
}

export default SourceCard;