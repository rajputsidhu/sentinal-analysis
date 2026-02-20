import { useState, useEffect } from 'react';
import './StatusBar.css';

export default function StatusBar() {
    const [health, setHealth] = useState(null);
    const [online, setOnline] = useState(false);

    useEffect(() => {
        const check = async () => {
            try {
                const res = await fetch('/api/health');
                if (res.ok) { setHealth(await res.json()); setOnline(true); }
                else setOnline(false);
            } catch { setOnline(false); }
        };
        check();
        const interval = setInterval(check, 10000);
        return () => clearInterval(interval);
    }, []);

    const uptime = (s) => {
        if (!s) return '—';
        const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60);
        return h > 0 ? `${h}h ${m}m` : `${m}m ${Math.floor(s % 60)}s`;
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
                    <div className="status-section"><span className="status-label">Uptime</span><span className="status-value">{uptime(health.uptime_seconds)}</span></div>
                    <div className="status-divider" />
                    <div className="status-section"><span className="status-label">Mode</span><span className="status-value mode-badge">{health.config?.analysis_mode}</span></div>
                    <div className="status-divider" />
                    <div className="status-section"><span className="status-label">Model</span><span className="status-value">{health.config?.model}</span></div>
                    <div className="status-divider" />
                    <div className="status-section">
                        <span className="status-label">Thresholds</span>
                        <span className="status-value">{health.config?.threshold_allow}/{health.config?.threshold_warn}/{health.config?.threshold_rewrite}</span>
                    </div>
                    {health.config?.dry_run && (
                        <><div className="status-divider" /><div className="status-section"><span className="dry-run-badge">🧪 DRY-RUN</span></div></>
                    )}
                </>
            )}
        </div>
    );
}
