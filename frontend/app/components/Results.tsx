"use client";
import type { AnalysisResult, Severity } from "../lib/types";
import { translations, type Lang } from "../lib/translations";

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

interface ResultsProps {
  data: AnalysisResult;
  lang: Lang;
}

export default function Results({ data, lang }: ResultsProps) {
  const { metadata, analysis } = data;
  const t = translations[lang];

  return (
    <div className="results">
      <div className="verdict-bar" style={{ borderLeft: `4px solid ${severityColor[analysis.severity]}` }}>
        <span className="verdict-label" style={{ color: severityColor[analysis.severity] }}>
          {t.severityLabels[analysis.severity]} {t.riskLabel}
        </span>
        <p className="verdict-text">{analysis.verdict}</p>
        <div className="meta-tags">
          <span className="tag">📁 {metadata.filename}</span>
          <span className="tag">⚖️ {analysis.domain}</span>
          {metadata.pages && <span className="tag">📄 {metadata.pages} {t.pages}</span>}
          <span className="tag">📝 {metadata.wordCount?.toLocaleString()} {t.words}</span>
        </div>
      </div>

      <section className="result-section summary-section">
        <h2>📋 {t.summary}</h2>
        <p>{analysis.summary}</p>
      </section>

      {analysis.risks?.length > 0 && (
        <section className="result-section risks-section">
          <h2>⚠️ {t.risks} ({analysis.risks.length})</h2>
          {analysis.risks.map((r, i) => (
            <div
              key={i}
              className="card risk-card"
              style={{ borderLeft: `3px solid ${severityColor[r.severity]}`, background: severityBg[r.severity] }}
            >
              <div className="card-header">
                <strong>{r.title}</strong>
                <span className="badge" style={{ background: severityColor[r.severity] }}>{t.severityLabels[r.severity]}</span>
              </div>
              <p>{r.description}</p>
              {r.clause && <small className="clause">📌 {t.clause}: {r.clause}</small>}
            </div>
          ))}
        </section>
      )}

      {analysis.obligations?.length > 0 && (
        <section className="result-section obligations-section">
          <h2>📌 {t.obligations}</h2>
          {analysis.obligations.map((o, i) => (
            <div key={i} className="card obligation-card">
              <strong>{o.party}</strong>
              <p>{o.action}</p>
              {o.deadline && <small>⏰ {t.deadline}: {o.deadline}</small>}
            </div>
          ))}
        </section>
      )}

      {analysis.improvements?.length > 0 && (
        <section className="result-section improvements-section">
          <h2>💡 {t.improvements}</h2>
          {analysis.improvements.map((imp, i) => (
            <div key={i} className="card improvement-card">
              <strong>🔧 {imp.issue}</strong>
              <p>{imp.suggestion}</p>
              <small className="priority">{t.priority}: {imp.priority}</small>
            </div>
          ))}
        </section>
      )}

      {analysis.keyTerms?.length > 0 && (
        <section className="result-section">
          <h2>🔑 {t.keyTerms}</h2>
          <div className="key-terms">
            {analysis.keyTerms.map((term, i) => <span key={i} className="term-badge">{term}</span>)}
          </div>
        </section>
      )}
    </div>
  );
}
