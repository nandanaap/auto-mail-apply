import { useEffect, useState } from "react";
import { getCompanies, uploadResume, sendToCompany, getLogs, getResume } from "./api";

export default function App() {
  const [companies, setCompanies] = useState([]);
  const [logs, setLogs] = useState([]);
  const [uploadMsg, setUploadMsg] = useState("");
  const [sendingId, setSendingId] = useState(null);
  const [resumeUrl, setResumeUrl] = useState(null);

  // simple auth state
  const [user, setUser] = useState(null);

  async function load() {
    const [c, l] = await Promise.all([getCompanies(), getLogs()]);
    setCompanies(c);
    setLogs(l);
  }

  useEffect(() => {
    load();
  }, []);

  async function handleUpload(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    const res = await uploadResume(file);
    setUploadMsg(res.ok ? "Resume uploaded ✅" : res.error || "Upload failed");
    if (res.ok) {
      setResumeUrl(`${import.meta.env.VITE_API_URL}${res.url}`);
    }
  }

  async function handleSend(id) {
    setSendingId(id);
    const res = await sendToCompany(id);
    await load();
    setSendingId(null);
    alert(res.status === "SENT" ? "Sent ✅" : `Failed ❌\n${res.error || ""}`);
  }

  function handleLogin() {
    // fake login (replace with real auth later)
    setUser({ name: "Nandana" });
  }

  function handleLogout() {
    setUser(null);
  }

  return (
    <div
      style={{
        maxWidth: 1100,
        margin: "40px auto",
        fontFamily: "Inter, system-ui, sans-serif",
        padding: "20px",
        background: "#f2e7f3ff",
        borderRadius: "12px",
        boxShadow: "0 2px 10px rgba(0,0,0,0.05)",
      }}
    >
      {/* NAVBAR */}
      <nav
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "10px 20px",
          background: "#4c2a65",
          color: "white",
          borderRadius: "8px",
          marginBottom: "20px",
        }}
      >
        <h2 style={{ margin: 0 }}>Auto Mailer</h2>
        <div>
          {user ? (
            <>
              <span style={{ marginRight: "15px" }}>Hello, {user.name}</span>
              <button
                onClick={handleLogout}
                style={{
                  padding: "6px 14px",
                  border: "none",
                  borderRadius: 6,
                  background: "#ff4d4f",
                  color: "white",
                  cursor: "pointer",
                }}
              >
                Logout
              </button>
            </>
          ) : (
            <button
              onClick={handleLogin}
              style={{
                padding: "6px 14px",
                border: "none",
                borderRadius: 6,
                background: "#28a745",
                color: "white",
                cursor: "pointer",
              }}
            >
              Login
            </button>
          )}
        </div>
      </nav>

      {/* Upload Resume Section */}
      <section
        style={{
          margin: "20px 0",
          padding: 20,
          border: "1px solid #756f77ff",
          borderRadius: 12,
          background: "#fff",
          boxShadow: "0 1px 4px rgba(0,0,0,0.05)",
        }}
      >
        <h3 style={{ marginBottom: 10, textAlign: "center" }}> Upload Resume </h3>
        <input
          type="file"
          accept="application/pdf"
          onChange={handleUpload}
          style={{
            margin: "20px 0",
            padding: 20,
            border: "1px solid #ddd",
            borderRadius: 12,
            background: "#fff",
            boxShadow: "0 1px 4px rgba(0,0,0,0.05)",
          }}
        />
        <div
          style={{
            marginTop: 8,
            fontSize: 14,
            color: uploadMsg.includes("✅") ? "green" : "crimson",
          }}
        >
          {uploadMsg}
        </div>

        {/* PDF Preview */}
        {resumeUrl && (
          <div style={{ marginTop: 20 }}>
            <h4>Stored Resume Preview:</h4>
            <embed
              src={resumeUrl}
              type="application/pdf"
              width="100%"
              height="400px"
              style={{ border: "1px solid #ccc", borderRadius: "8px" }}
            />
            <p style={{ marginTop: 8 }}>
              <a href={resumeUrl} target="_blank" rel="noopener noreferrer">
                Open in new tab
              </a>
            </p>
          </div>
        )}
      </section>

      {/* Two Column Layout */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "20px",
          marginTop: "20px",
        }}
      >
        {/* Companies Section */}
        <section
          style={{
            padding: 20,
            border: "1px solid #ddd",
            borderRadius: 12,
            background: "#fff",
            boxShadow: "0 1px 4px rgba(0,0,0,0.05)",
          }}
        >
          <h3 style={{ marginBottom: 10, textAlign: "center" }}>Companies</h3>
          {companies.length === 0 && (
            <p style={{ color: "#777" }}>No companies yet. Seed the DB.</p>
          )}
          <ul style={{ listStyle: "none", padding: 10, margin: 0 }}>
            {companies.map((c) => (
              <li
                key={c.id}
                style={{
                  display: "flex",
                  gap: 12,
                  alignItems: "center",
                  padding: "12px 0",
                  borderBottom: "1px solid #eee",
                }}
              >
                <div style={{ flex: 1 }}>
                  <strong style={{ fontSize: 16 }}>{c.name}</strong> —{" "}
                  <span style={{ color: "#555" }}>{c.role || "Role"}</span>
                  <div style={{ fontSize: 14, color: "#777" }}>
                    {c.hr_name || "Hiring Team"} • {c.hr_email}
                  </div>
                </div>
                <button
                  onClick={() => handleSend(c.id)}
                  disabled={sendingId === c.id}
                  style={{
                    padding: "6px 14px",
                    border: "none",
                    borderRadius: 8,
                    background: sendingId === c.id ? "#aaa" : "#007bff",
                    color: "#fff",
                    fontWeight: 500,
                    cursor: sendingId === c.id ? "not-allowed" : "pointer",
                    transition: "background 0.2s",
                  }}
                  onMouseOver={(e) => {
                    if (!sendingId) e.currentTarget.style.background = "#0056b3";
                  }}
                  onMouseOut={(e) => {
                    if (!sendingId) e.currentTarget.style.background = "#007bff";
                  }}
                >
                  {sendingId === c.id ? "Sending…" : "Send Resume"}
                </button>
              </li>
            ))}
          </ul>
        </section>

        {/* Logs Section */}
        <section
          style={{
            background: "#fff",
            padding: 20,
            border: "1px solid #ddd",
            borderRadius: 12,
            boxShadow: "0 1px 4px rgba(0,0,0,0.05)",
          }}
        >
          <h3 style={{ marginBottom: 10, textAlign: "center" }}>Logs</h3>
          <ul style={{ maxHeight: "400px", overflowY: "auto" }}>
            {logs.map((l) => (
              <li
                key={l.id}
                style={{
                  padding: "6px 0",
                  borderBottom: "1px solid #f1f1f1",
                }}
              >
                <strong>{l.company || `#${l.company_id}`}</strong> — {l.status} —{" "}
                <span style={{ color: "#666" }}>
                  {new Date(l.sent_at).toLocaleString()}
                </span>
                {l.error && <div style={{ color: "crimson" }}>{l.error}</div>}
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
}
