import { useEffect, useRef } from 'react';
import './ThreatGauge.css';

function getColor(score) {
    if (score < 0.4) return { main: 'var(--color-safe)', glow: 'var(--color-safe-glow)', label: 'SAFE' };
    if (score < 0.6) return { main: 'var(--color-warn)', glow: 'var(--color-warn-glow)', label: 'CAUTION' };
    if (score < 0.75) return { main: 'var(--color-rewrite)', glow: 'var(--color-rewrite-glow)', label: 'HIGH' };
    return { main: 'var(--color-danger)', glow: 'var(--color-danger-glow)', label: 'CRITICAL' };
}

export default function ThreatGauge({ score = 0, action = 'allow' }) {
    const circleRef = useRef(null);
    const radius = 70;
    const circumference = 2 * Math.PI * radius;
    const clampedScore = Math.min(Math.max(score, 0), 1);
    const offset = circumference - clampedScore * circumference;
    const { main, glow, label } = getColor(clampedScore);

    useEffect(() => {
        if (circleRef.current) {
            circleRef.current.style.setProperty('--target-offset', offset);
        }
    }, [offset]);

    return (
        <div className="threat-gauge glass-card">
            <div className="panel-header">
                <h2><span className="icon">🎯</span> Threat Level</h2>
            </div>
            <div className="gauge-body">
                <div className="gauge-container" style={{ '--gauge-color': main, '--gauge-glow': glow }}>
                    <svg width="180" height="180" viewBox="0 0 180 180">
                        {/* Background track */}
                        <circle
                            cx="90" cy="90" r={radius}
                            fill="none"
                            stroke="var(--bg-tertiary)"
                            strokeWidth="10"
                            strokeLinecap="round"
                        />
                        {/* Score arc */}
                        <circle
                            ref={circleRef}
                            cx="90" cy="90" r={radius}
                            fill="none"
                            stroke={main}
                            strokeWidth="10"
                            strokeLinecap="round"
                            strokeDasharray={circumference}
                            strokeDashoffset={offset}
                            className="gauge-arc"
                            transform="rotate(-90 90 90)"
                            style={{ filter: `drop-shadow(0 0 6px ${main})` }}
                        />
                    </svg>

                    <div className="gauge-center">
                        <div className="gauge-score" style={{ color: main }}>
                            {(clampedScore * 100).toFixed(0)}
                        </div>
                        <div className="gauge-label" style={{ color: main }}>
                            {label}
                        </div>
                    </div>
                </div>

                <div className="gauge-action" style={{ '--action-color': main }}>
                    <span className="action-dot" style={{ background: main }} />
                    Action: <strong>{action.toUpperCase()}</strong>
                </div>
            </div>
        </div>
    );
}
