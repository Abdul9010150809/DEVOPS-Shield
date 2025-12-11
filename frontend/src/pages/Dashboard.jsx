import React, { useMemo } from 'react';
import RunCard from '../components/RunCard';
import RiskBadge from '../components/RiskBadge';
import AlertsTable from '../components/AlertsTable';
import ImpactMetrics from '../components/ImpactMetrics.jsx';
import SecurityHighlights from '../components/SecurityHighlights.jsx';
import { formatDateTime } from '../utils/dateHelpers';

const Dashboard = ({
  pipelines = [],
  runsByPipeline = {},
  alerts = [],
  impactMetrics = {},
  authSession,
  securityHighlights = [],
  integrations = [],
  latestIncident,
  onRunAction,
  onAlertAction,
  onSelectPipeline,
  onViewAlerts,
  onManageIntegrations
}) => {
  const allRuns = useMemo(() => Object.values(runsByPipeline).flat(), [runsByPipeline]);
  const highestRiskRun = useMemo(() => [...allRuns].sort((a, b) => (b.risk?.score || 0) - (a.risk?.score || 0))[0], [allRuns]);
  const overallRiskScore = Math.round(
    allRuns.reduce((acc, run) => acc + (run.risk?.score || 0), 0) / Math.max(allRuns.length, 1)
  );

  const topPipelines = pipelines.slice(0, 3);
  const githubIntegration = useMemo(
    () => integrations.find((integration) => integration.id === 'github'),
    [integrations]
  );

  const prioritizedAlert = useMemo(() => {
    if (!alerts.length) return null;
    const severityOrder = { Critical: 4, High: 3, Medium: 2, Low: 1 };
    return [...alerts]
      .sort((a, b) => (severityOrder[b.severity] || 0) - (severityOrder[a.severity] || 0))
      .shift();
  }, [alerts]);

  const incident = latestIncident || prioritizedAlert;
  const incidentSeverity = incident?.severity
    || (incident?.riskScore >= 90 ? 'Critical' : incident?.riskScore >= 75 ? 'High' : incident?.riskScore >= 50 ? 'Medium' : 'Low');
  const incidentTimestamp = incident?.timestamp || incident?.createdAt || null;
  const incidentAlertCount = incident?.alerts ?? (incident === prioritizedAlert ? 1 : alerts.length || 0);
  const incidentTitle = incident?.title || incident?.scenarioName || incident?.id;
  const incidentMessage = incident?.message || incident?.impact || 'Incident details pending triage.';

  return (
    <div className="grid dashboard-grid">
      <section className="card span-2">
        <header className="card-header">
          <div>
            <h2>Live risk posture</h2>
            <p className="muted">CI/CD guardrails across {pipelines.length} pipelines.</p>
          </div>
          <RiskBadge score={overallRiskScore} size="lg" />
        </header>
        <div className="dashboard-metrics">
          <div>
            <span className="label">Active pipelines</span>
            <span>{pipelines.length}</span>
          </div>
          <div>
            <span className="label">High-risk incidents</span>
            <span>{alerts.filter((alert) => alert.severity === 'High' || alert.severity === 'Critical').length}</span>
          </div>
          <div>
            <span className="label">Malicious deploys blocked</span>
            <span>{impactMetrics.blockedMaliciousDeploys ?? 0}</span>
          </div>
          <div>
            <span className="label">Critical infra pipelines</span>
            <span>{pipelines.filter((p) => p.tags?.includes('civinfra')).length}</span>
          </div>
          <div>
            <span className="label">GitHub OAuth</span>
            <span>{authSession?.status ?? 'Unknown'}</span>
          </div>
          <div>
            <span className="label">PKCE enforced</span>
            <span>{authSession?.pkce ? 'Yes' : 'Review'}</span>
          </div>
        </div>
      </section>

      {incident && (
        <section className={`card span-2 latest-incident-card severity-${incidentSeverity.toLowerCase()}`}>
          <header className="card-header">
            <div>
              <h2>{latestIncident ? 'Latest simulated incident' : 'Priority alert'}</h2>
              <p className="muted">
                {incident?.pipelineId ? `${incident.pipelineId} · ` : ''}
                {incidentTimestamp ? formatDateTime(incidentTimestamp) : 'Detected recently'}
              </p>
            </div>
            <RiskBadge score={incident.riskScore} level={incidentSeverity} />
          </header>
          <div className="incident-body">
            <div className="incident-primary">
              <h3>{incidentTitle}</h3>
              <p className="muted">{incidentMessage}</p>
            </div>
            <dl className="incident-meta">
              <div>
                <dt>Incident id</dt>
                <dd>{incident.id}</dd>
              </div>
              <div>
                <dt>Severity</dt>
                <dd>{incidentSeverity}</dd>
              </div>
              <div>
                <dt>Alerts</dt>
                <dd>{incidentAlertCount || '—'}</dd>
              </div>
            </dl>
            <div className="incident-actions">
              <button type="button" className="btn-outline" onClick={() => onViewAlerts?.()}>
                View alerts
              </button>
              {incident.pipelineId && (
                <button type="button" className="btn-link" onClick={() => onSelectPipeline?.(incident.pipelineId)}>
                  Inspect pipeline →
                </button>
              )}
            </div>
          </div>
        </section>
      )}

      <section className="card span-2">
        <header className="card-header">
          <h2>Top watch pipelines</h2>
          <p className="muted">Focus on the pipelines shaping national scale services.</p>
        </header>
        <div className="top-pipelines">
          {topPipelines.map((pipeline) => (
            <button key={pipeline.id} type="button" className="top-pipeline-card" onClick={() => onSelectPipeline?.(pipeline.id)}>
              <div className="top-pipeline-card-header">
                <h3>{pipeline.name}</h3>
                <RiskBadge score={pipeline.lastRiskScore} level={pipeline.lastRiskLevel} />
              </div>
              <p className="muted">Last run status: {pipeline.lastStatus}</p>
              <div className="tags">
                {pipeline.tags?.map((tag) => <span key={tag} className="tag">{tag}</span>)}
              </div>
              <span className="btn-link" aria-hidden="true">View pipeline -&gt;</span>
            </button>
          ))}
        </div>
      </section>

      {githubIntegration && (
        <section className="card integration-card">
          <header className="card-header">
            <div>
              <h3>GitHub integration</h3>
              <p className="muted">{githubIntegration.critical ? 'Critical connector' : 'Optional integration'}</p>
            </div>
            <span className={`badge ${githubIntegration.status === 'Connected' ? 'badge-success' : 'badge-idle'}`}>
              {githubIntegration.status}
            </span>
          </header>
          <dl className="integration-meta">
            <div>
              <dt>Last sync</dt>
              <dd>{githubIntegration.lastSync ? formatDateTime(githubIntegration.lastSync) : 'Never'}</dd>
            </div>
            <div>
              <dt>Scopes</dt>
              <dd>{githubIntegration.scopes?.join(', ') || '—'}</dd>
            </div>
            <div>
              <dt>Org coverage</dt>
              <dd>{authSession?.organization || 'Not specified'}</dd>
            </div>
          </dl>
          <p className="muted">Manage GitHub credentials or rotate tokens from the GitHub Connect workspace.</p>
          <button type="button" className="btn-outline" onClick={() => onManageIntegrations?.()}>
            Review integrations
          </button>
        </section>
      )}

      {highestRiskRun && (
        <RunCard run={highestRiskRun} onAction={onRunAction} />
      )}

      <AlertsTable alerts={alerts.slice(0, 3)} onAction={onAlertAction} />

      <ImpactMetrics data={impactMetrics} />

      <SecurityHighlights items={securityHighlights} />
    </div>
  );
};

export default Dashboard;
