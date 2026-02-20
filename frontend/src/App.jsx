import { useState } from 'react';
import './App.css';
import ChatPanel from './components/ChatPanel';
import ThreatGauge from './components/ThreatGauge';
import AnalysisBreakdown from './components/AnalysisBreakdown';
import SessionLog from './components/SessionLog';
import StatusBar from './components/StatusBar';

export default function App() {
  const [sessionId, setSessionId] = useState(null);
  const [latestAnalysis, setLatestAnalysis] = useState(null);
  const [analysisHistory, setAnalysisHistory] = useState([]);

  const handleAnalysis = (sentinel) => {
    setLatestAnalysis(sentinel.analysis);
    setAnalysisHistory((prev) => [...prev, sentinel.analysis]);
  };

  return (
    <div className="app-layout">
      {/* ── Header ── */}
      <header className="app-header glass-card">
        <div className="app-logo">
          <div className="shield-icon">🛡️</div>
          <div>
            <h1>Sentinel-AI</h1>
            <div className="subtitle">Security Gateway</div>
          </div>
        </div>
      </header>

      {/* ── Main: Chat Panel ── */}
      <main className="main-area">
        <ChatPanel
          onAnalysis={handleAnalysis}
          sessionId={sessionId}
          onSessionId={setSessionId}
        />
      </main>

      {/* ── Sidebar: Gauge + Breakdown + Log ── */}
      <aside className="sidebar">
        <ThreatGauge
          score={latestAnalysis?.threat_score || 0}
          action={latestAnalysis?.action || 'allow'}
        />
        <AnalysisBreakdown analysis={latestAnalysis} />
        <SessionLog analyses={analysisHistory} />
      </aside>

      {/* ── Footer: Status Bar ── */}
      <footer className="app-footer">
        <StatusBar />
      </footer>
    </div>
  );
}
