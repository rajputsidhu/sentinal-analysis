import './SessionLog.css';

export default function SessionLog({ analyses = [] }) {
    const getActionColor = (action) => {
        const map = { allow: 'var(--color-safe)', warn: 'var(--color-warn)', rewrite: 'var(--color-rewrite)', block: 'var(--color-block)' };
        return map[action] || 'var(--text-muted)';
    };

    return (
        <div className="session-log glass-card">
            <h3>Session Log</h3>
            {analyses.length === 0 ? (
                <div className="log-empty">No analysis events yet</div>
            ) : (
                <div className="log-entries">
                    {analyses.map((a, i) => {
                        const ra = a.risk_analysis;
                        const color = getActionColor(ra.action);
                        return (
                            <div key={i} className="log-entry" style={{ animation: 'fadeIn 0.3s ease' }}>
                                <div className="log-dot" style={{ background: color, boxShadow: `0 0 6px ${color}` }} />
                                <div className="log-body">
                                    <div className="log-top">
                                        <span className="log-action" style={{ color }}>{ra.action.toUpperCase()}</span>
                                        <span className="log-score">{ra.final_score.toFixed(0)}/100</span>
                                        <span className="log-turn">Turn {ra.drift.turn_number}</span>
                                    </div>
                                    {ra.categories.length > 0 && (
                                        <div className="log-categories">
                                            {ra.categories.map((c, j) => (
                                                <span key={j} className="log-cat">{c.replace('_', ' ')}</span>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}
