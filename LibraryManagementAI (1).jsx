import { useState, useRef, useEffect } from "react";

const STYLES = `
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body { font-family: 'Inter', sans-serif; }

  :root {
    --sidebar-bg: #0f172a;
    --sidebar-text: #94a3b8;
    --sidebar-active: #1e293b;
    --sidebar-accent: #6366f1;
    --main-bg: #f8fafc;
    --card-bg: #ffffff;
    --border: #e2e8f0;
    --text-primary: #0f172a;
    --text-secondary: #64748b;
    --text-muted: #94a3b8;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --info: #6366f1;
  }

  .app { display: flex; height: 100vh; font-family: 'Inter', sans-serif; }

  /* SIDEBAR */
  .sidebar {
    width: 220px;
    min-width: 220px;
    background: var(--sidebar-bg);
    display: flex;
    flex-direction: column;
    padding: 20px 12px;
    gap: 4px;
  }
  .sidebar-logo {
    padding: 8px 10px 20px;
    border-bottom: 1px solid #1e293b;
    margin-bottom: 8px;
  }
  .sidebar-logo .logo-title {
    font-size: 14px;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: 0.02em;
  }
  .sidebar-logo .logo-sub {
    font-size: 11px;
    color: var(--sidebar-text);
    margin-top: 2px;
  }
  .nav-btn {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 10px;
    border: none;
    border-radius: 8px;
    background: transparent;
    color: var(--sidebar-text);
    font-size: 13px;
    font-weight: 400;
    cursor: pointer;
    text-align: left;
    width: 100%;
    transition: all 0.15s;
  }
  .nav-btn:hover { background: #1e293b; color: #f1f5f9; }
  .nav-btn.active { background: var(--sidebar-active); color: #f1f5f9; font-weight: 500; }
  .nav-btn.active .nav-dot { background: var(--sidebar-accent); }
  .nav-dot { width: 6px; height: 6px; border-radius: 50%; background: transparent; margin-left: auto; flex-shrink: 0; }
  .nav-icon { font-size: 15px; width: 18px; text-align: center; flex-shrink: 0; }
  .sidebar-footer { margin-top: auto; padding-top: 12px; border-top: 1px solid #1e293b; }
  .version-badge { font-size: 11px; color: #475569; padding: 4px 10px; }

  /* MAIN */
  .main { flex: 1; display: flex; flex-direction: column; background: var(--main-bg); overflow: hidden; }

  .topbar {
    background: var(--card-bg);
    border-bottom: 1px solid var(--border);
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
  }
  .topbar-title { font-size: 16px; font-weight: 600; color: var(--text-primary); }
  .topbar-right { display: flex; align-items: center; gap: 10px; }
  .ai-chip {
    display: flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: opacity 0.15s;
  }
  .ai-chip:hover { opacity: 0.9; }
  .ai-dot { width: 6px; height: 6px; border-radius: 50%; background: #a5f3fc; animation: pulse 2s infinite; }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

  .content { flex: 1; overflow-y: auto; padding: 24px; }

  /* CARDS */
  .card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
  }
  .card-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* STATS */
  .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 20px; }
  .stat-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 18px;
  }
  .stat-label { font-size: 12px; color: var(--text-secondary); margin-bottom: 6px; }
  .stat-value { font-size: 22px; font-weight: 700; color: var(--text-primary); }
  .stat-card.info .stat-value { color: var(--info); }
  .stat-card.success .stat-value { color: var(--success); }
  .stat-card.warning .stat-value { color: var(--warning); }
  .stat-card.danger .stat-value { color: var(--danger); }

  /* TABLE */
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { text-align: left; padding: 10px 12px; font-size: 12px; font-weight: 600; color: var(--text-secondary); border-bottom: 1px solid var(--border); background: #f8fafc; }
  td { padding: 11px 12px; border-bottom: 1px solid #f1f5f9; color: var(--text-primary); vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: #f8fafc; }

  /* BADGE */
  .badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; }
  .badge-success { background: #d1fae5; color: #065f46; }
  .badge-warning { background: #fef3c7; color: #92400e; }
  .badge-danger { background: #fee2e2; color: #991b1b; }
  .badge-info { background: #ede9fe; color: #4c1d95; }

  /* BUTTONS */
  .btn { padding: 7px 14px; border-radius: 8px; border: none; cursor: pointer; font-size: 13px; font-weight: 500; transition: all 0.15s; }
  .btn-primary { background: var(--info); color: white; }
  .btn-primary:hover { background: #4f46e5; }
  .btn-sm { padding: 4px 10px; font-size: 12px; }
  .btn-ghost { background: transparent; border: 1px solid var(--border); color: var(--text-secondary); }
  .btn-ghost:hover { background: var(--main-bg); }
  .btn-danger { background: var(--danger); color: white; }

  /* SEARCH BAR */
  .search-bar { display: flex; gap: 10px; margin-bottom: 16px; }
  .search-input {
    flex: 1; padding: 9px 14px; border: 1px solid var(--border);
    border-radius: 8px; font-size: 13px; color: var(--text-primary);
    background: var(--card-bg); outline: none;
    transition: border-color 0.15s;
  }
  .search-input:focus { border-color: var(--info); }

  /* BOOKS GRID */
  .books-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
  .book-card {
    border: 1px solid var(--border); border-radius: 10px; padding: 14px;
    background: var(--card-bg); transition: box-shadow 0.15s;
  }
  .book-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.07); }
  .book-title { font-size: 13px; font-weight: 600; color: var(--text-primary); margin-bottom: 4px; }
  .book-meta { font-size: 12px; color: var(--text-secondary); margin-bottom: 10px; }
  .book-footer { display: flex; align-items: center; justify-content: space-between; }

  /* REPORTS GRID */
  .reports-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
  .report-card {
    border: 1px solid var(--border); border-radius: 10px; padding: 16px;
    background: var(--card-bg); cursor: pointer; transition: all 0.15s;
  }
  .report-card:hover { border-color: var(--info); box-shadow: 0 2px 12px rgba(99,102,241,0.1); }
  .report-icon { font-size: 22px; margin-bottom: 8px; }
  .report-title { font-size: 13px; font-weight: 600; color: var(--text-primary); }
  .report-desc { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }

  /* FINES SUMMARY */
  .fines-summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 20px; }
  .fine-box { border: 1px solid var(--border); border-radius: 10px; padding: 16px; background: var(--card-bg); text-align: center; }
  .fine-box-label { font-size: 12px; color: var(--text-secondary); margin-bottom: 4px; }
  .fine-box-value { font-size: 20px; font-weight: 700; }

  /* SETTINGS */
  .settings-form { display: flex; flex-direction: column; gap: 14px; }
  .form-row { display: flex; flex-direction: column; gap: 5px; }
  .form-label { font-size: 12px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.04em; }
  .form-input {
    padding: 9px 12px; border: 1px solid var(--border); border-radius: 8px;
    font-size: 13px; color: var(--text-primary); outline: none;
    transition: border-color 0.15s;
  }
  .form-input:focus { border-color: var(--info); }
  .form-actions { display: flex; gap: 10px; margin-top: 4px; }

  /* AI PANEL */
  .ai-panel {
    position: fixed; right: 0; top: 0; bottom: 0; width: 380px;
    background: white; border-left: 1px solid var(--border);
    display: flex; flex-direction: column; z-index: 100;
    box-shadow: -4px 0 24px rgba(0,0,0,0.08);
    transform: translateX(100%);
    transition: transform 0.25s ease;
  }
  .ai-panel.open { transform: translateX(0); }
  .ai-panel-header {
    padding: 16px 18px;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
  }
  .ai-panel-title { font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
  .ai-close { background: none; border: none; color: white; cursor: pointer; font-size: 18px; padding: 2px 6px; border-radius: 4px; }
  .ai-close:hover { background: rgba(255,255,255,0.15); }

  .ai-messages { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }

  .msg { display: flex; flex-direction: column; max-width: 85%; }
  .msg.user { align-self: flex-end; }
  .msg.ai { align-self: flex-start; }
  .msg-bubble {
    padding: 10px 14px; border-radius: 12px; font-size: 13px; line-height: 1.55;
  }
  .msg.user .msg-bubble { background: var(--info); color: white; border-bottom-right-radius: 3px; }
  .msg.ai .msg-bubble { background: #f1f5f9; color: var(--text-primary); border-bottom-left-radius: 3px; }
  .msg-time { font-size: 10px; color: var(--text-muted); margin-top: 3px; padding: 0 4px; }
  .msg.user .msg-time { text-align: right; }

  .typing-indicator { display: flex; gap: 4px; align-items: center; padding: 10px 14px; background: #f1f5f9; border-radius: 12px; border-bottom-left-radius: 3px; width: fit-content; }
  .typing-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--text-muted); animation: typing 1.2s infinite; }
  .typing-dot:nth-child(2) { animation-delay: 0.2s; }
  .typing-dot:nth-child(3) { animation-delay: 0.4s; }
  @keyframes typing { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-5px)} }

  .ai-input-area {
    padding: 14px 16px;
    border-top: 1px solid var(--border);
    background: white;
  }
  .ai-suggestions { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }
  .suggestion-chip {
    background: #f1f5f9; border: 1px solid var(--border);
    border-radius: 16px; padding: 4px 10px;
    font-size: 11px; color: var(--text-secondary);
    cursor: pointer; transition: all 0.15s;
  }
  .suggestion-chip:hover { background: #ede9fe; border-color: var(--info); color: var(--info); }

  .ai-input-row { display: flex; gap: 8px; }
  .ai-input {
    flex: 1; padding: 9px 12px; border: 1px solid var(--border);
    border-radius: 8px; font-size: 13px; outline: none; resize: none;
    font-family: 'Inter', sans-serif; color: var(--text-primary);
    transition: border-color 0.15s; max-height: 80px; overflow-y: auto;
  }
  .ai-input:focus { border-color: var(--info); }
  .ai-send {
    background: var(--info); color: white; border: none;
    border-radius: 8px; padding: 9px 14px; cursor: pointer;
    font-size: 16px; transition: background 0.15s; flex-shrink: 0;
  }
  .ai-send:hover { background: #4f46e5; }
  .ai-send:disabled { background: var(--text-muted); cursor: not-allowed; }

  .overlay {
    position: fixed; inset: 0; background: rgba(0,0,0,0.15);
    z-index: 99; opacity: 0; pointer-events: none;
    transition: opacity 0.25s;
  }
  .overlay.show { opacity: 1; pointer-events: all; }
`;

