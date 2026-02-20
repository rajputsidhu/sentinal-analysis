import { useState, useEffect } from 'react';
import './StatusBar.css';

export default function StatusBar() {
    const [health, setHealth] = useState(null);
    const [online, setOnline] = useState(false);

    useEffect(() => {
        const check = async () => {
            try {
                const res = await fetch('/api/health');
                if (res.ok) {
                    const data = await res.json();
                    setHealth(data);
                    setOnline(true);
                } else {
                    setOnline(false);
                }
            } catch {
                setOnline(false);
            }
        };
        check();
        const interval = setInterval(check, 10000);
        return () => clearInterval(interval);
    }, []);

    const formatUptime = (seconds) => {
        if (!seconds) return '—';
        const h = Math.floor(seconds / 3600);
        const m = Math.floor((seconds % 3600) / 60);
        const s = Math.floor(seconds % 60);
        if (h > 0) return `${h}h ${m}m`;
        if (m > 0) return `${m}m ${s}s`;
        return `${s}s`;
    };

    return (
        <div className="status-bar glass-card">
            <div className="status-section">
                <div className={`status-indicator ${online ? 'online' : 'offline'}`}>
                    <span className="status-dot" />
                    <span className="status-text">{online ? 'Connected' : 'Offline'}</span>
                </div>
            </div>

            {health && (
                <>
                    <div className="status-divider" />
                    <div className="status-section">
                        <span className="status-label">Uptime</span>
                        <span className="status-value">{formatUptime(health.uptime_seconds)}</span>
                    </div>
                    <div className="status-divider" />
                    <div className="status-section">
                        <span className="status-label">Sessions</span>
                        <span className="status-value">{health.active_sessions}</span>
                    </div>
                    <div className="status-divider" />
                    <div className="status-section">
                        <span className="status-label">Mode</span>
                        <span className="status-value mode-badge">
                            {health.config?.analysis_mode || '—'}
                        </span>
                    </div>
                    <div className="status-divider" />
                    <div className="status-section">
                        <span className="status-label">Model</span>
                        <span className="status-value">{health.config?.model || '—'}</span>
                    </div>
                    {health.config?.dry_run && (
                        <>
                            <div className="status-divider" />
                            <div className="status-section">
                                <span className="dry-run-badge">🧪 DRY-RUN</span>
                            </div>
                        </>
                    )}
                </>
            )}
        </div>
    );
}
