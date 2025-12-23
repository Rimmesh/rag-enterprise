import { useContext, useState } from "react";
import { AuthContext } from "../auth/AuthContext";
import api from "../api/api";
import { useNavigate } from "react-router-dom";

export default function Sidebar({
  conversations,
  currentId,
  onNewChat,
  onSelectChat,
  onDeleteChat,
  user,
}) {
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const [uploading, setUploading] = useState(false);
  const [uploadMsg, setUploadMsg] = useState("");

  const upload = async (file) => {
    if (!file) return;

    setUploadMsg("");
    setUploading(true);

    try {
      const form = new FormData();
      form.append("file", file);

      await api.post("/upload", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setUploadMsg("✅ Document indexed successfully");
    } catch (e) {
      setUploadMsg(e.response?.data?.detail || "❌ Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const sorted = Object.values(conversations).sort((a, b) => b.createdAt - a.createdAt);

  return (
    <aside className="gpt-sidebar">
      <div className="sidebar-header">
        <h2>Enterprise RAG</h2>
        <span className="sidebar-sub">Knowledge Assistant</span>
      </div>

      <button className="new-chat-btn" onClick={onNewChat}>
        + New chat
      </button>

      {user?.role === "admin" && (
        <div className="upload-box">
          <label className={`upload-label ${uploading ? "uploading" : ""}`}>
            <span className="upload-icon">{uploading ? "⏳" : "📤"}</span>
            <span>{uploading ? "Indexing..." : "Upload knowledge"}</span>
            <input
              type="file"
              hidden
              accept=".pdf,.txt,.docx,.pptx"
              onChange={(e) => upload(e.target.files?.[0])}
              disabled={uploading}
            />
          </label>

          {uploadMsg && <div className="upload-status">{uploadMsg}</div>}
        </div>
      )}

      <div className="conversation-list">
        {sorted.map((c) => (
          <div key={c.id} className={`conversation-row ${c.id === currentId ? "active" : ""}`}>
            <span className="conversation-title" onClick={() => onSelectChat(c.id)}>
              {c.title}
            </span>

            <span
              className="conversation-delete"
              onClick={() => {
                if (confirm("Delete this conversation?")) onDeleteChat(c.id);
              }}
            >
              🗑
            </span>
          </div>
        ))}
      </div>

      <div className="sidebar-footer">
        <div className="user-info">
          <span>{user?.name || "User"}</span>
          <span className="role">{user?.role}</span>
        </div>

        <button
          className="logout-btn"
          onClick={() => {
            logout();
            navigate("/");
          }}
        >
          Logout
        </button>
      </div>
    </aside>
  );
}
