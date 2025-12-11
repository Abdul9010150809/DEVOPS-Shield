import React, { useState } from 'react';
import './App.css';
import Dashboard from './pages/Dashboard.jsx';
import Pipelines from './pages/Pipelines.jsx';
import AlertsPage from './pages/Alerts.jsx';
import AuditPage from './pages/Audit.jsx';
import SettingsPage from './pages/Settings.jsx';
import ImpactPage from './pages/Impact.jsx';
import SimulationPage from './pages/Simulation.jsx';
import GitHubConnect from './pages/GitHubConnect.jsx';
import AuthBanner from './components/AuthBanner.jsx';
import {
  pipelines as pipelineData,
  runsByPipeline as runsData,
  alerts as alertData,
  auditRecords,
  impactMetrics,
  integrations,
  policyControls,
  authSession,
  securityHighlights,
  attackScenarios,
  simulationRiskHistory,
} from './utils/sampleData.js';

const VIEWS = {
  DASHBOARD: 'dashboard',
  PIPELINES: 'pipelines',
  ALERTS: 'alerts',
  AUDIT: 'audit',
  SETTINGS: 'settings',
  IMPACT: 'impact',
  SIMULATION: 'simulation',
  GITHUB: 'github'
};

const navItems = [
  { id: VIEWS.DASHBOARD, label: 'Dashboard' },
  { id: VIEWS.PIPELINES, label: 'Pipelines' },
  { id: VIEWS.ALERTS, label: 'Alerts' },
  { id: VIEWS.SIMULATION, label: 'Attack Simulation' },
  { id: VIEWS.AUDIT, label: 'Audit' },
  { id: VIEWS.SETTINGS, label: 'Settings' },
  { id: VIEWS.GITHUB, label: 'GitHub Connect' },
  { id: VIEWS.IMPACT, label: 'Societal Impact' }
];

