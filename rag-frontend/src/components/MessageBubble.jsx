export default function MessageBubble({ role, text }) {
  return (
    <div className={`msg-row ${role === "user" ? "msg-right" : "msg-left"}`}>
      <div className={role === "user" ? "bubble-user" : "bubble-ai"}>
        {text}
      </div>
    </div>
  );
}
