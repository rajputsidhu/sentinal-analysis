import { Link } from 'react-router-dom';
import './AboutPage.css';

export default function AboutPage() {
    return (
        <div className="about-page">
            <div className="about-bg">
                <div className="glow-orb about-orb-1" />
            </div>

            <section className="about-hero">
                <div className="section-badge">
                    <span>🏛️ About Sentinel-AI</span>
                </div>
                <h1 className="section-title">
                    Built to <span className="gradient-text">Defend the Future</span> of AI
                </h1>
                <p className="section-subtitle">
                    Sentinel-AI is an open-source AI security gateway that protects LLM applications
                    from adversarial prompt attacks through real-time semantic analysis.
                </p>
            </section>

            <section className="about-grid">
                <div className="about-card glass-card">
                    <h3>🎯 Our Mission</h3>
                    <p>
                        As AI becomes ubiquitous, so do the attacks targeting it. We believe every AI application
                        deserves enterprise-grade security — the kind that doesn't just block bad words but
                        understands malicious intent evolution across conversations.
                    </p>
                </div>

                <div className="about-card glass-card">
                    <h3>🏗️ Architecture</h3>
                    <p>
                        Built on FastAPI with async-first design, Sentinel-AI processes prompts through
                        a multi-stage pipeline: embedding generation, adversarial simulation, risk classification,
                        drift detection, and intelligent mitigation — all in under 500ms.
                    </p>
                </div>

                <div className="about-card glass-card">
                    <h3>⚡ Tech Stack</h3>
                    <div className="tech-tags">
                        <span className="tech-tag">FastAPI</span>
                        <span className="tech-tag">React</span>
                        <span className="tech-tag">Groq / Llama 3.3</span>
                        <span className="tech-tag">SQLite</span>
                        <span className="tech-tag">Cosine Similarity</span>
                        <span className="tech-tag">TF-IDF</span>
                        <span className="tech-tag">Docker</span>
                        <span className="tech-tag">Vite</span>
                    </div>
                </div>

                <div className="about-card glass-card">
                    <h3>📈 What Makes Us Different</h3>
                    <ul className="about-list">
                        <li>We don't detect bad words — we detect <strong>malicious intent evolution</strong></li>
                        <li>Multi-turn conversation-aware analysis</li>
                        <li>Adversarial red-team + defensive blue-team dual LLM approach</li>
                        <li>Semantic drift detection across conversation history</li>
                        <li>Transparent, explainable security decisions</li>
                    </ul>
                </div>
            </section>

            <section className="about-cta-section">
                <div className="about-cta-card glass-card">
                    <h2>Ready to secure your AI?</h2>
                    <p>Try Sentinel-AI now — test prompts, view real-time risk analysis, and see the security pipeline in action.</p>
                    <Link to="/dashboard" className="btn-primary">
                        Launch Dashboard
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M5 12h14M12 5l7 7-7 7" />
                        </svg>
                    </Link>
                </div>
            </section>
        </div>
    );
}