const App = () => {
  const [view, setView] = useState(VIEWS.DASHBOARD);
  const [activePipelineId, setActivePipelineId] = useState(pipelineData[0]?.id);
  const defaultRunId = runsData[pipelineData[0]?.id]?.[0]?.runId;
  const [activeRunId, setActiveRunId] = useState(defaultRunId);
  const [alertsState, setAlertsState] = useState(alertData);
  const [authState, setAuthState] = useState(authSession);
  const [integrationsState, setIntegrationsState] = useState(integrations);
  const [latestIncident, setLatestIncident] = useState(null);

  const onSelectPipeline = (pipelineId) => {
    setActivePipelineId(pipelineId);
    const nextRunId = runsData[pipelineId]?.[0]?.runId;
    setActiveRunId(nextRunId);
    setView(VIEWS.PIPELINES);
  };

  const onSelectRun = (runId) => {
    setActiveRunId(runId);
  };

  const onRunAction = (action, payload) => {
    console.info('Run action', action, payload?.runId);
  };

  const onAlertAction = (action, payload) => {
    console.info('Alert action', action, payload?.id);
  };

  const onExport = (format, record) => {
    console.info('Export', format, record?.id);
  };

  const onReconnect = (provider) => {
    console.info('Re-authenticate provider', provider);
    const now = new Date().toISOString();
    setAuthState((prev) => ({
      ...prev,
      status: 'Connected',
      lastVerification: now
    }));
    setIntegrationsState((prev) => prev.map((integration) => (
      integration.id === 'github'
        ? { ...integration, status: 'Connected', lastSync: now }
        : integration
    )));
  };

  const handleGitHubDisconnect = () => {
    const now = new Date().toISOString();
    setAuthState((prev) => ({
      ...prev,
      status: 'Disconnected',
      lastVerification: now,
      scopes: prev.scopes || []
    }));
    setIntegrationsState((prev) => prev.map((integration) => (
      integration.id === 'github'
        ? { ...integration, status: 'Disconnected', lastSync: now }
        : integration
    )));
  };

  const handleGitHubConnect = ({ username, scopes, org }) => {
    const now = new Date().toISOString();
    setAuthState((prev) => ({
      ...prev,
      status: 'Connected',
      account: username || prev.account,
      scopes: scopes?.length ? scopes : prev.scopes,
      organization: org || prev.organization,
      lastVerification: now
    }));
    setIntegrationsState((prev) => prev.map((integration) => (
      integration.id === 'github'
        ? {
            ...integration,
            status: 'Connected',
            lastSync: now,
            scopes: scopes?.length ? scopes : integration.scopes
          }
        : integration
    )));
  };

  const onDisconnect = (provider) => {
    console.info('Disconnect provider', provider);
    handleGitHubDisconnect();
  };

  const handleSimulationIncident = (incident) => {
    const severity = incident.riskScore >= 90 ? 'Critical' : incident.riskScore >= 75 ? 'High' : 'Medium';
    const newAlert = {
      id: incident.id.toLowerCase(),
      pipelineId: incident.pipelineId,
      title: `Simulated ${incident.scenarioName}`,
      severity,
      createdAt: incident.timestamp,
      status: 'Open',
      riskScore: incident.riskScore,
      impact: incident.message || 'Automated drill impact pending review'
    };

    setAlertsState((prev) => [newAlert, ...prev]);
    setLatestIncident({ ...incident, severity });
  };

  let content;
  switch (view) {
    case VIEWS.DASHBOARD:
      content = (
        <Dashboard
          pipelines={pipelineData}
          runsByPipeline={runsData}
          alerts={alertsState}
          impactMetrics={impactMetrics}
          authSession={authState}
          securityHighlights={securityHighlights}
          integrations={integrationsState}
          latestIncident={latestIncident}
          onSelectPipeline={onSelectPipeline}
          onRunAction={onRunAction}
          onAlertAction={onAlertAction}
          onViewAlerts={() => setView(VIEWS.ALERTS)}
          onManageIntegrations={() => setView(VIEWS.GITHUB)}
        />
      );
      break;
    case VIEWS.PIPELINES:
      content = (
        <Pipelines
          pipelines={pipelineData}
          runsByPipeline={runsData}
          activePipelineId={activePipelineId}
          activeRunId={activeRunId}
          onSelectPipeline={onSelectPipeline}
          onSelectRun={onSelectRun}
          onRunAction={onRunAction}
        />
      );
      break;
    case VIEWS.ALERTS:
      content = <AlertsPage alerts={alertsState} onAction={onAlertAction} />;
      break;
    case VIEWS.AUDIT:
      content = <AuditPage records={auditRecords} onExport={onExport} />;
      break;
    case VIEWS.SETTINGS:
      content = (
        <SettingsPage
          integrations={integrationsState}
          policies={policyControls}
          authSession={authState}
          securityHighlights={securityHighlights}
        />
      );
      break;
    case VIEWS.IMPACT:
      content = <ImpactPage impactMetrics={impactMetrics} />;
      break;
    case VIEWS.SIMULATION:
      content = (
        <SimulationPage
          scenarios={attackScenarios}
          history={simulationRiskHistory}
          onIncident={handleSimulationIncident}
        />
      );
      break;
    case VIEWS.GITHUB:
      content = (
        <GitHubConnect
          authSession={authState}
          onConnect={handleGitHubConnect}
          onDisconnect={handleGitHubDisconnect}
        />
      );
      break;
    default:
      content = null;
  }

  return (
    <div className="shell">
      <aside className="shell-nav">
        <div className="nav-brand">DEVOPS SHIELD</div>
        <nav>
          {navItems.map((item) => (
            <button
              key={item.id}
              type="button"
              className={item.id === view ? 'nav-link active' : 'nav-link'}
              onClick={() => setView(item.id)}
            >
              {item.label}
            </button>
          ))}
        </nav>
        <div className="nav-footer">
          <span className="muted">Immutable by design · {new Date().getFullYear()}</span>
        </div>
      </aside>
      <main className="shell-content">
        <AuthBanner session={authState} onReconnect={onReconnect} onDisconnect={onDisconnect} />
        <header className="content-header">
          <div>
            <h1>{navItems.find((item) => item.id === view)?.label}</h1>
            <p className="muted">Production-ready CI/CD risk observability.</p>
          </div>
          <div className="header-actions">
            <button type="button" className="btn-outline" onClick={() => setView(VIEWS.SIMULATION)}>Simulate attack</button>
            <button type="button" className="btn-primary" onClick={() => setView(VIEWS.GITHUB)}>Connect GitHub</button>
          </div>
        </header>
        {latestIncident && (
          <section className={`card incident-banner ${latestIncident.severity?.toLowerCase()}`}>
            <div>
              <strong>{latestIncident.severity} alert · {latestIncident.id}</strong>
              <p className="muted">Risk {latestIncident.riskScore}% on {latestIncident.pipelineId}. {latestIncident.message}</p>
            </div>
            <div className="incident-banner-actions">
              <button type="button" className="btn-outline" onClick={() => setView(VIEWS.ALERTS)}>Open alerts</button>
            </div>
          </section>
        )}
        <div className="content-body">
          {content}
        </div>
      </main>
    </div>
  );
};

export default App;
