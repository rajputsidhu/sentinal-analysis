import './DriftChart.css';

export default function DriftChart({ driftHistory = [] }) {
    const maxPoints = 20;
    const data = driftHistory.slice(-maxPoints);
    const svgW = 360;
    const svgH = 120;
    const pad = { top: 10, right: 10, bottom: 25, left: 35 };
    const w = svgW - pad.left - pad.right;
    const h = svgH - pad.top - pad.bottom;

    const getColor = (val) => {
        if (val > 0.5) return 'var(--color-danger)';
        if (val > 0.2) return 'var(--color-warn)';
        return 'var(--color-safe)';
    };

    const points = data.map((d, i) => ({
        x: pad.left + (data.length > 1 ? (i / (data.length - 1)) * w : w / 2),
        y: pad.top + h - d.score * h,
        score: d.score,
        turn: d.turn,
    }));

    const linePath = points.length > 1
        ? points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ')
        : '';

    // Threshold lines
    const threshY1 = pad.top + h - 0.2 * h;
    const threshY2 = pad.top + h - 0.5 * h;

    return (
        <div className="drift-chart glass-card">
            <div className="drift-header">
                <h3>Intent Drift</h3>
                {data.length > 0 && (
                    <span className="drift-current" style={{ color: getColor(data[data.length - 1].score) }}>
                        {(data[data.length - 1].score * 100).toFixed(0)}%
                    </span>
                )}
            </div>

            {data.length === 0 ? (
                <div className="drift-empty">Send messages to track drift</div>
            ) : (
                <svg viewBox={`0 0 ${svgW} ${svgH}`} className="drift-svg">
                    {/* Grid lines */}
                    <line x1={pad.left} y1={threshY1} x2={svgW - pad.right} y2={threshY1} className="thresh-line safe" />
                    <line x1={pad.left} y1={threshY2} x2={svgW - pad.right} y2={threshY2} className="thresh-line danger" />

                    {/* Labels */}
                    <text x={pad.left - 4} y={pad.top + h + 2} className="axis-label">0</text>
                    <text x={pad.left - 4} y={threshY1 + 3} className="axis-label">0.2</text>
                    <text x={pad.left - 4} y={threshY2 + 3} className="axis-label">0.5</text>
                    <text x={pad.left - 4} y={pad.top + 4} className="axis-label">1.0</text>
                    <text x={svgW / 2} y={svgH - 2} className="axis-label-x">Turn Number</text>

                    {/* Line */}
                    {linePath && (
                        <path d={linePath} fill="none" stroke="var(--accent-blue)" strokeWidth="2" strokeLinecap="round" />
                    )}

                    {/* Dots */}
                    {points.map((p, i) => (
                        <g key={i}>
                            <circle cx={p.x} cy={p.y} r="4" fill={getColor(p.score)} stroke="none" />
                            <circle cx={p.x} cy={p.y} r="6" fill={getColor(p.score)} opacity="0.2" />
                        </g>
                    ))}
                </svg>
            )}

            <div className="drift-legend">
                <span className="legend-item"><span className="dot safe" /> Stable (&lt;0.2)</span>
                <span className="legend-item"><span className="dot warn" /> Suspicious (0.2-0.5)</span>
                <span className="legend-item"><span className="dot danger" /> Shift (&gt;0.5)</span>
            </div>
        </div>
    );
}
