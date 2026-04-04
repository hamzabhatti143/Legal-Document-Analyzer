"use client";
import type { AnalysisResult, Severity } from "../lib/types";

const severityColor: Record<Severity, string> = {
  low: "#22c55e",
  medium: "#f59e0b",
  high: "#ef4444",
  critical: "#7f1d1d",
};

const severityBg: Record<Severity, string> = {
  low: "#f0fdf4",
  medium: "#fffbeb",
  high: "#fef2f2",
  critical: "#450a0a",
};

const severityTextColor: Record<Severity, string> = {
  low: "#14532d",
  medium: "#78350f",
  high: "#7f1d1d",
  critical: "#fecaca",
};

interface ResultsProps {
  data: AnalysisResult;
}

export default function Results({ data }: ResultsProps) {
  const { metadata, analysis } = data;

  return (
    <div className="results">
      <div className="verdict-bar" style={{ borderLeft: `4px solid ${severityColor[analysis.severity]}` }}>
        <span className="verdict-label" style={{ color: severityColor[analysis.severity] }}>
          {analysis.severity.toUpperCase()} RISK
        </span>
        <p className="verdict-text">{analysis.verdict}</p>
        <div className="meta-tags">
          <span className="tag">📁 {metadata.filename}</span>
          <span className="tag">⚖️ {analysis.domain}</span>
          {metadata.pages && <span className="tag">📄 {metadata.pages} pages</span>}
          <span className="tag">📝 {metadata.wordCount?.toLocaleString()} words</span>
        </div>
      </div>

      <section className="result-section summary-section">
        <h2>📋 Summary</h2>
        <p>{analysis.summary}</p>
      </section>

      {analysis.risks?.length > 0 && (
        <section className="result-section risks-section">
          <h2>⚠️ Risks Identified ({analysis.risks.length})</h2>
          {analysis.risks.map((r, i) => (
            <div
              key={i}
              className="card risk-card"
              style={{ borderLeft: `3px solid ${severityColor[r.severity]}`, background: severityBg[r.severity], color: severityTextColor[r.severity] }}
            >
              <div className="card-header">
                <strong style={{ color: severityTextColor[r.severity] }}>{r.title}</strong>
                <span className="badge" style={{ background: severityColor[r.severity] }}>{r.severity}</span>
              </div>
              <p style={{ color: severityTextColor[r.severity] }}>{r.description}</p>
              {r.clause && <small className="clause" style={{ color: severityTextColor[r.severity], opacity: 0.8 }}>📌 Clause: {r.clause}</small>}
            </div>
          ))}
        </section>
      )}

      {analysis.obligations?.length > 0 && (
        <section className="result-section obligations-section">
          <h2>📌 Obligations</h2>
          {analysis.obligations.map((o, i) => (
            <div key={i} className="card obligation-card">
              <strong>{o.party}</strong>
              <p>{o.action}</p>
              {o.deadline && <small>⏰ Deadline: {o.deadline}</small>}
            </div>
          ))}
        </section>
      )}

      {analysis.improvements?.length > 0 && (
        <section className="result-section improvements-section">
          <h2>💡 Suggested Improvements</h2>
          {analysis.improvements.map((imp, i) => (
            <div key={i} className="card improvement-card">
              <strong>🔧 {imp.issue}</strong>
              <p>{imp.suggestion}</p>
              <small className="priority">Priority: {imp.priority}</small>
            </div>
          ))}
        </section>
      )}

      {analysis.keyTerms?.length > 0 && (
        <section className="result-section">
          <h2>🔑 Key Terms</h2>
          <div className="key-terms">
            {analysis.keyTerms.map((term, i) => <span key={i} className="term-badge">{term}</span>)}
          </div>
        </section>
      )}
    </div>
  );
}
