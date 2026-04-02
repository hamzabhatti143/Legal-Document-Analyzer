"use client";
import { useState, useTransition } from "react";
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
  const [isPending, startTransition] = useTransition();
  const t = translations[lang];

  const handleSubmit = (formData: FormData) => {
    setError("");
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
