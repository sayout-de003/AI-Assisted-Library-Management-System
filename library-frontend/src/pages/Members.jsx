import { useEffect, useState } from "react";
import { membersAPI } from "../services/api";
import Header from "../components/Header";

export default function Members() {
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchMembers = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await membersAPI.list();
      // Handle paginated response
      setMembers(res.data.results || res.data || []);
    } catch (err) {
      console.error("Error fetching members:", err);
      setError(err.message || "Failed to fetch members. Please try again.");
      setMembers([]);
    } finally {
      setLoading(false);
    }
  };

  // Note: Toggle functionality removed as endpoint doesn't exist in backend
  // const toggleApproval = async (id) => {
  //   try {
  //     await membersAPI.toggleApproval(id);
  //     fetchMembers();
  //   } catch (err) {
  //     console.error("Error toggling approval:", err);
  //     alert(err.message || "Failed to toggle approval. Please try again.");
  //   }
  // };

  useEffect(() => {
    fetchMembers();
  }, []);

  return (
    <div>
      <Header />
      <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "0 1rem" }}>
        <h2>Members</h2>
        
        {error && (
          <div style={{ color: "red", marginBottom: "1rem", padding: "1rem", backgroundColor: "#fee", borderRadius: "4px" }}>
            {error}
          </div>
        )}

        {loading ? (
          <p>Loading members...</p>
        ) : members.length > 0 ? (
          <div>
            {members.map(m => (
              <div key={m.id} style={{ marginBottom: "0.5rem", padding: "0.5rem", border: "1px solid #ddd", borderRadius: "4px" }}>
                <div>
                  <strong>{m.name}</strong> - {m.email}
                </div>
                <div style={{ fontSize: "0.9rem", color: "#666", marginTop: "0.25rem" }}>
                  Membership ID: {m.membership_id} | Status: {m.is_active ? "Active" : "Inactive"}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>No members found.</p>
        )}
      </div>
    </div>
  );
}
