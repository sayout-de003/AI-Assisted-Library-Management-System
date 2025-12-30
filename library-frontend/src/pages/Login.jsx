import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState(""); // for signup
  const [isSignup, setIsSignup] = useState(false);
  const [signupType, setSignupType] = useState("member");
  const [requestedRole, setRequestedRole] = useState("");
  const { login, signup, requestManagement } = useAuth();
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    try {
      if (isSignup) {
        await signup({ name, email, password });
      } else {
        await login(email, password);
      }
      navigate("/books");
    } catch (err) {
      alert(err.message || "Authentication failed");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "2rem auto" }}>
      <form onSubmit={submit}>
        <h2>{isSignup ? "Sign Up" : "Login"}</h2>

        {isSignup && (
          <>
            <input
              placeholder="Full Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />

            <div>
              <label>
                <input
                  type="radio"
                  value="member"
                  checked={signupType === "member"}
                  onChange={(e) => setSignupType(e.target.value)}
                />
                Sign up as Member
              </label>
              <label>
                <input
                  type="radio"
                  value="management_request"
                  checked={signupType === "management_request"}
                  onChange={(e) => setSignupType(e.target.value)}
                />
                Sign up and Request Management Role
              </label>
            </div>

            {signupType === "management_request" && (
              <select
                value={requestedRole}
                onChange={(e) => setRequestedRole(e.target.value)}
              >
                <option value="">Select Role</option>
                <option value="ADMIN">Admin</option>
                <option value="LIBRARIAN">Librarian</option>
              </select>
            )}
          </>
        )}

        <input
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button type="submit">{isSignup ? "Sign Up" : "Login"}</button>
      </form>

      <p style={{ marginTop: "1rem" }}>
        {isSignup ? "Already have an account?" : "Don't have an account?"}{" "}
        <span
          style={{ color: "blue", cursor: "pointer" }}
          onClick={() => setIsSignup(!isSignup)}
        >
          {isSignup ? "Login" : "Sign Up"}
        </span>
      </p>
    </div>
  );
}
