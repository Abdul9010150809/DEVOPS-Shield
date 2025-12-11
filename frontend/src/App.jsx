import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import Alerts from './components/Alerts';
import PipelineMonitor from './components/PipelineMonitor';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [stats, setStats] = useState({
    total_analyses: 1240,
    high_risk_analyses: 3,
    active_alerts: 2,
    average_risk_score: 0.12
  });
  const [isOnline, setIsOnline] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 30000);

    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      clearInterval(interval);
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const fetchStats = async () => {
    try {
      const apiUrl = process.env.REACT_APP_API_URL || '';
      const response = await fetch(`${apiUrl}/api/fraud/stats`);
      if (response.ok) {
        const data = await response.json();
        setStats(data.data || data);
        setLastUpdate(new Date());
        setIsOnline(true);
      } else {
        setIsOnline(false);
      }
    } catch (error) {
      console.warn('API unavailable, using mock data');
      setIsOnline(false);
    }
  };

  const tabs = [
    { id: 'dashboard', label: '🏠 Dashboard', icon: '🛡️' },
    { id: 'pipelines', label: '🚀 CI/CD Pipelines', icon: '⚙️' },
    { id: 'alerts', label: '🚨 Alerts', icon: '🔔', badge: stats.active_alerts }
  ];

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%)',
      fontFamily: 'Inter, system-ui, sans-serif',
      color: '#f8fafc'
    }}>
      
      {/* Top Navigation Bar */}
      <nav style={{
        background: 'rgba(15, 23, 42, 0.95)',
        backdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        padding: '0 24px',
        position: 'sticky',
        top: 0,
        zIndex: 1000,
        boxShadow: '0 4px 24px rgba(0, 0, 0, 0.4)'
      }}>
        <div style={{
          maxWidth: '1800px',
          margin: '0 auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          height: '70px'
        }}>
          
          {/* Logo & Brand */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '16px'
          }}>
            <div style={{
              width: '48px',
              height: '48px',
              background: 'linear-gradient(135deg, #3b82f6, #10b981)',
              borderRadius: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem',
              boxShadow: '0 8px 24px rgba(59, 130, 246, 0.4)'
            }}>
              🛡️
            </div>
            <div>
              <h1 style={{
                margin: 0,
                fontSize: '1.4rem',
                fontWeight: 900,
                background: 'linear-gradient(135deg, #3b82f6, #10b981)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                letterSpacing: '-0.5px'
              }}>
                DEVOPS-SHIELD
              </h1>
              <p style={{
                margin: 0,
                fontSize: '0.75rem',
                color: '#64748b',
                fontWeight: 500,
                letterSpacing: '1px',
                textTransform: 'uppercase'
              }}>
                Blockchain Security Platform
              </p>
            </div>
          </div>

          {/* Tab Navigation */}
          <div style={{
            display: 'flex',
            gap: '8px',
            background: 'rgba(30, 41, 59, 0.5)',
            padding: '6px',
            borderRadius: '12px',
            border: '1px solid rgba(255, 255, 255, 0.05)'
          }}>
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  background: activeTab === tab.id
                    ? 'linear-gradient(135deg, #3b82f6, #2563eb)'
                    : 'transparent',
                  border: 'none',
                  color: activeTab === tab.id ? 'white' : '#94a3b8',
                  padding: '10px 20px',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                  fontWeight: 600,
                  transition: 'all 0.3s ease',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  position: 'relative',
                  boxShadow: activeTab === tab.id
                    ? '0 4px 16px rgba(59, 130, 246, 0.4)'
                    : 'none'
                }}
                onMouseEnter={e => {
                  if (activeTab !== tab.id) {
                    e.currentTarget.style.background = 'rgba(59, 130, 246, 0.1)';
                    e.currentTarget.style.color = '#e2e8f0';
                  }
                }}
                onMouseLeave={e => {
                  if (activeTab !== tab.id) {
                    e.currentTarget.style.background = 'transparent';
                    e.currentTarget.style.color = '#94a3b8';
                  }
                }}>
                {tab.label}
                {tab.badge > 0 && (
                  <span style={{
                    background: '#ef4444',
                    color: 'white',
                    fontSize: '0.7rem',
                    fontWeight: 700,
                    padding: '2px 8px',
                    borderRadius: '12px',
                    minWidth: '20px',
                    textAlign: 'center',
                    boxShadow: '0 2px 8px rgba(239, 68, 68, 0.4)'
                  }}>
                    {tab.badge}
                  </span>
                )}
              </button>
            ))}
          </div>

          {/* Status Indicator */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            background: isOnline 
              ? 'rgba(16, 185, 129, 0.1)' 
              : 'rgba(239, 68, 68, 0.1)',
            padding: '8px 16px',
            borderRadius: '8px',
            border: `1px solid ${isOnline ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`
          }}>
            <div style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              background: isOnline ? '#10b981' : '#ef4444',
              boxShadow: `0 0 12px ${isOnline ? '#10b981' : '#ef4444'}`,
              animation: 'pulse 2s infinite'
            }}/>
            <span style={{
              fontSize: '0.85rem',
              fontWeight: 600,
              color: isOnline ? '#10b981' : '#ef4444'
            }}>
              {isOnline ? 'ONLINE' : 'OFFLINE'}
            </span>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main style={{
        padding: '0',
        minHeight: 'calc(100vh - 70px)'
      }}>
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'pipelines' && <PipelineMonitor />}
        {activeTab === 'alerts' && <Alerts />}
      </main>

      {/* CSS Animations */}
      <style>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.5;
          }
        }

        @keyframes slideIn {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }

        * {
          scrollbar-width: thin;
          scrollbar-color: rgba(59, 130, 246, 0.5) rgba(30, 41, 59, 0.3);
        }

        *::-webkit-scrollbar {
          width: 8px;
          height: 8px;
        }

        *::-webkit-scrollbar-track {
          background: rgba(30, 41, 59, 0.3);
          border-radius: 4px;
        }

        *::-webkit-scrollbar-thumb {
          background: rgba(59, 130, 246, 0.5);
          border-radius: 4px;
        }

        *::-webkit-scrollbar-thumb:hover {
          background: rgba(59, 130, 246, 0.7);
        }
      `}</style>
    </div>
  );
}

export default App;