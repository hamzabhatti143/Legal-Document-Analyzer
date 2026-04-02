"use server";

import type { AnalysisResult } from "../lib/types";

const ALLOWED_TYPES = [
  "application/pdf",
  "application/msword",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
];

export async function analyzeDocumentAction(formData: FormData): Promise<AnalysisResult> {
  const file = formData.get("document") as File | null;
  const domain = (formData.get("domain") as string) || "general";

  if (!file) throw new Error("No file uploaded");
  if (!ALLOWED_TYPES.includes(file.type)) throw new Error("Only PDF and DOC/DOCX files are allowed");
  if (file.size > 10 * 1024 * 1024) throw new Error("File size must be under 10MB");

  const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";

  const language = (formData.get("language") as string) || "en";

  const backendForm = new FormData();
  backendForm.append("file", file);
  backendForm.append("domain", domain);
  backendForm.append("language", language);

  const res = await fetch(`${backendUrl}/analyze`, {
    method: "POST",
    body: backendForm,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Analysis failed" }));
    throw new Error(err.detail || "Analysis failed");
  }

  return res.json();
}
