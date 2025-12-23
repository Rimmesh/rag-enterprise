import { createContext, useEffect, useMemo, useState } from "react";
import api from "../api/api";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Safe logout (do NOT clear everything)
  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  const login = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken); // ✅ triggers /me fetch
  };

  useEffect(() => {
    let alive = true;

    const fetchMe = async () => {
      setLoading(true);

      if (!token) {
        if (alive) {
          setUser(null);
          setLoading(false);
        }
        return;
      }

      try {
        const res = await api.get("/auth/me");
        if (alive) setUser(res.data); // { email, name, role }
      } catch (e) {
        // Token invalid/expired → log out
        if (alive) {
          logout();
        }
      } finally {
        if (alive) setLoading(false);
      }
    };

    fetchMe();
    return () => {
      alive = false;
    };
  }, [token]);

  const value = useMemo(
    () => ({
      user,
      token,
      loading,
      login,
      logout,
      isAuthenticated: !!token,
    }),
    [user, token, loading]
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
