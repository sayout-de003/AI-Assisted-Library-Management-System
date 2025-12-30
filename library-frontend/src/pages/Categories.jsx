import { useEffect, useState } from "react";
import { categoriesAPI } from "../services/api";
import Header from "../components/Header";

export default function Categories() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        setError(null);
        const res = await categoriesAPI.list();
        // Handle paginated response
        setCategories(res.data.results || res.data || []);
      } catch (err) {
        console.error("Error fetching categories:", err);
        setError(err.message || "Failed to fetch categories. Please try again.");
        setCategories([]);
      } finally {
        setLoading(false);
      }
    };
    
    fetchCategories();
  }, []);

  return (
    <div>
      <Header />
      <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "0 1rem" }}>
        <h2>Categories</h2>
        
        {error && (
          <div style={{ color: "red", marginBottom: "1rem", padding: "1rem", backgroundColor: "#fee", borderRadius: "4px" }}>
            {error}
          </div>
        )}

        {loading ? (
          <p>Loading categories...</p>
        ) : categories.length > 0 ? (
          <div>
            {categories.map(c => (
              <div key={c.id} style={{ marginBottom: "0.5rem", padding: "0.5rem", border: "1px solid #ddd", borderRadius: "4px" }}>
                <strong>{c.name}</strong>
              </div>
            ))}
          </div>
        ) : (
          <p>No categories found.</p>
        )}
      </div>
    </div>
  );
}
