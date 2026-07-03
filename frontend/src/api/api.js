import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 300000,
  headers: {
    "Content-Type": "application/json",
  },
});


API.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error(
      "API Error:",
      error.response?.data || error.message
    );

    return Promise.reject(error);
  }
);

export default API;


export const uploadPDF = (formData) =>
  API.post("/upload", formData);

export const askQuestion = (
  sessionId,
  question
) =>
  API.post("/query", {
    session_id: sessionId,
    message: question,
  });

export const getDocuments = () =>
  API.get("/documents");

export const deleteDocument = (filename) =>
  API.delete(`/documents/${filename}`);