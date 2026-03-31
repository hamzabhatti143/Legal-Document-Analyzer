import { NextResponse } from "next/server";

export async function GET(): Promise<NextResponse> {
  return NextResponse.json({ status: "ok", service: "Legal Docs AI (Gemini)", timestamp: new Date().toISOString() });
}
