import { useContext, useEffect, useMemo, useState } from "react";
import { AuthContext } from "../auth/AuthContext";
import Sidebar from "../components/Sidebar";
import ChatShell from "../components/ChatShell";
import api from "../api/api";
import { useNavigate } from "react-router-dom";

export default function Chat() {
  const { user, loading } = useContext(AuthContext);
  const navigate = useNavigate();

  // ✅ Per-user storage keys (prevents shared history between accounts)
  const storage = useMemo(() => {
    const email = user?.email || "guest";
    return {
      convKey: `conversations:${email}`,
      currentKey: `currentChatId:${email}`,
    };
  }, [user?.email]);

  const [conversations, setConversations] = useState({});
  const [currentId, setCurrentId] = useState(null);

  // ✅ Load conversations when user becomes available
  useEffect(() => {
    if (!user?.email) return;

    const saved = localStorage.getItem(storage.convKey);
    const savedId = localStorage.getItem(storage.currentKey);

    const parsed = saved ? JSON.parse(saved) : {};
    setConversations(parsed);
    setCurrentId(savedId || null);
  }, [user?.email, storage.convKey, storage.currentKey]);

  // ✅ Persist per-user
  useEffect(() => {
    if (!user?.email) return;
    localStorage.setItem(storage.convKey, JSON.stringify(conversations));
    if (currentId) localStorage.setItem(storage.currentKey, currentId);
  }, [conversations, currentId, user?.email, storage.convKey, storage.currentKey]);

  // ✅ Auth guard
  useEffect(() => {
    if (!loading && !user) navigate("/");
  }, [loading, user, navigate]);

  // ✅ Create new chat
  const newChat = () => {
    const id = "c_" + Date.now();
    setConversations((prev) => ({
      ...prev,
      [id]: { id, title: "New chat", messages: [], createdAt: Date.now() },
    }));
    setCurrentId(id);
  };

  // ✅ Ensure at least one chat exists
  useEffect(() => {
    if (loading) return;
    if (!user) return;

    const hasCurrent = currentId && conversations[currentId];
    const any = Object.keys(conversations).length > 0;

    if (!hasCurrent) {
      if (!any) newChat();
      else setCurrentId(Object.keys(conversations)[0]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loading, user]);

  const deleteChat = (id) => {
    setConversations((prev) => {
      const updated = { ...prev };
      delete updated[id];

      const ids = Object.keys(updated);
      setCurrentId(ids[0] || null);
      return updated;
    });
  };

  const currentConv = currentId ? conversations[currentId] : null;

  const ask = async (question) => {
    if (!currentId) return;

    // push user message
    setConversations((prev) => {
      const updated = { ...prev };
      const conv = { ...(updated[currentId] || {}) };
      const messages = [...(conv.messages || []), { role: "user", content: question }];

      if (messages.length === 1) {
        conv.title = question.split(" ").slice(0, 6).join(" ") + "…";
      }

      conv.messages = messages;
      updated[currentId] = conv;
      return updated;
    });

    try {
      const r = await api.post("/ask", { question });

      setConversations((prev) => {
        const updated = { ...prev };
        const conv = { ...(updated[currentId] || {}) };

        conv.messages = [
          ...(conv.messages || []),
          { role: "assistant", content: r.data.answer },
        ];

        updated[currentId] = conv;
        return updated;
      });
    } catch {
      setConversations((prev) => {
        const updated = { ...prev };
        const conv = { ...(updated[currentId] || {}) };

        conv.messages = [
          ...(conv.messages || []),
          { role: "assistant", content: "⚠️ Backend error. Please try again." },
        ];

        updated[currentId] = conv;
        return updated;
      });
    }
  };

  // ✅ UI loading
  if (loading) {
    return (
      <div
        style={{
          height: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "white",
          fontSize: 18,
          opacity: 0.75,
        }}
      >
        Loading your workspace…
      </div>
    );
  }

  if (!user) return null;

  return (
    <div className="layout">
      <Sidebar
        conversations={conversations}
        currentId={currentId}
        onNewChat={newChat}
        onSelectChat={setCurrentId}
        onDeleteChat={deleteChat}
        user={user}
      />

      <ChatShell messages={currentConv?.messages || []} onSend={ask} />
    </div>
  );
}
