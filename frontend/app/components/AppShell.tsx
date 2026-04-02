"use client";
import { useState } from "react";
import Image from "next/image";
import LegalAnalyzer from "./LegalAnalyzer";
import { translations, type Lang } from "../lib/translations";

export default function AppShell() {
  const [lang, setLang] = useState<Lang>("en");
  const t = translations[lang];
  const isRtl = lang === "ur";

  return (
    <div dir={isRtl ? "rtl" : "ltr"} className={isRtl ? "rtl" : ""}>
      <header className="header">
        <div className="header-top">
          <button
            className="lang-toggle"
            onClick={() => setLang(lang === "en" ? "ur" : "en")}
            aria-label="Toggle language"
          >
            {lang === "en" ? "اردو" : "English"}
          </button>
        </div>
        <div className="logo">
          <Image src="/images/logo.svg" alt="Document Analyzer" width={72} height={72} priority />
        </div>
        <h1>{t.title}</h1>
        <p>{t.subtitle}</p>
        <small className="powered">{t.powered}</small>
      </header>
      <div className="content">
        <LegalAnalyzer lang={lang} />
      </div>
    </div>
  );
}
