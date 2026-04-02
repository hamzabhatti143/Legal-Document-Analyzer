import { NextResponse } from "next/server";

export async function GET(): Promise<NextResponse> {
  return NextResponse.json({ status: "ok", service: "Document Analyzer", timestamp: new Date().toISOString() });
}
