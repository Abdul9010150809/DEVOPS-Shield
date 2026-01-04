/**
 * Performance Dashboard Component - Real-time Performance Monitoring
 * =================================================================
 * 
 * This component provides a comprehensive performance monitoring dashboard
 * with real-time metrics, alerts, and optimization recommendations.
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { usePerformanceMonitor, useOptimizedAsync } from '../hooks/usePerformanceMonitor';
import './PerformanceDashboard.css';

const PerformanceDashboard = () => {
  const [refreshInterval, setRefreshInterval] = useState(5000); // 5 seconds
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [selectedMetric, setSelectedMetric] = useState('overview');
  
  // Performance monitoring for this component
  const { metrics, isPerformant, getPerformanceScore, getPerformanceGrade } = usePerformanceMonitor(
    'PerformanceDashboard',
    { enableMemoryTracking: true, enableRecommendations: true }
  );
  
  // Fetch performance data with optimization
  const { result: performanceData, loading, error, execute } = useOptimizedAsync(
    async () => {
      const response = await fetch('/api/performance/dashboard');
      if (!response.ok) throw new Error('Failed to fetch performance data');
      return response.json();
    },
    [autoRefresh, refreshInterval]
  );
  
  // Auto-refresh logic
  useEffect(() => {
    if (!autoRefresh) return;
    
    const interval = setInterval(() => {
      execute();
    }, refreshInterval);
    
    return () => clearInterval(interval);
  }, [autoRefresh, refreshInterval, execute]);
  
  // Memoized metric calculations
  const metricCalculations = useMemo(() => {
    if (!performanceData) return null;
    
    const { system_metrics, database_metrics, application_metrics, performance_score } = performanceData;
    
    return {
      systemScore: calculateSystemScore(system_metrics),
      databaseScore: calculateDatabaseScore(database_metrics),
      applicationScore: calculateApplicationScore(application_metrics),
      overallScore: performance_score,
      grade: getGradeFromScore(performance_score)
    };
  }, [performanceData]);
  
  // Optimized event handlers
  const handleRefresh = useCallback(() => {
    execute();
  }, [execute]);
  
  const handleMetricChange = useCallback((metric) => {
    setSelectedMetric(metric);
  }, []);
  
  const handleIntervalChange = useCallback((interval) => {
    setRefreshInterval(interval);
  }, []);
  
  const toggleAutoRefresh = useCallback(() => {
    setAutoRefresh(prev => !prev);
  }, []);
  
  // Calculate scores
  const calculateSystemScore = (metrics) => {
    if (!metrics) return 0;
    
    let score = 100;
    const memoryPercent = metrics.memory?.used_percent || 0;
    const cpuPercent = metrics.cpu?.percent || 0;
    const diskPercent = metrics.disk?.used_percent || 0;
    
    if (memoryPercent > 80) score -= 30;
    if (cpuPercent > 80) score -= 30;
    if (diskPercent > 90) score -= 40;
    
    return Math.max(0, score);
  };
  
  const calculateDatabaseScore = (metrics) => {
    if (!metrics) return 0;
    
    let score = 100;
    const avgResponseTime = metrics.avg_response_time_ms || 0;
    const cacheHitRate = metrics.cache_hit_rate || 0;
    
    if (avgResponseTime > 1000) score -= 40;
    else if (avgResponseTime > 500) score -= 20;
    
    if (cacheHitRate < 50) score -= 30;
    else if (cacheHitRate < 70) score -= 15;
    
    return Math.max(0, score);
  };
  
  const calculateApplicationScore = (metrics) => {
    if (!metrics) return 0;
    
    let score = 100;
    const errorRate = metrics.error_rate || 0;
    const uptime = metrics.uptime_seconds || 0;
    
    if (errorRate > 5) score -= 40;
    else if (errorRate > 2) score -= 20;
    
    if (uptime < 3600) score -= 20; // Less than 1 hour
    
    return Math.max(0, score);
  };
  
  const getGradeFromScore = (score) => {
    if (score >= 90) return { grade: 'A', color: '#10b981' };
    if (score >= 80) return { grade: 'B', color: '#3b82f6' };
    if (score >= 70) return { grade: 'C', color: '#f59e0b' };
    if (score >= 60) return { grade: 'D', color: '#ef4444' };
    return { grade: 'F', color: '#dc2626' };
  };
  
  if (loading && !performanceData) {
    return (
      <div className="performance-dashboard loading">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading performance metrics...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="performance-dashboard error">
        <div className="error-message">
          <h3>Performance Monitoring Error</h3>
          <p>{error.message}</p>
          <button onClick={handleRefresh} className="retry-button">
            Retry
          </button>
        </div>
      </div>
    );
  }
  
  if (!performanceData) {
    return (
      <div className="performance-dashboard empty">
        <div className="empty-state">
          <h3>No Performance Data Available</h3>
          <p>Unable to fetch performance metrics.</p>
        </div>
      </div>
    );
  }
  
  const { grade } = metricCalculations || {};
  
  return (
    <div className="performance-dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div className="header-content">
          <h1>Performance Dashboard</h1>
          <p>Real-time system and application performance monitoring</p>
        </div>
        
        <div className="header-controls">
          <div className="overall-score">
            <div className={`score-display grade-${grade?.grade.toLowerCase()}`}>
              <span className="score-grade">{grade?.grade}</span>
              <span className="score-value">{metricCalculations?.overallScore || 0}</span>
            </div>
          </div>
          
          <div className="refresh-controls">
            <button
              onClick={toggleAutoRefresh}
              className={`toggle-button ${autoRefresh ? 'active' : ''}`}
            >
              {autoRefresh ? 'Auto-refresh ON' : 'Auto-refresh OFF'}
            </button>
            
            <select
              value={refreshInterval}
              onChange={(e) => handleIntervalChange(Number(e.target.value))}
              className="interval-select"
              disabled={!autoRefresh}
            >
              <option value={1000}>1s</option>
              <option value={5000}>5s</option>
              <option value={10000}>10s</option>
              <option value={30000}>30s</option>
            </select>
            
            <button onClick={handleRefresh} className="refresh-button">
              Refresh
            </button>
          </div>
        </div>
      </div>
      
      {/* Metric Tabs */}
      <div className="metric-tabs">
        <button
          onClick={() => handleMetricChange('overview')}
          className={`tab-button ${selectedMetric === 'overview' ? 'active' : ''}`}
        >
          Overview
        </button>
        <button
          onClick={() => handleMetricChange('system')}
          className={`tab-button ${selectedMetric === 'system' ? 'active' : ''}`}
        >
          System
        </button>
        <button
          onClick={() => handleMetricChange('database')}
          className={`tab-button ${selectedMetric === 'database' ? 'active' : ''}`}
        >
          Database
        </button>
        <button
          onClick={() => handleMetricChange('application')}
          className={`tab-button ${selectedMetric === 'application' ? 'active' : ''}`}
        >
          Application
        </button>
        <button
          onClick={() => handleMetricChange('alerts')}
          className={`tab-button ${selectedMetric === 'alerts' ? 'active' : ''}`}
        >
          Alerts
        </button>
      </div>
      
      {/* Content */}
      <div className="dashboard-content">
        {selectedMetric === 'overview' && <OverviewTab data={performanceData} />}
        {selectedMetric === 'system' && <SystemTab data={performanceData.system_metrics} />}
        {selectedMetric === 'database' && <DatabaseTab data={performanceData.database_metrics} />}
        {selectedMetric === 'application' && <ApplicationTab data={performanceData.application_metrics} />}
        {selectedMetric === 'alerts' && <AlertsTab recommendations={performanceData.recommendations} />}
      </div>
      
      {/* Footer */}
      <div className="dashboard-footer">
        <div className="footer-info">
          <span>Last updated: {new Date(performanceData.timestamp).toLocaleString()}</span>
          <span>Component performance: {getPerformanceGrade()} ({getPerformanceScore()}%)</span>
        </div>
      </div>
    </div>
  );
};

