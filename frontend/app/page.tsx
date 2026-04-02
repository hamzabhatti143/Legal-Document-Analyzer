import Image from "next/image";
import LegalAnalyzer from "./components/LegalAnalyzer";

export default function Home() {
  return (
    <main className="main">
      <header className="header">
        <div className="logo">
          <Image src="/images/logo.svg" alt="Document Analyzer" width={72} height={72} priority />
        </div>
        <h1>Document Analyzer</h1>
        <p>Upload any document — get plain English analysis, risks, and advice instantly.</p>
        <small className="powered">Intelligent Document Analysis</small>
      </header>
      <div className="content">
        <LegalAnalyzer />
      </div>
    </main>
  );
}
