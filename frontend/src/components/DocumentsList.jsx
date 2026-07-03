import { useEffect, useState } from "react";
import { MoreHorizontal } from "lucide-react";
import {
  getDocuments,
  deleteDocument,
} from "../api/api";


function DocumentsList({
  documents,
  setDocuments,
}) {

  const [activeMenu, setActiveMenu] =
  useState(null);


  const loadDocuments = async () => {
    try {
      const response =
        await getDocuments();

      setDocuments(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);



  const handleDelete = async (
    filename
  ) => {
      const confirmDelete =
        window.confirm(
          `Are you sure you want to delete "${filename}" ?`
        );

    if (!confirmDelete) return;

    try {
      await deleteDocument(filename);

      loadDocuments();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="documents-list">

      <h3>
        Documents ({documents.length})
      </h3>

      {documents.length === 0 ? (
        <p className="empty-documents">
          No documents uploaded
        </p>
      ) : (
          documents.map((doc) => (
            <div
              key={doc.filename}
              className="document-item"
            >
              <span className="document-name">
                📄 {doc.filename}
              </span>

              <div className="menu-container">
                <button
                  className="menu-btn"
                  onClick={() =>
                    setActiveMenu(
                      activeMenu === doc.filename
                        ? null
                        : doc.filename
                    )
                  }
                >
                  <MoreHorizontal size={18} />
                </button>

                {activeMenu === doc.filename && (
                  <div className="dropdown-menu">
                    <button
                      className="delete-option"
                      onClick={() =>
                        handleDelete(doc.filename)
                      }
                    >
                      Delete
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))
      )}
    </div>
  );
}

export default DocumentsList;