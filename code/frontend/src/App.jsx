import { useState } from 'react';
import './App.css';
import ChatPanel from './components/ChatPanel';
import ThreatGauge from './components/ThreatGauge';
import DriftChart from './components/DriftChart';
import RiskDashboard from './components/RiskDashboard';
import SessionLog from './components/SessionLog';
import StatusBar from './components/StatusBar';

export default function App() {
  const [conversationId, setConversationId] = useState(null);
  const [latestData, setLatestData] = useState(null);
  const [analysisHistory, setAnalysisHistory] = useState([]);
  const [driftHistory, setDriftHistory] = useState([]);

  const handleAnalysis = (data) => {
    setLatestData(data);
    setAnalysisHistory((prev) => [...prev, data]);

    // Track drift over turns
    if (data.risk_analysis?.drift) {
      setDriftHistory((prev) => [
        ...prev,
        {
          score: data.drift_score,
          turn: data.risk_analysis.drift.turn_number,
        },
      ]);
    }
  };

  return (
    <div className="app-layout">
      {/* ── Header ── */}
      <header className="app-header glass-card">
        <div className="app-logo">
          <div className="shield-icon">🛡️</div>
          <div>
            <h1>Sentinel-AI</h1>
            <div className="subtitle">Security Gateway v2</div>
          </div>
        </div>
        <div className="header-version">v2.0.0</div>
      </header>

      {/* ── Main: Chat + Risk Dashboard ── */}
      <main className="main-area">
        <ChatPanel
          onAnalysis={handleAnalysis}
          conversationId={conversationId}
          onConversationId={setConversationId}
        />
      </main>

      {/* ── Sidebar ── */}
      <aside className="sidebar">
        <ThreatGauge
          score={latestData?.risk_analysis?.final_score || 0}
          action={latestData?.action_taken || 'allow'}
        />
        <DriftChart driftHistory={driftHistory} />
        <RiskDashboard data={latestData} />
        <SessionLog analyses={analysisHistory} />
      </aside>

      {/* ── Footer ── */}
      <footer className="app-footer">
        <StatusBar />
      </footer>
    </div>
  );
}
