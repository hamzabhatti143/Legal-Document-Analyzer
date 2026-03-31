import LegalAnalyzer from "./components/LegalAnalyzer";

export default function Home() {
  return (
    <main className="main">
      <header className="header">
        <div className="logo">⚖️</div>
        <h1>Legal Document Simplifier</h1>
        <p>Upload any legal document — get plain English analysis, risks, and advice instantly.</p>
        <small className="powered">Intelligent Document Analysis</small>
      </header>
      <div className="content">
        <LegalAnalyzer />
      </div>
    </main>
  );
}
