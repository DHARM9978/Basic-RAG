import UploadBox from "./UploadBox";
import DocumentsList from "./DocumentsList";

function Sidebar({
  documents,
  setDocuments,
}) {
  return (
    <aside className="sidebar">
      <UploadBox
        documents={documents}
        setDocuments={setDocuments}
      />

      <div>
        <DocumentsList
          documents={documents}
          setDocuments={setDocuments}
        />
      </div>
    </aside>
  );
}

export default Sidebar;