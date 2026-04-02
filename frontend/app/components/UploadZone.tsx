"use client";
import { useState, useRef } from "react";
import { translations, type Lang } from "../lib/translations";

interface UploadZoneProps {
  onSubmit: (formData: FormData) => void;
  isLoading: boolean;
  error: string;
  lang: Lang;
}

const ALLOWED_TYPES = [
  "application/pdf",
  "application/msword",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
];

const DOMAIN_KEYS = ["general", "contract", "employment", "real_estate", "ip", "corporate", "privacy"] as const;

export default function UploadZone({ onSubmit, isLoading, error, lang }: UploadZoneProps) {
  const [dragging, setDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [domain, setDomain] = useState("general");
  const [localError, setLocalError] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  const t = translations[lang];

  const handleFile = (f: File | null | undefined) => {
    if (!f) return;
    if (!ALLOWED_TYPES.includes(f.type)) { setLocalError(t.errorType); return; }
    if (f.size > 10 * 1024 * 1024) { setLocalError(t.errorSize); return; }
    setLocalError("");
    setFile(f);
  };

  const handleSubmit = () => {
    if (!file) return;
    const form = new FormData();
    form.append("document", file);
    form.append("domain", domain);
    onSubmit(form);
  };

  const displayError = localError || error;

  return (
    <div className="upload-zone-container">
      <div
        className={`drop-zone ${dragging ? "dragging" : ""} ${file ? "has-file" : ""}`}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => { e.preventDefault(); setDragging(false); handleFile(e.dataTransfer.files[0]); }}
        onClick={() => inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.doc,.docx"
          hidden
          onChange={(e) => handleFile(e.target.files?.[0])}
        />
        {file ? (
          <div className="file-info">
            <span className="file-icon">📄</span>
            <span className="file-name">{file.name}</span>
            <span className="file-size">{(file.size / 1024).toFixed(1)} KB</span>
          </div>
        ) : (
          <div className="upload-prompt">
            <span className="upload-icon">⬆</span>
            <p>{t.dropZone}</p>
            <small>{t.dropZoneHint}</small>
          </div>
        )}
      </div>

      <select className="domain-select" value={domain} onChange={(e) => setDomain(e.target.value)}>
        {DOMAIN_KEYS.map((key) => (
          <option key={key} value={key}>{t.domains[key]}</option>
        ))}
      </select>

      {displayError && <p className="error-msg">{displayError}</p>}

      <button className="analyze-btn" onClick={handleSubmit} disabled={!file || isLoading}>
        {isLoading ? t.analyzing : t.analyzeBtn}
      </button>
    </div>
  );
}
