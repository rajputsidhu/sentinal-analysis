import './FeaturesPage.css';

const FEATURES = [
    {
        icon: '🔴',
        title: 'Red-Team Simulation',
        description: 'An adversarial LLM assumes the user is malicious, identifying hidden objectives, attack strategies, and exploitation vectors with confidence scoring.',
        tag: 'Adversarial AI',
        color: '#f87171',
    },
    {
        icon: '🔵',
        title: 'Blue-Team Classification',
        description: 'A defensive policy engine classifies prompts into attack categories — jailbreak, data exfiltration, instruction hijack, tool abuse — with detailed risk explanations.',
        tag: 'Defense Engine',
        color: '#6c9eff',
    },
    {
        icon: '📊',
        title: 'Intent Drift Detection',
        description: 'Tracks semantic drift across multi-turn conversations using embedding centroids and cosine distance to detect gradual escalation patterns.',
        tag: 'Semantic Analysis',
        color: '#a78bfa',
    },
    {
        icon: '🛡️',
        title: 'Smart Mitigation',
        description: 'Automatically rewrites dangerous prompts to preserve legitimate intent while removing malicious payloads. Supports allow, warn, rewrite, and block actions.',
        tag: 'Auto-Response',
        color: '#34d399',
    },
    {
        icon: '🧠',
        title: 'Conversation Memory',
        description: 'Maintains full conversation context with embedding history and centroid tracking, enabling detection of sophisticated multi-turn attack chains.',
        tag: 'Context-Aware',
        color: '#fbbf24',
    },
    {
        icon: '💡',
        title: 'Explainable AI',
        description: 'Generates human-readable explanations for every security decision — why a prompt was flagged, what dangerous segments were detected, and intent evolution.',
        tag: 'Transparency',
        color: '#f472b6',
    },
];

export default function FeaturesPage() {
    return (
        <div className="features-page">
            <div className="features-bg">
                <div className="glow-orb feat-orb-1" />
                <div className="glow-orb feat-orb-2" />
            </div>

            <section className="features-hero">
                <div className="section-badge">
                    <span>✨ Core Capabilities</span>
                </div>
                <h1 className="section-title">
                    Six Layers of <span className="gradient-text">Intelligent Defense</span>
                </h1>
                <p className="section-subtitle">
                    Each component works in concert to provide comprehensive, real-time protection
                    against the most sophisticated AI prompt attacks.
                </p>
            </section>

            <section className="features-grid">
                {FEATURES.map((feat, i) => (
                    <div
                        key={i}
                        className="feature-card glass-card"
                        style={{ '--accent': feat.color, animationDelay: `${i * 0.1}s` }}
                    >
                        <div className="feature-icon-wrap">
                            <span className="feature-icon">{feat.icon}</span>
                        </div>
                        <div className="feature-tag" style={{ color: feat.color, borderColor: `${feat.color}33` }}>
                            {feat.tag}
                        </div>
                        <h3 className="feature-title">{feat.title}</h3>
                        <p className="feature-desc">{feat.description}</p>
                        <div className="feature-glow" style={{ background: `radial-gradient(circle, ${feat.color}10, transparent)` }} />
                    </div>
                ))}
            </section>
        </div>
    );
}
