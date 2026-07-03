import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [documents, setDocuments] = useState([]);

  return (
    <div className="app">
      <Sidebar
        documents={documents}
        setDocuments={setDocuments}
      />

      <main className="main-content">
        <header className="chat-header">
          <h1>🤖 RAG Assistant</h1>
          <p>
            Ask questions about your uploaded
            documents
          </p>
        </header>

        <ChatWindow messages={messages} />

        <ChatInput
          messages={messages}
          setMessages={setMessages}
        />
      </main>
    </div>
  );
}

export default App;