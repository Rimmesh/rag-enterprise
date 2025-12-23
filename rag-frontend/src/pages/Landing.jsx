import { useState } from "react";
import AuthModal from "../components/AuthModal";
import "../styles/landing.css";

export default function Landing() {
  const [authMode, setAuthMode] = useState(null); // "login" | "register" | null

  return (
    <div className="landing-root">
      {/* Animated background */}
      <div className="bg-orbs">
        <span />
        <span />
        <span />
      </div>

      <main className="landing-content">
        <h1 className="landing-title">
          Enterprise <span>RAG</span> Assistant
        </h1>

        <p className="landing-subtitle">
          Secure. Context-aware. Built on your knowledge — not the internet.
        </p>

        <div className="landing-actions">
          <button
            className="btn-primary"
            onClick={() => setAuthMode("login")}
          >
            Sign In
          </button>

          <button
            className="btn-secondary"
            onClick={() => setAuthMode("register")}
          >
            Register
          </button>
        </div>

        <div className="landing-features">
          <div className="feature">🔐 Private knowledge only</div>
          <div className="feature">📄 PDF, DOCX, PPT ingestion</div>
          <div className="feature">🧠 FAISS + LLM reasoning</div>
          <div className="feature">⚡ Instant semantic search</div>
        </div>
      </main>

      <footer className="landing-footer">
        Built for internal intelligence · Zero hallucinations · Full control
      </footer>

      {/* 🔮 Glass Auth Modal */}
      {authMode && (
        <AuthModal
          mode={authMode}
          onClose={() => setAuthMode(null)}
        />
      )}
    </div>
  );
}
