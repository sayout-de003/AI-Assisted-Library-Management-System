import { useEffect, useState } from "react";
import Header from "../components/Header";
import { booksAPI, membersAPI, issueAPI } from "../services/api";

export default function IssueReturn() {
  const [books, setBooks] = useState([]);
  const [members, setMembers] = useState([]);
  const [bookId, setBookId] = useState("");
  const [memberId, setMemberId] = useState("");
  const [issueId, setIssueId] = useState("");

  useEffect(() => {
    Promise.all([booksAPI.list(), membersAPI.list()]).then(
      ([b, m]) => {
        setBooks(b.data.results || b.data);
        setMembers(m.data.results || m.data);
      }
    );
  }, []);

  const issueBook = async () => {
    await issueAPI.issue({ book_id: bookId, member_id: memberId });
    alert("Book issued");
  };

  const returnBook = async () => {
    await issueAPI.return(issueId);
    alert("Book returned");
  };

  return (
    <>
      <Header />
      <div style={styles.box}>
        <h2>Issue Book</h2>

        <select onChange={(e) => setBookId(e.target.value)}>
          <option value="">Select Book</option>
          {books.map(b => (
            <option key={b.id} value={b.id}>{b.title}</option>
          ))}
        </select>

        <select onChange={(e) => setMemberId(e.target.value)}>
          <option value="">Select Member</option>
          {members.map(m => (
            <option key={m.id} value={m.id}>
              {m.name} ({m.member_id})
            </option>
          ))}
        </select>

        <button onClick={issueBook}>Issue</button>

        <hr />

        <h2>Return Book</h2>
        <input
          placeholder="Issue ID"
          value={issueId}
          onChange={(e) => setIssueId(e.target.value)}
        />
        <button onClick={returnBook}>Return</button>
      </div>
    </>
  );
}

const styles = {
  box: { maxWidth: "500px", margin: "2rem auto", padding: "2rem", border: "1px solid #ddd" }
};
