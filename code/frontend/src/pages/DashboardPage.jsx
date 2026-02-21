import { useState } from 'react';
import ChatPanel from '../components/ChatPanel';
import ThreatGauge from '../components/ThreatGauge';
import DriftChart from '../components/DriftChart';
import RiskDashboard from '../components/RiskDashboard';
import SessionLog from '../components/SessionLog';
import StatusBar from '../components/StatusBar';
import './DashboardPage.css';

export default function DashboardPage() {
    const [conversationId, setConversationId] = useState(null);
    const [latestData, setLatestData] = useState(null);
    const [analysisHistory, setAnalysisHistory] = useState([]);
    const [driftHistory, setDriftHistory] = useState([]);

    const handleAnalysis = (data) => {
        setLatestData(data);
        setAnalysisHistory((prev) => [...prev, data]);

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
        <div className="dashboard-page">
            <div className="dashboard-layout">
                {/* ── Main: Chat ── */}
                <main className="dash-main">
                    <ChatPanel
                        onAnalysis={handleAnalysis}
                        conversationId={conversationId}
                        onConversationId={setConversationId}
                    />
                </main>

                {/* ── Sidebar ── */}
                <aside className="dash-sidebar">
                    <ThreatGauge
                        score={latestData?.risk_analysis?.final_score || 0}
                        action={latestData?.action_taken || 'allow'}
                    />
                    <DriftChart driftHistory={driftHistory} />
                    <RiskDashboard data={latestData} />
                    <SessionLog analyses={analysisHistory} />
                </aside>
            </div>

            {/* ── Footer ── */}
            <footer className="dash-footer">
                <StatusBar />
            </footer>
        </div>
    );
}