const MENU = [
  { id: "dashboard", icon: "🏠", label: "Dashboard" },
  { id: "books", icon: "📚", label: "Books" },
  { id: "members", icon: "👥", label: "Members" },
  { id: "transactions", icon: "🔄", label: "Transactions" },
  { id: "fines", icon: "⚠️", label: "Fines & Penalties" },
  { id: "reports", icon: "📊", label: "Reports" },
  { id: "settings", icon: "⚙️", label: "Settings" },
];

const STATS = [
  { label: "Total Books", value: "2,450", color: "info" },
  { label: "Active Members", value: "1,823", color: "success" },
  { label: "Books Issued", value: "345", color: "warning" },
  { label: "Pending Fines", value: "₨18,500", color: "danger" },
];

const RECENT_TX = [
  { id: 1, member: "Ali Hassan", book: "Database Systems", action: "Issued", date: "2024-01-10" },
  { id: 2, member: "Fatima Khan", book: "Web Development", action: "Returned", date: "2024-01-09" },
  { id: 3, member: "Ahmed Malik", book: "Data Science 101", action: "Issued", date: "2024-01-09" },
];

const BOOKS = [
  { title: "Database Design", author: "Ramez Elmasri", status: "Available" },
  { title: "Web Development", author: "Jon Duckett", status: "Issued" },
  { title: "Data Science 101", author: "Joel Grus", status: "Available" },
  { title: "System Design", author: "Alex Xu", status: "Available" },
  { title: "Python Guide", author: "Mark Lutz", status: "Issued" },
  { title: "JavaScript", author: "David Flanagan", status: "Available" },
];

