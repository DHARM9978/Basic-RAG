import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const uploadPDF = (formData) =>
  API.post("/upload", formData, {
    headers: {
      "Content-Type":
        "multipart/form-data",
    },
  });

export const getDocuments = () =>
  API.get("/documents");

export const deleteDocument = (
  filename
) =>
  API.delete(
    `/documents/${filename}`
  );

export const askQuestion = (
  sessionId,
  question
) =>
  API.post("/query", {
    session_id: sessionId,
    message: question,
  });

export const askQuestionStream =
  async (
    sessionId,
    question,
    onChunk
  ) => {

    const response =
      await fetch(
        "http://localhost:8000/query-stream",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            session_id:
              sessionId,
            message:
              question,
          }),
        }
      );

    if (!response.ok) {
      throw new Error(
        "Streaming request failed"
      );
    }

    const reader =
      response.body.getReader();

    const decoder =
      new TextDecoder();

    let fullText = "";

    while (true) {

      const {
        done,
        value,
      } =
        await reader.read();

      if (done) break;

      const chunk =
        decoder.decode(
          value,
          {
            stream: true,
          }
        );

      fullText += chunk;

      onChunk(fullText);
    }

    return fullText;
  };

export default API;