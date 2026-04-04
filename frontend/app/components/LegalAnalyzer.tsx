"use client";
import { useState, useTransition } from "react";
import { analyzeDocumentAction } from "../actions/analyze";
import UploadZone from "./UploadZone";
import Results from "./Results";
import type { AnalysisResult } from "../lib/types";

export default function LegalAnalyzer() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");
  const [isPending, startTransition] = useTransition();

  const handleSubmit = (formData: FormData) => {
    setError("");
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
      <UploadZone onSubmit={handleSubmit} isLoading={isPending} error={error} />
      {isPending && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Analyzing your document, please wait...</p>
        </div>
      )}
      {result && !isPending && <Results data={result} />}
    </>
  );
}