// Overview Tab Component
const OverviewTab = ({ data }) => {
  const metrics = [
    {
      title: 'System Health',
      value: data.system_metrics?.memory?.used_percent || 0,
      unit: '%',
      status: getHealthStatus(data.system_metrics?.memory?.used_percent || 0),
      icon: '💻'
    },
    {
      title: 'Database Performance',
      value: data.database_metrics?.avg_response_time_ms || 0,
      unit: 'ms',
      status: getHealthStatus(data.database_metrics?.avg_response_time_ms || 0, 1000),
      icon: '🗄️'
    },
    {
      title: 'Error Rate',
      value: data.application_metrics?.error_rate || 0,
      unit: '%',
      status: getHealthStatus(data.application_metrics?.error_rate || 0, 5),
      icon: '⚠️'
    },
    {
      title: 'Uptime',
      value: formatUptime(data.application_metrics?.uptime_seconds || 0),
      unit: '',
      status: 'healthy',
      icon: '⏱️'
    }
  ];
  
  return (
    <div className="overview-tab">
      <div className="metrics-grid">
        {metrics.map((metric, index) => (
          <div key={index} className={`metric-card ${metric.status}`}>
            <div className="metric-header">
              <span className="metric-icon">{metric.icon}</span>
              <h3>{metric.title}</h3>
            </div>
            <div className="metric-value">
              <span className="value">{metric.value}</span>
              <span className="unit">{metric.unit}</span>
            </div>
            <div className={`status-indicator ${metric.status}`}></div>
          </div>
        ))}
      </div>
      
      <div className="recommendations-section">
        <h3>Performance Recommendations</h3>
        {data.recommendations?.length > 0 ? (
          <ul className="recommendations-list">
            {data.recommendations.map((rec, index) => (
              <li key={index} className="recommendation-item">
                <span className="recommendation-icon">💡</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="no-recommendations">No performance issues detected. System is running optimally!</p>
        )}
      </div>
    </div>
  );
};

// System Tab Component
const SystemTab = ({ data }) => {
  if (!data) return <div className="no-data">No system data available</div>;
  
  return (
    <div className="system-tab">
      <div className="system-grid">
        <div className="system-card">
          <h3>Memory Usage</h3>
          <div className="progress-bar">
            <div 
              className="progress-fill memory"
              style={{ width: `${data.memory?.used_percent || 0}%` }}
            ></div>
          </div>
          <p>{data.memory?.used_gb || 0} GB / {data.memory?.total_gb || 0} GB</p>
        </div>
        
        <div className="system-card">
          <h3>CPU Usage</h3>
          <div className="progress-bar">
            <div 
              className="progress-fill cpu"
              style={{ width: `${data.cpu?.percent || 0}%` }}
            ></div>
          </div>
          <p>{data.cpu?.percent || 0}% ({data.cpu?.count || 0} cores)</p>
        </div>
        
        <div className="system-card">
          <h3>Disk Usage</h3>
          <div className="progress-bar">
            <div 
              className="progress-fill disk"
              style={{ width: `${data.disk?.used_percent || 0}%` }}
            ></div>
          </div>
          <p>{data.disk?.free_gb || 0} GB free</p>
        </div>
        
        <div className="system-card">
          <h3>Network</h3>
          <p>Connections: {data.network?.connections || 0}</p>
          <p>Sent: {formatBytes(data.network?.bytes_sent || 0)}</p>
          <p>Received: {formatBytes(data.network?.bytes_recv || 0)}</p>
        </div>
      </div>
    </div>
  );
};

// Database Tab Component
const DatabaseTab = ({ data }) => {
  if (!data) return <div className="no-data">No database data available</div>;
  
  return (
    <div className="database-tab">
      <div className="database-grid">
        <div className="database-card">
          <h3>Query Performance</h3>
          <p>Avg Response Time: {data.avg_response_time_ms || 0}ms</p>
          <p>Total Queries: {data.total_queries || 0}</p>
          <p>Success Rate: {((data.successful_queries || 0) / (data.total_queries || 1) * 100).toFixed(1)}%</p>
        </div>
        
        <div className="database-card">
          <h3>Cache Performance</h3>
          <p>Hit Rate: {data.cache_hit_rate || 0}%</p>
          <p>Cache Size: {data.cache_size || 0}</p>
          <p>Total Hits: {data.total_hits || 0}</p>
        </div>
        
        <div className="database-card">
          <h3>Connection Health</h3>
          <p>Status: {data.health_status ? 'Healthy' : 'Unhealthy'}</p>
          <p>Last Check: {data.last_health_check ? new Date(data.last_health_check).toLocaleString() : 'Never'}</p>
        </div>
      </div>
      
      {data.recent_slow_queries?.length > 0 && (
        <div className="slow-queries">
          <h3>Recent Slow Queries</h3>
          <ul>
            {data.recent_slow_queries.map((query, index) => (
              <li key={index}>
                {query.query} - {query.duration.toFixed(2)}ms
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

// Application Tab Component
const ApplicationTab = ({ data }) => {
  if (!data) return <div className="no-data">No application data available</div>;
  
  return (
    <div className="application-tab">
      <div className="application-grid">
        <div className="application-card">
          <h3>Request Statistics</h3>
          <p>Total Requests: {data.request_count || 0}</p>
          <p>Error Count: {data.error_count || 0}</p>
          <p>Error Rate: {data.error_rate || 0}%</p>
        </div>
        
        <div className="application-card">
          <h3>Uptime</h3>
          <p>{formatUptime(data.uptime_seconds || 0)}</p>
          <p>Started: {data.last_health_check ? new Date(data.last_health_check).toLocaleString() : 'Unknown'}</p>
        </div>
      </div>
    </div>
  );
};

// Alerts Tab Component
const AlertsTab = ({ recommendations }) => {
  return (
    <div className="alerts-tab">
      <h3>Performance Alerts & Recommendations</h3>
      {recommendations?.length > 0 ? (
        <div className="alerts-list">
          {recommendations.map((alert, index) => (
            <div key={index} className="alert-item warning">
              <span className="alert-icon">⚠️</span>
              <span className="alert-message">{alert}</span>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-alerts">
          <span className="success-icon">✅</span>
          <p>No performance alerts. System is running optimally!</p>
        </div>
      )}
    </div>
  );
};

// Utility functions
const getHealthStatus = (value, threshold = 80) => {
  if (value > threshold) return 'critical';
  if (value > threshold * 0.8) return 'warning';
  return 'healthy';
};

const formatUptime = (seconds) => {
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  
  if (days > 0) return `${days}d ${hours}h ${minutes}m`;
  if (hours > 0) return `${hours}h ${minutes}m`;
  return `${minutes}m`;
};

const formatBytes = (bytes) => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export default PerformanceDashboard;
