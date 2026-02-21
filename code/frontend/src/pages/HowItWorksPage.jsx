import './HowItWorksPage.css';

const STEPS = [
    {
        num: '01',
        icon: '📨',
        title: 'Prompt Intake',
        desc: 'User prompt arrives at the Sentinel-AI gateway with conversation context and session metadata.',
        detail: 'POST /analyze → { prompt, conversation_id, user_id }',
    },
    {
        num: '02',
        icon: '🧬',
        title: 'Embedding Generation',
        desc: 'Prompt is converted into a high-dimensional vector embedding and compared against conversation centroid.',
        detail: 'current_embedding = embed(prompt) → cosine_distance(embedding, centroid)',
    },
    {
        num: '03',
        icon: '🔴',
        title: 'Red-Team Simulation',
        desc: 'An adversarial LLM assumes worst-case intent, identifying hidden objectives and exploitation strategies.',
        detail: '{ hidden_intent, attack_type, exploitation_strategy, confidence: 0.92 }',
    },
    {
        num: '04',
        icon: '🔵',
        title: 'Blue-Team Classification',
        desc: 'A defensive policy engine classifies the risk level and attack category with detailed reasoning.',
        detail: '{ risk_level: "malicious", attack_category: "jailbreak", score: 87 }',
    },
    {
        num: '05',
        icon: '📊',
        title: 'Unified Risk Scoring',
        desc: 'Final score computed from weighted combination: 40% blue-team + 30% drift + 30% red-team confidence.',
        detail: 'final_score = 0.4 × blue + 0.3 × drift + 0.3 × red → normalize(0–100)',
    },
    {
        num: '06',
        icon: '🛡️',
        title: 'Action & Mitigation',
        desc: 'Based on score thresholds: Allow (0–40), Warn (40–70), Rewrite (70–85), or Block (85–100).',
        detail: 'score ≥ 85 → BLOCK | score ≥ 70 → REWRITE dangerous segments',
    },
    {
        num: '07',
        icon: '✅',
        title: 'Safe Response',
        desc: 'Clean prompt forwarded to the main LLM. Response returned with full risk analysis and explanation.',
        detail: '→ { response, risk_analysis, explanation, drift_score, action_taken }',
    },
];

export default function HowItWorksPage() {
    return (
        <div className="hiw-page">
            <div className="hiw-bg">
                <div className="glow-orb hiw-orb-1" />
            </div>

            <section className="hiw-hero">
                <div className="section-badge">
                    <span>🔬 Under the Hood</span>
                </div>
                <h1 className="section-title">
                    The <span className="gradient-text">Security Pipeline</span>
                </h1>
                <p className="section-subtitle">
                    Every prompt passes through seven stages of intelligent analysis
                    before reaching the main LLM — all in under 500ms.
                </p>
            </section>

            <section className="pipeline">
                <div className="pipeline-line" />
                {STEPS.map((step, i) => (
                    <div
                        key={i}
                        className={`pipeline-step ${i % 2 === 0 ? 'left' : 'right'}`}
                        style={{ animationDelay: `${i * 0.12}s` }}
                    >
                        <div className="step-connector">
                            <div className="step-dot" />
                        </div>
                        <div className="step-card glass-card">
                            <div className="step-num">{step.num}</div>
                            <div className="step-icon">{step.icon}</div>
                            <h3 className="step-title">{step.title}</h3>
                            <p className="step-desc">{step.desc}</p>
                            <code className="step-detail">{step.detail}</code>
                        </div>
                    </div>
                ))}
            </section>
        </div>
    );
}
