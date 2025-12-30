import React, { createContext, useContext, useState } from "react";
import { authAPI, managementAPI } from "../services/api";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(
    localStorage.getItem("access_token")
  );

  const login = async (email, password) => {
    const res = await authAPI.login({ email, password });
    localStorage.setItem("access_token", res.data.access);
    localStorage.setItem("refresh_token", res.data.refresh);
    setUser(res.data.access);
  };

  const signup = async (data) => {
    // Signup expects { email, name, password }
    try {
      await authAPI.signup(data);
      // After successful signup, automatically log the user in
      await login(data.email, data.password);
    } catch (error) {
      // Re-throw with a more user-friendly message
      const errorMessage = error.response?.data?.email?.[0] || 
                          error.response?.data?.detail || 
                          error.response?.data?.message ||
                          error.message || 
                          "Signup failed. Please try again.";
      throw new Error(errorMessage);
    }
  };

  const requestManagement = async (requestedRole) => {
    await managementAPI.request({ requested_role: requestedRole });
  };

  const logout = async () => {
    localStorage.clear();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, requestManagement }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
