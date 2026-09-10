import { useEffect, useRef, useState } from "react";
import ResultChart from "./components/ResultChart";
import "./index.css";

const API = "http://127.0.0.1:8000";

function formatValue(value, column) {
  if (value == null) return "";

  const name = column.toLowerCase();

  if (typeof value === "string" && /^\d{4}-\d{2}-\d{2}T/.test(value)) {
    const [year, month, day] = value.slice(0, 10).split("-");
    const time = value.slice(11, 19);

    if (name.includes("month")) {
      return new Date(+year, +month - 1).toLocaleDateString("en-GB", {
        month: "short",
        year: "numeric"
      });
    }

    if (time === "00:00:00") return `${day}/${month}/${year}`;
    return `${day}/${month}/${year} ${time.slice(0, 5)}`;
  }

  if (typeof value === "number") {
    if (name.includes("revenue") || name.includes("amount")) {
      return Math.round(value).toLocaleString();
    }

    if (
      name.includes("percent") ||
      name.includes("share") ||
      name.includes("rate")
    ) {
      return `${value.toFixed(1)}%`;
    }

    return Number.isInteger(value)
      ? value.toLocaleString()
      : value.toLocaleString(undefined, { maximumFractionDigits: 2 });
  }

  return String(value);
}

function ResultTable({ data }) {
  if (!data?.length) return null;

  const columns = Object.keys(data[0]);

  return (
    <div style={{ overflowX: "auto", marginTop: 16 }}>
      <table>
        <thead>
          <tr>
            {columns.map(column => (
              <th key={column}>
                {column.replaceAll("_", " ")}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {columns.map(column => (
                <td key={column}>
                  {formatValue(row[column], column)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Change({ value }) {
  if (value == null) return null;

  if (value === 0) {
    return <small>→ 0% vs. previous 30 days</small>;
  }

  const positive = value > 0;

  return (
    <small className={positive ? "positive" : "negative"}>
      {positive ? "↗" : "↘"} {positive ? "+" : ""}
      {value}% vs. previous 30 days
    </small>
  );
}

async function downloadExcel(data, filename = "anytime-analytics.xlsx") {
  if (!data?.length) return;

  const response = await fetch(`${API}/export/excel`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ data, filename })
  });

  if (!response.ok) throw new Error("Excel export failed");

  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();

  URL.revokeObjectURL(url);
}

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [kpis, setKpis] = useState(null);
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);

  async function loadSessions() {
    const response = await fetch(`${API}/sessions`);
    if (!response.ok) throw new Error("Could not load sessions");
    setSessions(await response.json());
  }

  useEffect(() => {
    fetch(`${API}/kpis`)
      .then(response => response.json())
      .then(setKpis)
      .catch(console.error);

    loadSessions().catch(console.error);
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end"
    });
  }, [messages, loading]);

  async function openSession(id) {
    try {
      const response = await fetch(`${API}/sessions/${id}`);
      if (!response.ok) throw new Error("Could not load chat");

      const result = await response.json();

      setSessionId(id);
      setMessages(result.messages);
    } catch (error) {
      console.error(error);
    }
  }

  async function sendQuestion(text = question) {
    const cleanQuestion = text.trim();
    if (!cleanQuestion || loading) return;

    setMessages(prev => [
      ...prev,
      { role: "user", content: cleanQuestion }
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: cleanQuestion,
          session_id: sessionId
        })
      });

      if (!response.ok) {
        throw new Error(`API error ${response.status}`);
      }

      const result = await response.json();

      setSessionId(result.session_id);

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: result.answer,
          data: result.data,
          sql: result.sql,
          suggestions: result.suggestions || []
        }
      ]);

      await loadSessions();
    } catch (error) {
      console.error(error);

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: "Something went wrong while processing your request."
        }
      ]);
    } finally {
      setLoading(false);
    }
  }

  function newChat() {
    setMessages([]);
    setSessionId(null);
    setQuestion("");
  }

  function submit(event) {
    event.preventDefault();
    sendQuestion();
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <div className="logoBox">
            any<br />time
          </div>

          <span>
            Anytime<br />Analytics
          </span>
        </div>

        <button className="newChat" onClick={newChat}>
          ＋ New chat
        </button>

        <p className="sectionTitle">
          Recent conversations
        </p>

        <div className="chats">
          {sessions.slice(0, 10).map(session => (
            <button
              key={session.session_id}
              className={
                session.session_id === sessionId
                  ? "chat active"
                  : "chat"
              }
              onClick={() => openSession(session.session_id)}
              title={session.title}
            >
              {session.title}
            </button>
          ))}
        </div>
      </aside>

      <main className="main">
        <header>
          <h1>Anytime Analytics</h1>
          <p>
            Ask questions about rides, customers, revenue and fleet.
          </p>
        </header>

        <section className="kpis">
          <div className="kpi">
            <span>Revenue</span>
            <strong>
              {kpis
                ? Math.round(kpis.revenue).toLocaleString()
                : "—"}
            </strong>
            <Change value={kpis?.revenue_change} />
          </div>

          <div className="kpi">
            <span>Rides</span>
            <strong>
              {kpis
                ? kpis.rides.toLocaleString()
                : "—"}
            </strong>
            <Change value={kpis?.rides_change} />
          </div>

          <div className="kpi">
            <span>Paying users</span>
            <strong>
              {kpis
                ? kpis.paying_users.toLocaleString()
                : "—"}
            </strong>
            <Change value={kpis?.paying_users_change} />
          </div>

          <div className="kpi">
            <span>Fleet size</span>
            <strong>
              {kpis
                ? kpis.fleet_size.toLocaleString()
                : "—"}
            </strong>

            {kpis && (
              <small
                className={
                  kpis.fleet_change > 0
                    ? "positive"
                    : kpis.fleet_change < 0
                      ? "negative"
                      : ""
                }
              >
                {kpis.fleet_change > 0
                  ? `↗ +${kpis.fleet_change}`
                  : kpis.fleet_change < 0
                    ? `↘ ${kpis.fleet_change}`
                    : "→ 0"}{" "}
                vs. previous day
              </small>
            )}
          </div>
        </section>

        <section className="conversation">
          {messages.length === 0 && (
            <div className="answer">
              <h3>What would you like to know?</h3>
              <p>
                Ask a question about rides, revenue, customers
                or the current fleet.
              </p>
            </div>
          )}

          {messages.map((message, index) => {
            if (message.role === "user") {
              return (
                <div className="userMessage" key={index}>
                  {message.content}
                </div>
              );
            }

            return (
              <div className="answer" key={index}>
                <p>{message.content}</p>

                <ResultTable data={message.data} />

                <ResultChart data={message.data} />

                {message.data?.length > 0 && (
                  <button
                    className="downloadButton"
                    onClick={() => downloadExcel(message.data)}
                  >
                    ↓ Download Excel
                  </button>
                )}

                {message.sql && (
                  <details className="technical">
                    <summary>
                      View SQL query
                    </summary>

                    <pre>
                      <code>{message.sql}</code>
                    </pre>
                  </details>
                )}

                {message.suggestions?.length > 0 && (
                  <div className="messageSuggestions">
                    {message.suggestions.map(
                      (suggestion, suggestionIndex) => (
                        <button
                          key={suggestionIndex}
                          onClick={() =>
                            sendQuestion(suggestion)
                          }
                          disabled={loading}
                        >
                          {suggestion}
                        </button>
                      )
                    )}
                  </div>
                )}
              </div>
            );
          })}

          {loading && (
            <div className="answer loadingAnswer">
              <div className="typingDots">
                <span />
                <span />
                <span />
              </div>
              <span>Analyzing</span>
            </div>
          )}

          <div ref={bottomRef} />
        </section>

        <form
          className="inputBar"
          onSubmit={submit}
        >
          <input
            value={question}
            onChange={event =>
              setQuestion(event.target.value)
            }
            placeholder="Ask your analytics question..."
            disabled={loading}
          />

          <button
            type="submit"
            disabled={loading}
          >
            ➤
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;