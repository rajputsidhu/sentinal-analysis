import { useEffect, useRef } from 'react';
import './ThreatGauge.css';

export default function ThreatGauge({ score = 0, action = 'allow' }) {
    const circleRef = useRef(null);
    const radius = 70;
    const circumference = 2 * Math.PI * radius;
    const pct = score / 100;
    const offset = circumference - pct * circumference;

    useEffect(() => {
        if (circleRef.current) {
            circleRef.current.style.strokeDashoffset = offset;
        }
    }, [offset]);

    const getColor = () => {
        if (score >= 85) return 'var(--color-block)';
        if (score >= 70) return 'var(--color-rewrite)';
        if (score >= 40) return 'var(--color-warn)';
        return 'var(--color-safe)';
    };

    const color = getColor();

    return (
        <div className="threat-gauge glass-card">
            <h3>Threat Level</h3>
            <div className="gauge-container">
                <svg viewBox="0 0 180 180" className="gauge-svg">
                    <circle cx="90" cy="90" r={radius} className="gauge-bg" />
                    <circle
                        ref={circleRef}
                        cx="90" cy="90" r={radius}
                        className="gauge-fill"
                        style={{
                            stroke: color,
                            strokeDasharray: circumference,
                            strokeDashoffset: circumference,
                            filter: `drop-shadow(0 0 8px ${color})`,
                        }}
                    />
                </svg>
                <div className="gauge-label">
                    <span className="gauge-score" style={{ color }}>{score.toFixed(0)}</span>
                    <span className="gauge-max">/100</span>
                </div>
            </div>
            <div className="gauge-action" style={{ '--badge-color': color }}>
                {action.toUpperCase()}
            </div>
        </div>
    );
}
