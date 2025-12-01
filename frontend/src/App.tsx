import { useEffect, useRef, useState } from "react";
import "./App.css";

interface HistoryItem {
  id: number;
  question: string;
  title: string;
  result: string;
}

type ToastType = "info" | "success" | "error";

interface Toast {
  id: number;
  type: ToastType;
  message: string;
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

const thinkingStages = [
  "🔍 Looking for reliable resources…",
  "📚 Researching and gathering evidence…",
  "🧠 Analyzing and organizing key insights…",
  "✍️ Articulating a clear research memo…",
];

/**
 * Very small markdown → HTML formatter for our memo text.
 * Supports:
 *  - #, ##, ### headings
 *  - **bold**
 *  - "- " bullets rendered as • paragraphs
 *  - other lines as paragraphs
 */
function simpleMarkdownToHtml(md: string): string {
  if (!md) return "";

  // escape HTML first
  let html = md
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // headings
  html = html.replace(/^### (.*)$/gm, "<h3>$1</h3>");
  html = html.replace(/^## (.*)$/gm, "<h2>$1</h2>");
  html = html.replace(/^# (.*)$/gm, "<h1>$1</h1>");

  // bold
  html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

  // bullets: "- text" → "• text"
  html = html.replace(/^- (.*)$/gm, "<p>• $1</p>");

  // any remaining non-empty lines that are not already wrapped
  html = html.replace(
    /^(?!<h1>|<h2>|<h3>|<p>)(.+)$/gm,
    "<p>$1</p>"
  );

  return html;
}

function App() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // chat messages in the main window
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  // history in sidebar (persisted)
  const [history, setHistory] = useState<HistoryItem[]>(() => {
    try {
      const saved = localStorage.getItem("dr_history_v2");
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });
  const [activeId, setActiveId] = useState<number | null>(null);

  // theme + toasts
  const [theme, setTheme] = useState<"dark" | "light">(
    (localStorage.getItem("dr_theme") as "dark" | "light") || "dark"
  );
  const [toasts, setToasts] = useState<Toast[]>([]);

  // thinking animation index
  const [thinkingIndex, setThinkingIndex] = useState(0);

  // scroll + drag-scroll
  const outputRef = useRef<HTMLDivElement | null>(null);
  const dragState = useRef({
    isDown: false,
    startY: 0,
    scrollTop: 0,
  });

  // persist history
  useEffect(() => {
    localStorage.setItem("dr_history_v2", JSON.stringify(history));
  }, [history]);

  // apply theme
  useEffect(() => {
    document.body.dataset.theme = theme;
    localStorage.setItem("dr_theme", theme);
  }, [theme]);

  // auto-scroll when messages or loading change
  useEffect(() => {
    if (!outputRef.current) return;
    const el = outputRef.current;
    el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  // thinking stage animation while loading
  useEffect(() => {
    if (!loading) return;
    setThinkingIndex(0);
    const id = window.setInterval(() => {
      setThinkingIndex((prev) => (prev + 1) % thinkingStages.length);
    }, 1500);
    return () => window.clearInterval(id);
  }, [loading]);

  function showToast(type: ToastType, message: string) {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 3000);
  }

  async function sendRequest() {
    if (!input.trim() || loading) return;

    // show user question bubble immediately
    const userText = input;
    setMessages((prev) => [...prev, { role: "user", content: userText }]);
    setInput("");

    setLoading(true);
    showToast("info", "Research started…");

    try {
      const response = await fetch("http://127.0.0.1:8000/research", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(extractFields(userText)),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      const raw = data?.final_report_markdown;
      const resultText: string =
        typeof raw === "string" ? raw : "No report returned.";

      // assistant bubble
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: resultText },
      ]);

      const id = Date.now();
      const newEntry: HistoryItem = {
        id,
        question: userText,
        title: userText.length > 60 ? userText.slice(0, 60) + "…" : userText,
        result: resultText,
      };

      setHistory((prev) => [newEntry, ...prev]);
      setActiveId(id);

      showToast("success", "Research complete ✅");
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "❌ Error: Could not fetch report." },
      ]);
      showToast("error", "Error while calling the API. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  function extractFields(text: string) {
    const nameMatch = text.match(/name[:=]\s*([^,]+)|company[:=]\s*([^,]+)/i);
    const websiteMatch = text.match(/website[:=]\s*([^, ]+)/i);
    const industryMatch = text.match(/industry[:=]\s*([^,]+)/i);
    const depthMatch = text.match(
      /(brief|standard|detailed|descriptive|deep dive)/i
    );

    return {
      company_name: nameMatch?.[1] || nameMatch?.[2] || "Unknown",
      website: websiteMatch?.[1] || "",
      industry: industryMatch?.[1] || "",
      memo_depth: depthMatch?.[1]?.toLowerCase() || "standard",
    };
  }

  function handleNewChat() {
    setMessages([]);
    setActiveId(null);
    setInput("");
  }

  function handleClearHistory() {
    setHistory([]);
    setMessages([]);
    setActiveId(null);
    showToast("info", "History cleared.");
  }

  // drag-scroll handlers
  function handleMouseDown(e: React.MouseEvent<HTMLDivElement>) {
    const el = outputRef.current;
    if (!el) return;
    dragState.current.isDown = true;
    dragState.current.startY = e.clientY;
    dragState.current.scrollTop = el.scrollTop;
    el.classList.add("dragging");
  }

  function handleMouseMove(e: React.MouseEvent<HTMLDivElement>) {
    const el = outputRef.current;
    if (!el || !dragState.current.isDown) return;
    const dy = e.clientY - dragState.current.startY;
    el.scrollTop = dragState.current.scrollTop - dy;
  }

  function handleMouseUpOrLeave() {
    const el = outputRef.current;
    dragState.current.isDown = false;
    if (el) el.classList.remove("dragging");
  }

  return (
    <div className="app-container">
      {/* ====== SIDEBAR ====== */}
      <div className="sidebar">
        <div className="sidebar-header-row">
          <h1 className="title">Deep Research Agent</h1>
          <button
            className="theme-toggle"
            onClick={() =>
              setTheme((prev) => (prev === "dark" ? "light" : "dark"))
            }
          >
            {theme === "dark" ? "☀" : "🌙"}
          </button>
        </div>

        <button className="new-chat" onClick={handleNewChat}>
          + New
        </button>

        <button
          className="clear-history-btn"
          onClick={handleClearHistory}
          disabled={history.length === 0}
        >
          🗑 Clear history
        </button>

        <h2 className="history-title">RESEARCH HISTORY</h2>

        <div className="history-list">
          {history.length === 0 ? (
            <p className="empty-history">
              No research yet. Run your first request!
            </p>
          ) : (
            history.map((h) => (
              <div
                key={h.id}
                className={
                  "history-item" + (activeId === h.id ? " active-history" : "")
                }
                onClick={() => {
                  setActiveId(h.id);
                  setMessages([
                    { role: "user", content: h.question },
                    { role: "assistant", content: h.result },
                  ]);
                }}
              >
                {h.title}
              </div>
            ))
          )}
        </div>

        <div className="api-box">
          <p className="api-label">API Key (optional, sent as X-API-Key)</p>
          <input
            className="apikey-input"
            placeholder="Paste key here..."
            // wire into headers later if needed
          />
        </div>
      </div>

      {/* ====== MAIN CHAT AREA ====== */}
      <div className="main">
        <h2 className="header">Research about anything</h2>

        <div
          className="output-box"
          ref={outputRef}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUpOrLeave}
          onMouseLeave={handleMouseUpOrLeave}
        >
          {!messages.length && !loading && (
            <p className="placeholder-text">
              Ask your research agent about any company, topic, or industry to
              get a detailed memo.
            </p>
          )}

          <div className="messages-container">
            {messages.map((msg, i) => {
              const isUser = msg.role === "user";
              return (
                <div
                  key={i}
                  className={
                    "msg-row " + (isUser ? "msg-row-user" : "msg-row-assistant")
                  }
                >
                  {/* Assistant avatar on left */}
                  {!isUser && (
                    <div className="msg-avatar msg-avatar-ai">
                      <span>RA</span>
                    </div>
                  )}

                  <div
                    className={
                      "msg-bubble " +
                      (isUser ? "user-msg" : "ai-msg fade-in")
                    }
                  >
                    {isUser ? (
                      <pre>{msg.content}</pre>
                    ) : (
                      <div
                        className="markdown-body"
                        dangerouslySetInnerHTML={{
                          __html: simpleMarkdownToHtml(msg.content),
                        }}
                      />
                    )}
                  </div>

                  {/* User avatar on right */}
                  {isUser && (
                    <div className="msg-avatar msg-avatar-user">
                      <span>U</span>
                    </div>
                  )}
                </div>
              );
            })}

            {loading && (
              <div className="msg-row msg-row-assistant">
                <div className="msg-avatar msg-avatar-ai">
                  <span>RA</span>
                </div>
                <div className="msg-bubble ai-msg fade-in">
                  <div className="thinking-status">
                    {thinkingStages[thinkingIndex]}
                  </div>
                  <div className="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* input area */}
        <div className="input-area">
          <div className="input-wrapper">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder='Example: "Do a detailed research on company name: Microsoft, website: https://www.microsoft.com, industry: Technology, response: brief"'
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendRequest();
                }
              }}
            />
            <button onClick={sendRequest} className="send-btn">
              {loading ? "Researching…" : "Send"}
            </button>
          </div>
          <p className="input-helper">
            Tip: Mention <span>name</span>, <span>website</span>,{" "}
            <span>industry</span>, and <span>brief / detailed</span> for best
            results.
          </p>
        </div>
      </div>

      {/* Toasts */}
      <div className="toast-container">
        {toasts.map((t) => (
          <div key={t.id} className={`toast toast-${t.type}`}>
            {t.message}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
