import { useEffect, useState } from "react";
import { booksAPI, searchAPI } from "../services/api";
import IssueReturnModal from "../components/modals/IssueReturnModal";
import Header from "../components/Header";

export default function Books() {
  const [books, setBooks] = useState([]);
  const [page, setPage] = useState(1);
  const [query, setQuery] = useState("");
  const [modalBookId, setModalBookId] = useState(null);

  // Fetch books for pagination
  useEffect(() => {
    if (!query) {
      booksAPI.list(page)
        .then(res => {
          setBooks(res.data.results || []);
        })
        .catch(err => {
          console.error("Error fetching books:", err);
          alert(err.message || "Failed to fetch books. Please try again.");
        });
    }
  }, [page, query]);

  // Search function
  const handleSearch = async () => {
    if (!query) return;
    try {
      const res = await searchAPI.books(query);
      setBooks(res.data.results || []);
    } catch (err) {
      console.error("Error searching books:", err);
      alert(err.message || "Failed to search books. Please try again.");
    }
  };

  return (
    <div>
      <Header />
      <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "0 1rem" }}>
        <h2>Books</h2>

      {/* Search bar */}
      <div style={{ marginBottom: "1rem" }}>
        <input
          placeholder="Search books..."
          value={query}
          onChange={e => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {/* Book list */}
      {books.length > 0 ? (
        books.map(b => (
          <div key={b.id} style={{ marginBottom: "0.5rem" }}>
            <strong>{b.title}</strong> — {b.author}
            <button
              style={{ marginLeft: "1rem" }}
              onClick={() => setModalBookId(b.id)}
            >
              Issue / Return
            </button>
          </div>
        ))
      ) : (
        <p>No books found.</p>
      )}

      {/* Pagination buttons (hidden when searching) */}
      {!query && (
        <div style={{ marginTop: "1rem" }}>
          <button onClick={() => setPage(p => Math.max(1, p - 1))}>
            Prev
          </button>
          <button onClick={() => setPage(p => p + 1)}>Next</button>
        </div>
      )}

      {/* Issue/Return Modal */}
      {modalBookId && (
        <IssueReturnModal
          bookId={modalBookId}
          onClose={() => setModalBookId(null)}
        />
      )}
      </div>
    </div>
  );
}
