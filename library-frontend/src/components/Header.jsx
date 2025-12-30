import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Header() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate("/login");
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  const isActive = (path) => {
    return location.pathname === path ? "active" : "";
  };

  if (!user) {
    return null; // Don't show header on login page
  }

  return (
    <header style={styles.header}>
      <div style={styles.container}>
        <div style={styles.logo}>
          <Link to="/books" style={styles.logoLink}>
            📚 Library Management System
          </Link>
        </div>
        
        <nav style={styles.nav}>
          <Link 
            to="/books" 
            style={{ ...styles.navLink, ...(isActive("/books") && styles.activeLink) }}
          >
            Books
          </Link>
          <Link 
            to="/members" 
            style={{ ...styles.navLink, ...(isActive("/members") && styles.activeLink) }}
          >
            Members
          </Link>
          <Link 
            to="/categories" 
            style={{ ...styles.navLink, ...(isActive("/categories") && styles.activeLink) }}
          >
            Categories
          </Link>
        </nav>

        <div style={styles.userSection}>
          <button onClick={handleLogout} style={styles.logoutBtn}>
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}

const styles = {
  header: {
    backgroundColor: "#007bff",
    color: "white",
    padding: "1rem 0",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
    marginBottom: "2rem",
  },
  container: {
    maxWidth: "1200px",
    margin: "0 auto",
    padding: "0 1rem",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    flexWrap: "wrap",
  },
  logo: {
    fontSize: "1.5rem",
    fontWeight: "bold",
  },
  logoLink: {
    color: "white",
    textDecoration: "none",
  },
  nav: {
    display: "flex",
    gap: "1.5rem",
    alignItems: "center",
  },
  navLink: {
    color: "white",
    textDecoration: "none",
    padding: "0.5rem 1rem",
    borderRadius: "4px",
    transition: "background-color 0.3s",
    fontSize: "1rem",
    display: "inline-block",
  },
  activeLink: {
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    fontWeight: "bold",
  },
  userSection: {
    display: "flex",
    alignItems: "center",
    gap: "1rem",
  },
  logoutBtn: {
    backgroundColor: "#dc3545",
    color: "white",
    border: "none",
    padding: "0.5rem 1rem",
    borderRadius: "4px",
    cursor: "pointer",
    fontSize: "1rem",
    transition: "background-color 0.3s",
  },
};

