import { useState } from "react";
import { issueAPI } from "../../services/api";

export default function IssueReturnModal({ bookId, onClose }) {
  const [memberId, setMemberId] = useState("");

  const issueBook = async () => {
    await issueAPI.issue({ book_id: bookId, member_id: memberId });
    onClose();
  };

  const returnBook = async () => {
    await issueAPI.return({ book_id: bookId, member_id: memberId });
    onClose();
  };

  return (
    <div style={{ background: "#fff", padding: 20 }}>
      <h3>Issue / Return Book</h3>
      <input placeholder="Member ID" value={memberId} onChange={e => setMemberId(e.target.value)} />
      <button onClick={issueBook}>Issue</button>
      <button onClick={returnBook}>Return</button>
      <button onClick={onClose}>Close</button>
    </div>
  );
}
