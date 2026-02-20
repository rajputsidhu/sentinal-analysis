import './RiskDashboard.css';

export default function RiskDashboard({ data }) {
    if (!data) {
        return (
            <div className="risk-dashboard glass-card">
                <h3>Risk Dashboard</h3>
                <div className="risk-empty">Send a prompt to see analysis</div>
            </div>
        );
    }

    const { risk_analysis, explanation, action_taken, rewritten_prompt } = data;
    const { blue_team, red_team } = risk_analysis;

    const levelColors = {
        safe: 'var(--color-safe)',
        suspicious: 'var(--color-warn)',
        malicious: 'var(--color-danger)',
    };
    const levelColor = levelColors[blue_team.risk_level] || 'var(--text-muted)';

    return (
        <div className="risk-dashboard glass-card">
            <h3>Risk Dashboard</h3>

            {/* Risk Level Badge */}
            <div className="risk-level-row">
                <span className="risk-level-badge" style={{ '--lc': levelColor }}>
                    {blue_team.risk_level?.toUpperCase() || 'SAFE'}
                </span>
                <span className="risk-score-pill">{risk_analysis.final_score.toFixed(0)}/100</span>
                {risk_analysis.categories.length > 0 && (
                    <div className="category-tags">
                        {risk_analysis.categories.map((c, i) => (
                            <span key={i} className="cat-tag">{c.replace('_', ' ')}</span>
                        ))}
                    </div>
                )}
            </div>

            {/* Explanation */}
            {explanation && (
                <div className="risk-explanation">
                    <div className="risk-section-label">Explanation</div>
                    <p>{explanation}</p>
                </div>
            )}

            {/* Risky Phrases */}
            {blue_team.risky_phrases?.length > 0 && (
                <div className="risky-phrases">
                    <div className="risk-section-label">Highlighted Phrases</div>
                    <div className="phrase-list">
                        {blue_team.risky_phrases.map((p, i) => (
                            <span key={i} className="phrase-chip">{p}</span>
                        ))}
                    </div>
                </div>
            )}

            {/* Red-Team Insight */}
            {red_team.hidden_intent && red_team.hidden_intent !== 'none detected' && (
                <div className="redteam-insight">
                    <div className="risk-section-label">🔴 Red-Team Insight</div>
                    <div className="insight-row"><span>Hidden Intent:</span> {red_team.hidden_intent}</div>
                    <div className="insight-row"><span>Attack Type:</span> {red_team.attack_type}</div>
                    <div className="insight-row"><span>Target:</span> {red_team.sensitive_target}</div>
                    <div className="insight-row"><span>Confidence:</span> {(red_team.confidence_score * 100).toFixed(0)}%</div>
                </div>
            )}

            {/* Rewritten Prompt */}
            {rewritten_prompt && (
                <div className="rewrite-section">
                    <div className="risk-section-label">✏️ Sanitized Prompt</div>
                    <p className="rewritten-text">{rewritten_prompt}</p>
                </div>
            )}

            {/* Action */}
            <div className="action-row">
                <span className="risk-section-label">Action:</span>
                <span className="action-taken">{action_taken.toUpperCase()}</span>
            </div>
        </div>
    );
}
