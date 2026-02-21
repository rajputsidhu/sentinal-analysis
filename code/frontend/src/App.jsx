import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import HeroPage from './pages/HeroPage';
import FeaturesPage from './pages/FeaturesPage';
import HowItWorksPage from './pages/HowItWorksPage';
import AboutPage from './pages/AboutPage';
import DashboardPage from './pages/DashboardPage';

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
}

function AppContent() {
  const location = useLocation();
  const isDashboard = location.pathname === '/dashboard';

  return (
    <>
      <Navbar />
      <ScrollToTop />
      <Routes>
        <Route path="/" element={<HeroPage />} />
        <Route path="/features" element={<FeaturesPage />} />
        <Route path="/how-it-works" element={<HowItWorksPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
      {!isDashboard && (
        <footer className="site-footer">
          <div className="footer-inner">
            <div className="footer-brand">
              <span className="footer-logo">🛡️ Sentinel-AI</span>
              <span className="footer-copy">© 2025 Sentinel-AI. AI Security Gateway.</span>
            </div>
            <div className="footer-links">
              <a href="/features">Features</a>
              <a href="/how-it-works">Architecture</a>
              <a href="/about">About</a>
              <a href="/dashboard">Dashboard</a>
            </div>
          </div>
        </footer>
      )}
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}
