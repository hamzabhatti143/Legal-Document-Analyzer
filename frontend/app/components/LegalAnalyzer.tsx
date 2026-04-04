"use client";
import { useState, useTransition, useEffect, useRef } from "react";
import { analyzeDocumentAction } from "../actions/analyze";
import UploadZone from "./UploadZone";
import Results from "./Results";
import { translations, type Lang } from "../lib/translations";
import type { AnalysisResult } from "../lib/types";

interface Props {
  lang: Lang;
}

export default function LegalAnalyzer({ lang }: Props) {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");
  const [langHint, setLangHint] = useState(false);
  const [isPending, startTransition] = useTransition();
  const isFirstRender = useRef(true);
  const t = translations[lang];

  useEffect(() => {
    if (isFirstRender.current) { isFirstRender.current = false; return; }
    if (result) {
      setResult(null);
      setLangHint(true);
    }
  }, [lang]);

  const handleSubmit = (formData: FormData) => {
    setError("");
    setLangHint(false);
    formData.append("language", lang);
    startTransition(async () => {
      try {
        const data = await analyzeDocumentAction(formData);
        setResult(data);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Analysis failed");
      }
    });
  };

  return (
    <>
      <UploadZone onSubmit={handleSubmit} isLoading={isPending} error={error} lang={lang} />
      {langHint && !isPending && (
        <p className="lang-hint">{t.langChanged}</p>
      )}
      {isPending && (
        <div className="loading">
          <div className="spinner"></div>
          <p>{t.analyzing}</p>
        </div>
      )}
      {result && !isPending && <Results data={result} lang={lang} />}
    </>
  );
}
