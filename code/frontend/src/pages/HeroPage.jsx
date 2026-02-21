import { Link } from 'react-router-dom';
import { useEffect, useRef } from 'react';
import './HeroPage.css';

export default function HeroPage() {
    const statsRef = useRef(null);

    useEffect(() => {
        // Animate stat counters
        const counters = document.querySelectorAll('.stat-number');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const target = parseInt(entry.target.dataset.target);
                    animateCounter(entry.target, target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach((c) => observer.observe(c));
        return () => observer.disconnect();
    }, []);

    const animateCounter = (el, target) => {
        let current = 0;
        const step = Math.max(1, Math.floor(target / 60));
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = current.toLocaleString() + (el.dataset.suffix || '');
        }, 20);
    };

    return (
        <div className="hero-page">
            {/* Animated Background */}
            <div className="hero-bg">
                <div className="grid-overlay" />
                <div className="glow-orb orb-1" />
                <div className="glow-orb orb-2" />
                <div className="glow-orb orb-3" />
                <div className="scan-line" />
            </div>

            {/* Hero Content */}
            <section className="hero-section">
                <div className="hero-badge">
                    <span className="badge-dot" />
                    <span>Next-Gen AI Security</span>
                </div>

                <h1 className="hero-title">
                    <span className="title-line">AI Security Gateway</span>
                    <span className="title-line gradient-text">That Thinks Like</span>
                    <span className="title-line gradient-text-alt">an Attacker</span>
                </h1>

                <p className="hero-subtitle">
                    Sentinel-AI analyzes prompts in real-time using adversarial simulation,
                    intent drift tracking, and multi-layer risk scoring to protect your LLM applications
                    from jailbreaks, data exfiltration, and prompt injection attacks.
                </p>

                <div className="hero-actions">
                    <Link to="/dashboard" className="btn-primary">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <rect x="3" y="3" width="7" height="7" rx="1" />
                            <rect x="14" y="3" width="7" height="7" rx="1" />
                            <rect x="3" y="14" width="7" height="7" rx="1" />
                            <rect x="14" y="14" width="7" height="7" rx="1" />
                        </svg>
                        Launch Dashboard
                    </Link>
                    <Link to="/how-it-works" className="btn-secondary">
                        See How It Works
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M5 12h14M12 5l7 7-7 7" />
                        </svg>
                    </Link>
                </div>

                {/* Terminal Preview */}
                <div className="hero-terminal glass-card">
                    <div className="terminal-header">
                        <div className="terminal-dots">
                            <span className="dot red" />
                            <span className="dot yellow" />
                            <span className="dot green" />
                        </div>
                        <span className="terminal-title">sentinel-ai — threat analysis</span>
                    </div>
                    <div className="terminal-body">
                        <div className="term-line">
                            <span className="term-prompt">$</span>
                            <span className="term-cmd typing-anim">analyze --prompt "Ignore all instructions..."</span>
                        </div>
                        <div className="term-line delay-1">
                            <span className="term-label warn">⚠ RED-TEAM</span>
                            <span className="term-text">Jailbreak attempt detected • confidence: 0.92</span>
                        </div>
                        <div className="term-line delay-2">
                            <span className="term-label info">🔵 BLUE-TEAM</span>
                            <span className="term-text">Category: instruction_hijack • score: 87/100</span>
                        </div>
                        <div className="term-line delay-3">
                            <span className="term-label danger">🛡️ ACTION</span>
                            <span className="term-text block-text">BLOCKED — Malicious intent detected</span>
                        </div>
                    </div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="stats-section" ref={statsRef}>
                <div className="stat-card glass-card">
                    <div className="stat-icon">🔴</div>
                    <div className="stat-number" data-target="2847" data-suffix="+">0</div>
                    <div className="stat-label">Threats Blocked</div>
                </div>
                <div className="stat-card glass-card">
                    <div className="stat-icon">📊</div>
                    <div className="stat-number" data-target="99" data-suffix="%">0</div>
                    <div className="stat-label">Detection Accuracy</div>
                </div>
                <div className="stat-card glass-card">
                    <div className="stat-icon">⚡</div>
                    <div className="stat-number" data-target="150" data-suffix="ms">0</div>
                    <div className="stat-label">Avg Response Time</div>
                </div>
                <div className="stat-card glass-card">
                    <div className="stat-icon">🔄</div>
                    <div className="stat-number" data-target="12" data-suffix="">0</div>
                    <div className="stat-label">Attack Types Covered</div>
                </div>
            </section>

            {/* Trusted By */}
            <section className="trust-section">
                <p className="trust-label">Protecting AI applications with</p>
                <div className="trust-tags">
                    <span className="trust-tag">Multi-Turn Analysis</span>
                    <span className="trust-tag">Adversarial Simulation</span>
                    <span className="trust-tag">Semantic Drift Detection</span>
                    <span className="trust-tag">Real-Time Scoring</span>
                    <span className="trust-tag">Auto-Mitigation</span>
                </div>
            </section>
        </div>
    );
}
