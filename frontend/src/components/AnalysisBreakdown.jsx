import { useState } from 'react';
import './AnalysisBreakdown.css';

const ENGINE_META = {
    embedding: { icon: '🔍', label: 'Embedding Engine', desc: 'Semantic similarity to known attack signatures' },
    redteam: { icon: '🎭', label: 'Red-Team LLM', desc: 'Adversarial evaluation of prompt intent' },
    drift: { icon: '📈', label: 'Drift Analyzer', desc: 'Intent tracking across conversation turns' },
    pattern: { icon: '🧬', label: 'Pattern Scanner', desc: 'Regex matching against attack databases' },
};

function ScoreBar({ score, color }) {
    return (
        <div className="score-bar-track">
            <div
                className="score-bar-fill"
                style={{
                    width: `${Math.min(score * 100, 100)}%`,
                    background: color,
                    boxShadow: `0 0 8px ${color}`,
                }}
            />
        </div>
    );
}

function getScoreColor(score) {
    if (score < 0.4) return 'var(--color-safe)';
    if (score < 0.75) return 'var(--color-warn)';
    return 'var(--color-danger)';
}

function EngineCard({ engineKey, data }) {
    const [expanded, setExpanded] = useState(false);
    const meta = ENGINE_META[engineKey];
    if (!meta || !data) return null;

    const score = data.score || 0;
    const color = getScoreColor(score);

    return (
        <div className={`engine-card ${expanded ? 'expanded' : ''}`} onClick={() => setExpanded(!expanded)}>
            <div className="engine-card-header">
                <div className="engine-info">
                    <span className="engine-icon">{meta.icon}</span>
                    <div>
                        <div className="engine-label">{meta.label}</div>
                        <div className="engine-desc">{meta.desc}</div>
                    </div>
                </div>
                <div className="engine-score" style={{ color }}>
                    {(score * 100).toFixed(0)}%
                </div>
            </div>

            <ScoreBar score={score} color={color} />

            {expanded && (
                <div className="engine-details animate-in">
                    {data.top_matches?.length > 0 && (
                        <div className="detail-row">
                            <span className="detail-label">Matches</span>
                            <div className="detail-tags">
                                {data.top_matches.map((m, i) => <span key={i} className="detail-tag">{m}</span>)}
                            </div>
                        </div>
                    )}
                    {data.reasoning && (
                        <div className="detail-row">
                            <span className="detail-label">Reasoning</span>
                            <span className="detail-value">{data.reasoning}</span>
                        </div>
                    )}
                    {data.categories?.length > 0 && (
                        <div className="detail-row">
                            <span className="detail-label">Categories</span>
                            <div className="detail-tags">
                                {data.categories.map((c, i) => <span key={i} className="detail-tag tag-danger">{c}</span>)}
                            </div>
                        </div>
                    )}
                    {data.drift_detected !== undefined && (
                        <div className="detail-row">
                            <span className="detail-label">Drift</span>
                            <span className={`detail-value ${data.drift_detected ? 'text-warn' : ''}`}>
                                {data.drift_detected ? '⚠️ Detected' : '✅ None'}
                            </span>
                        </div>
                    )}
                    {data.details && (
                        <div className="detail-row">
                            <span className="detail-label">Details</span>
                            <span className="detail-value">{data.details}</span>
                        </div>
                    )}
                    {data.matches?.length > 0 && (
                        <div className="detail-row">
                            <span className="detail-label">Patterns</span>
                            <div className="detail-tags">
                                {data.matches.map((m, i) => <span key={i} className="detail-tag tag-danger">{m}</span>)}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default function AnalysisBreakdown({ analysis }) {
    if (!analysis) {
        return (
            <div className="analysis-breakdown glass-card">
                <div className="panel-header">
                    <h2><span className="icon">📊</span> Analysis Breakdown</h2>
                </div>
                <div className="panel-body empty-panel">
                    <p>Send a message to see per-engine analysis</p>
                </div>
            </div>
        );
    }

    return (
        <div className="analysis-breakdown glass-card">
            <div className="panel-header">
                <h2><span className="icon">📊</span> Analysis Breakdown</h2>
                <span className="timestamp">{new Date(analysis.timestamp).toLocaleTimeString()}</span>
            </div>
            <div className="panel-body engines-list">
                <EngineCard engineKey="embedding" data={analysis.embedding} />
                <EngineCard engineKey="redteam" data={analysis.redteam} />
                <EngineCard engineKey="drift" data={analysis.drift} />
                <EngineCard engineKey="pattern" data={analysis.pattern} />
            </div>
        </div>
    );
}
