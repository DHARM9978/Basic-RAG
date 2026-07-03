import { UploadCloud } from "lucide-react";
import { useState } from "react";
import API, { getDocuments } from "../api/api";

function UploadBox({
  documents,
  setDocuments,
}) {
  const [uploading, setUploading] =
    useState(false);

  const [uploadProgress, setUploadProgress] =
    useState(0);

  const [message, setMessage] = useState("");

  const handleUpload = async (e) => {
    const file = e.target.files[0];

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

   try {
    setUploading(true);
    setUploadProgress(0);
    setMessage("");

    await API.post(
      "/upload",
      formData,
      {
        headers: {
          "Content-Type":
            "multipart/form-data",
        },

        onUploadProgress: (
          progressEvent
        ) => {
          const percentCompleted =
            Math.round(
              (progressEvent.loaded *
                100) /
                progressEvent.total
            );

          setUploadProgress(
            percentCompleted
          );
        },
      }
    );

    // Refresh documents from backend
    const response =
      await getDocuments();

    setDocuments(response.data);

    setMessage(
      "✅ File uploaded successfully!"
    );

    setUploadProgress(100);

    setTimeout(() => {
      setUploading(false);
    }, 1000);
  } catch (err) {
    console.error(err);

    setUploading(false);
    setUploadProgress(0);

    setMessage(
      "❌ Failed to upload file."
    );
  }
  };

  return (
    <label className="upload-box">
      <UploadCloud size={50} />

      <h3>
        {uploading
          ? `Uploading ${uploadProgress}%`
          : "Upload PDF"}
      </h3>

      <p>
        {uploading
          ? "Please wait..."
          : "Drag & Drop or Click"}
      </p>

      {uploading && (
        <div
          style={{
            width: "100%",
            marginTop: "15px",
          }}
        >
          <div
            style={{
              width: "100%",
              height: "10px",
              background:
                "#e2e8f0",
              borderRadius: "999px",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${uploadProgress}%`,
                height: "100%",
                background:
                  "#4f46e5",
                transition:
                  "width 0.3s ease",
              }}
            />
          </div>

          <p
            style={{
              marginTop: "8px",
              fontSize: "13px",
              color: "#64748b",
            }}
          >
            {uploadProgress}% Uploaded
          </p>
        </div>
      )}

      {message && (
        <p
          style={{
            marginTop: "10px",
            fontSize: "14px",
            fontWeight: "500",
            color: message.startsWith("✅")
              ? "green"
              : "red",
          }}
        >
          {message}
        </p>
      )}

      <input
        type="file"
        accept=".pdf"
        onChange={handleUpload}
        disabled={uploading}
      />
    </label>
  );
}

export default UploadBox;