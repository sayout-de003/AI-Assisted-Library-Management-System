import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";

import Login from "./pages/Login";
import Books from "./pages/Books";
import Members from "./pages/Members";
import Categories from "./pages/Categories";

// Private route wrapper
const PrivateRoute = ({ children }) => {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" />;
};

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />

          <Route
            path="/books"
            element={
              <PrivateRoute>
                <Books />
              </PrivateRoute>
            }
          />
          <Route
            path="/members"
            element={
              <PrivateRoute>
                <Members />
              </PrivateRoute>
            }
          />
          <Route
            path="/categories"
            element={
              <PrivateRoute>
                <Categories />
              </PrivateRoute>
            }
          />

          {/* Redirect any unknown route to /books */}
          <Route path="*" element={<Navigate to="/books" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
