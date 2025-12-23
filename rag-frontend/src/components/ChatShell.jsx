import { useEffect, useRef, useState } from "react";
import MessageBubble from "./MessageBubble";

export default function ChatShell({ messages, onSend }) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const send = async () => {
    if (!input.trim() || loading) return;

    const question = input;
    setInput("");
    setLoading(true);

    await onSend(question);

    setLoading(false);
  };

  return (
    <div className="chat-wrapper">
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="bubble-ai intro">
            👋 Welcome to Enterprise RAG Assistant.  
            Ask questions about your documents, reports, or policies.
          </div>
        )}

        {messages.map((m, i) => (
          <MessageBubble key={i} role={m.role} text={m.content} />
        ))}

        {loading && (
          <div className="msg-row msg-left">
            <div className="bubble-ai thinking">
              Thinking<span className="dots">...</span>
            </div>
          </div>
        )}

        <div ref={endRef} />
      </div>

      <div className="chat-input-bar">
        <input
          placeholder="Ask about your documents..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
        />
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}