const AI_SYSTEM_PROMPT = `You are an intelligent AI assistant for a Library Management System called "Central City Library."

Library Data (as of today):
- Total Books: 2,450
- Active Members: 1,823
- Books Currently Issued: 345
- Pending Fines: ₨18,500
- Recently Issued: Database Systems (Ali Hassan), Data Science 101 (Ahmed Malik)
- Recently Returned: Web Development (Fatima Khan)

Available Books: Database Design, Data Science 101, System Design, JavaScript
Currently Issued Books: Web Development (to Fatima Khan), Python Guide

Members: M001 (Member 1), M002 (Member 2), M003 (Member 3)
Fine breakdown: Late Return - ₨5,000 (Pending), Damaged Book - ₨10,000 (Paid), Lost Book - ₨15,000 (Paid)

Your responsibilities:
- Answer questions about books, members, transactions, fines, and reports
- Suggest books based on interests or categories
- Help with overdue reminders and fine calculations
- Assist with generating report summaries
- Guide librarians through library operations
- Support Urdu and English mixed queries (Hinglish/Roman Urdu is fine)

Keep responses concise, helpful, and professional. Use bullet points for lists. Always be friendly and efficient.`;

function timeStr() {
  return new Date().toLocaleTimeString("en-PK", { hour: "2-digit", minute: "2-digit" });
}

