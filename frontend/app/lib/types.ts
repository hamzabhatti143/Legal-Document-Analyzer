export type Severity = "low" | "medium" | "high" | "critical";
export type Priority = "low" | "medium" | "high";
export type Domain = "contract" | "employment" | "real_estate" | "ip" | "corporate" | "privacy" | "general";

export interface Risk {
  title: string;
  description: string;
  severity: Severity;
  clause?: string;
}

export interface Obligation {
  party: string;
  action: string;
  deadline?: string;
}

export interface Improvement {
  issue: string;
  suggestion: string;
  priority: Priority;
}

export interface Analysis {
  domain: Domain;
  severity: Severity;
  summary: string;
  risks: Risk[];
  obligations: Obligation[];
  improvements: Improvement[];
  keyTerms: string[];
  verdict: string;
}

export interface Metadata {
  pages: number | null;
  wordCount: number;
  domain: string;
  filename: string;
}

export interface AnalysisResult {
  success: boolean;
  metadata: Metadata;
  analysis: Analysis;
}

export interface ParseResult {
  text: string;
  pages: number | null;
  wordCount: number;
}
