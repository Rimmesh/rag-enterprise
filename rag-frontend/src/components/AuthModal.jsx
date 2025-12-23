import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import { AuthContext } from "../auth/AuthContext";
import "../styles/auth-modal.css";

export default function AuthModal({ mode, onClose }) {
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const isLogin = mode === "login";

  const submit = async () => {
    setError("");

    if (!email || !password) {
      setError("Please fill all fields");
      return;
    }

    try {
      setLoading(true);

      if (!isLogin) {
        // Register first
        await api.post("/auth/register", { email, password });
      }

      // Always login to get token
      const res = await api.post("/auth/login", { email, password });

      // ✅ Update AuthContext (this is what stops the /chat → / glitch)
      login(res.data.access_token);

      onClose();
      navigate("/chat");
    } catch (err) {
      setError(err.response?.data?.detail || "Authentication failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-overlay" onClick={onClose}>
      <div className="auth-modal" onClick={(e) => e.stopPropagation()}>
        <button className="auth-close" onClick={onClose}>
          ×
        </button>

        <h2>{isLogin ? "Sign In" : "Register"}</h2>

        {error && <div className="auth-error">{error}</div>}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          autoComplete="email"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete={isLogin ? "current-password" : "new-password"}
        />

        <button className="auth-submit" onClick={submit} disabled={loading}>
          {loading ? "Please wait..." : isLogin ? "Sign In" : "Create account"}
        </button>
      </div>
    </div>
  );
}
