import './SessionLog.css';

const ACTION_STYLES = {
    allow: { bg: 'rgba(16,185,129,0.12)', color: 'var(--color-safe)', icon: '✅' },
    warn: { bg: 'rgba(245,158,11,0.12)', color: 'var(--color-warn)', icon: '⚠️' },
    rewrite: { bg: 'rgba(139,92,246,0.12)', color: 'var(--color-rewrite)', icon: '✏️' },
    block: { bg: 'rgba(239,68,68,0.12)', color: 'var(--color-danger)', icon: '⛔' },
};

export default function SessionLog({ analyses = [] }) {
    return (
        <div className="session-log glass-card">
            <div className="panel-header">
                <h2><span className="icon">📜</span> Session Log</h2>
                <span className="log-count">{analyses.length} events</span>
            </div>
            <div className="panel-body log-entries">
                {analyses.length === 0 ? (
                    <div className="empty-panel"><p>No events yet</p></div>
                ) : (
                    analyses.map((entry, i) => {
                        const action = entry.action || 'allow';
                        const style = ACTION_STYLES[action] || ACTION_STYLES.allow;
                        return (
                            <div key={i} className="log-entry animate-in" style={{ animationDelay: `${i * 0.05}s` }}>
                                <div className="log-timeline">
                                    <div className="log-dot" style={{ background: style.color }} />
                                    {i < analyses.length - 1 && <div className="log-line" />}
                                </div>
                                <div className="log-content">
                                    <div className="log-header">
                                        <span className="log-action-badge" style={{ background: style.bg, color: style.color }}>
                                            {style.icon} {action.toUpperCase()}
                                        </span>
                                        <span className="log-score" style={{ color: style.color }}>
                                            {(entry.threat_score * 100).toFixed(0)}%
                                        </span>
                                    </div>
                                    {entry.categories?.length > 0 && (
                                        <div className="log-categories">
                                            {entry.categories.filter(c => c !== 'none').map((c, j) => (
                                                <span key={j} className="log-cat">{c}</span>
                                            ))}
                                        </div>
                                    )}
                                    <div className="log-time">
                                        {entry.timestamp ? new Date(entry.timestamp).toLocaleTimeString() : ''}
                                    </div>
                                </div>
                            </div>
                        );
                    })
                )}
            </div>
        </div>
    );
}