export default function LibraryManagementAI() {
  const [view, setView] = useState("dashboard");
  const [aiOpen, setAiOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "ai",
      text: "Assalam-o-Alaikum! 👋 Main aapka Library AI Assistant hoon. Books, members, fines, ya reports ke baare mein kuch poochna ho toh zaroor poochein!",
      time: timeStr(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const messagesEnd = useRef(null);

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async (text) => {
    const userText = text || input.trim();
    if (!userText || loading) return;
    setInput("");

    const userMsg = { role: "user", text: userText, time: timeStr() };
    setMessages((m) => [...m, userMsg]);
    setLoading(true);

    try {
      const history = messages.map((m) => ({
        role: m.role === "ai" ? "assistant" : "user",
        content: m.text,
      }));
      history.push({ role: "user", content: userText });

      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: AI_SYSTEM_PROMPT,
          messages: history,
        }),
      });

      const data = await res.json();
      const reply = data.content?.map((c) => c.text || "").join("") || "Koi jawab nahi mila.";
      setMessages((m) => [...m, { role: "ai", text: reply, time: timeStr() }]);
    } catch {
      setMessages((m) => [...m, { role: "ai", text: "❌ AI se connection nahi ho saka. Dobara try karein.", time: timeStr() }]);
    } finally {
      setLoading(false);
    }
  };

  const SUGGESTIONS = [
    "Overdue books kaun si hain?",
    "Aaj ki transactions",
    "Pending fines summary",
    "Python books available hain?",
  ];

  // ─── VIEWS ───────────────────────────────────────────────
  const Dashboard = () => (
    <>
      <div className="stats-grid">
        {STATS.map((s) => (
          <div key={s.label} className={`stat-card ${s.color}`}>
            <div className="stat-label">{s.label}</div>
            <div className="stat-value">{s.value}</div>
          </div>
        ))}
      </div>
      <div className="card">
        <div className="card-title">📋 Recent Transactions</div>
        <table>
          <thead><tr><th>Member</th><th>Book Title</th><th>Action</th><th>Date</th></tr></thead>
          <tbody>
            {RECENT_TX.map((t) => (
              <tr key={t.id}>
                <td>{t.member}</td>
                <td>{t.book}</td>
                <td><span className={`badge ${t.action === "Issued" ? "badge-warning" : "badge-success"}`}>{t.action}</span></td>
                <td>{t.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );

  const Books = () => {
    const filtered = BOOKS.filter((b) =>
      b.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      b.author.toLowerCase().includes(searchQuery.toLowerCase())
    );
    return (
      <div className="card">
        <div className="card-title">📚 Books Catalog</div>
        <div className="search-bar">
          <input
            className="search-input"
            placeholder="Book ya author ka naam search karein..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button className="btn btn-primary">Search</button>
        </div>
        <div className="books-grid">
          {filtered.map((b) => (
            <div key={b.title} className="book-card">
              <div className="book-title">{b.title}</div>
              <div className="book-meta">by {b.author}</div>
              <div className="book-footer">
                <span className={`badge ${b.status === "Available" ? "badge-success" : "badge-warning"}`}>{b.status}</span>
                {b.status === "Available" && <button className="btn btn-primary btn-sm">Issue</button>}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const Members = () => (
    <div className="card">
      <div className="card-title" style={{ justifyContent: "space-between" }}>
        <span>👥 Members</span>
        <button className="btn btn-primary btn-sm">+ Add New Member</button>
      </div>
      <table>
        <thead><tr><th>Member ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Action</th></tr></thead>
        <tbody>
          {["M001", "M002", "M003"].map((id, i) => (
            <tr key={id}>
              <td><span className="badge badge-info">{id}</span></td>
              <td>Member {i + 1}</td>
              <td>member{i + 1}@email.com</td>
              <td>+92-300-000000{i}</td>
              <td><button className="btn btn-ghost btn-sm">Edit</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  const Transactions = () => (
    <div className="card">
      <div className="card-title" style={{ justifyContent: "space-between", flexWrap: "wrap", gap: 8 }}>
        <span>🔄 Book Transactions</span>
        <div style={{ display: "flex", gap: 8 }}>
          <button className="btn btn-primary btn-sm">Issue Book</button>
          <button className="btn btn-ghost btn-sm">Return Book</button>
          <button className="btn btn-ghost btn-sm">Renew Book</button>
        </div>
      </div>
      <table>
        <thead><tr><th>Transaction ID</th><th>Member</th><th>Book</th><th>Type</th><th>Date</th></tr></thead>
        <tbody>
          {[1, 2, 3, 4].map((item) => (
            <tr key={item}>
              <td>TXN00{item}</td>
              <td>Member {item}</td>
              <td>Book Title {item}</td>
              <td><span className={`badge ${item % 2 === 0 ? "badge-success" : "badge-warning"}`}>{item % 2 === 0 ? "Return" : "Issue"}</span></td>
              <td>2024-01-{10 - item}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  const Fines = () => (
    <>
      <div className="fines-summary">
        {[["Total Fines", "₨24,500", "#0f172a"], ["Paid", "₨6,000", "#10b981"], ["Pending", "₨18,500", "#ef4444"]].map(([l, v, c]) => (
          <div key={l} className="fine-box">
            <div className="fine-box-label">{l}</div>
            <div className="fine-box-value" style={{ color: c }}>{v}</div>
          </div>
        ))}
      </div>
      <div className="card">
        <div className="card-title">⚠️ Fine Records</div>
        <table>
          <thead><tr><th>Member</th><th>Reason</th><th>Amount</th><th>Status</th></tr></thead>
          <tbody>
            {[["Late Return", "₨5,000", "Pending"], ["Damaged Book", "₨10,000", "Paid"], ["Lost Book", "₨15,000", "Paid"]].map(([r, a, s], i) => (
              <tr key={i}>
                <td>Member {i + 1}</td>
                <td>{r}</td>
                <td>{a}</td>
                <td><span className={`badge ${s === "Pending" ? "badge-danger" : "badge-success"}`}>{s}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );

  const Reports = () => (
    <div className="card">
      <div className="card-title">📊 Reports</div>
      <div className="reports-grid">
        {[
          { title: "Inventory Report", icon: "📄", desc: "Current book inventory" },
          { title: "Member Activity", icon: "👥", desc: "Member usage statistics" },
          { title: "Fine Collection", icon: "💰", desc: "Fine payment details" },
          { title: "Overdue Books", icon: "⏰", desc: "Books exceeding due date" },
          { title: "Monthly Report", icon: "📅", desc: "Monthly activity summary" },
          { title: "Annual Report", icon: "📈", desc: "Yearly performance data" },
        ].map((r) => (
          <div key={r.title} className="report-card">
            <div className="report-icon">{r.icon}</div>
            <div className="report-title">{r.title}</div>
            <div className="report-desc">{r.desc}</div>
            <button
              className="btn btn-primary btn-sm"
              style={{ marginTop: 12 }}
              onClick={() => { setAiOpen(true); sendMessage(`${r.title} generate karo`); }}
            >
              Generate via AI ✨
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  const Settings = () => (
    <div className="card">
      <div className="card-title">⚙️ Settings</div>
      <div className="settings-form">
        {[
          ["Library Name", "Central City Library"],
          ["Email", "library@example.com"],
          ["Phone", "+92-XXX-XXXXXXX"],
          ["Address", "City Center, Main Street"],
        ].map(([label, val]) => (
          <div key={label} className="form-row">
            <label className="form-label">{label}</label>
            <input className="form-input" defaultValue={val} />
          </div>
        ))}
        <div className="form-actions">
          <button className="btn btn-primary">Save Changes</button>
          <button className="btn btn-ghost">Cancel</button>
        </div>
      </div>
    </div>
  );

  const VIEWS = { dashboard: Dashboard, books: Books, members: Members, transactions: Transactions, fines: Fines, reports: Reports, settings: Settings };
  const CurrentView = VIEWS[view] || Dashboard;

  return (
    <>
      <style>{STYLES}</style>
      <div className="app">
        {/* SIDEBAR */}
        <aside className="sidebar">
          <div className="sidebar-logo">
            <div className="logo-title">📖 Library</div>
            <div className="logo-sub">Management System</div>
          </div>
          {MENU.map((item) => (
            <button
              key={item.id}
              className={`nav-btn ${view === item.id ? "active" : ""}`}
              onClick={() => setView(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
              <span className="nav-dot" />
            </button>
          ))}
          <div className="sidebar-footer">
            <div className="version-badge">System v1.0 — AI Enabled</div>
          </div>
        </aside>

        {/* MAIN */}
        <div className="main">
          <div className="topbar">
            <div className="topbar-title">
              {MENU.find((m) => m.id === view)?.icon} {MENU.find((m) => m.id === view)?.label}
            </div>
            <div className="topbar-right">
              <button className="ai-chip" onClick={() => setAiOpen(true)}>
                <span className="ai-dot" />
                AI Assistant
              </button>
            </div>
          </div>
          <div className="content">
            <CurrentView />
          </div>
        </div>

        {/* OVERLAY */}
        <div className={`overlay ${aiOpen ? "show" : ""}`} onClick={() => setAiOpen(false)} />

        {/* AI PANEL */}
        <aside className={`ai-panel ${aiOpen ? "open" : ""}`}>
          <div className="ai-panel-header">
            <div className="ai-panel-title">🤖 Library AI Assistant</div>
            <button className="ai-close" onClick={() => setAiOpen(false)}>✕</button>
          </div>

          <div className="ai-messages">
            {messages.map((msg, i) => (
              <div key={i} className={`msg ${msg.role}`}>
                <div className="msg-bubble">{msg.text}</div>
                <div className="msg-time">{msg.time}</div>
              </div>
            ))}
            {loading && (
              <div className="msg ai">
                <div className="typing-indicator">
                  <div className="typing-dot" />
                  <div className="typing-dot" />
                  <div className="typing-dot" />
                </div>
              </div>
            )}
            <div ref={messagesEnd} />
          </div>

          <div className="ai-input-area">
            <div className="ai-suggestions">
              {SUGGESTIONS.map((s) => (
                <button key={s} className="suggestion-chip" onClick={() => sendMessage(s)}>{s}</button>
              ))}
            </div>
            <div className="ai-input-row">
              <textarea
                className="ai-input"
                rows={1}
                placeholder="Kuch poochein..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); } }}
              />
              <button className="ai-send" onClick={() => sendMessage()} disabled={loading || !input.trim()}>➤</button>
            </div>
          </div>
        </aside>
      </div>
    </>
  );
}
