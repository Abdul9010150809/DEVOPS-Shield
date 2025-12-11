from .ai_analyzer import AIAnalyzer
from .rule_engine import RuleEngine
from .risk_scorer import RiskScorer
from .cybersecurity_analyzer import CybersecurityAnalyzer
from ..utils.logger import get_logger
from ..services.db_service import DBService
from ..services.blockchain_service import BlockchainAuditService
import json

logger = get_logger(__name__)

class FraudEngine:
    def __init__(self):
        self.ai_analyzer = AIAnalyzer()
        self.rule_engine = RuleEngine()
        self.risk_scorer = RiskScorer()
        self.cybersecurity_analyzer = CybersecurityAnalyzer()
        self.db_service = DBService()
        self.blockchain_service = BlockchainAuditService()

    def analyze_repository(self, repo_data, commits):
        """Comprehensive fraud analysis with blockchain and cybersecurity"""
        logger.info(f"🔍 Starting enhanced fraud analysis for repository: {repo_data.get('name', 'unknown')}")

        # AI-based anomaly detection
        ai_results = self.ai_analyzer.analyze_commits(commits)

        # Rule-based checks
        rule_violations = self.rule_engine.check_rules(commits, repo_data)

        # Advanced cybersecurity analysis
        cybersecurity_results = []
        for commit in commits:
            behavioral = self.cybersecurity_analyzer.analyze_behavioral_anomaly(
                commit.get('author', 'unknown'),
                commit
            )
            if behavioral.get('anomalies'):
                cybersecurity_results.append(behavioral)
        
        # Calculate overall risk score
        risk_score = self.risk_scorer.calculate_risk_score(ai_results, rule_violations, repo_data)
        
        # Adjust risk score based on cybersecurity findings
        if cybersecurity_results:
            cyber_risk = sum(r.get('risk_score', 0) for r in cybersecurity_results) / len(cybersecurity_results)
            risk_score = min(1.0, risk_score + (cyber_risk * 0.3))

        # Prepare analysis result
        analysis_result = {
            "repository": repo_data.get("name", "unknown"),
            "timestamp": repo_data.get("timestamp"),
            "risk_score": risk_score,
            "ai_analysis": ai_results,
            "rule_violations": rule_violations,
            "cybersecurity_findings": cybersecurity_results,
            "recommendations": self._generate_recommendations(risk_score, rule_violations),
            "event_type": "fraud_detection"
        }

        # Store in database
        self.db_service.store_analysis_result(analysis_result)
        
        # Store on blockchain for immutable audit trail
        if risk_score >= 0.5:
            blockchain_receipt = self.blockchain_service.store_fraud_event(analysis_result)
            if blockchain_receipt:
                analysis_result['blockchain_tx'] = blockchain_receipt.get('transaction_hash')
                logger.info(f"✅ Stored on blockchain: {blockchain_receipt.get('transaction_hash', 'N/A')[:16]}...")

        # Check if alert should be triggered
        if risk_score > 0.7:
            self._trigger_alert(analysis_result)

        logger.info(f"✅ Fraud analysis completed. Risk score: {risk_score:.2f}")
        return analysis_result

    def analyze_commit(self, commit_data):
        """Analyze a single commit for fraud indicators"""
        logger.info(f"Analyzing commit: {commit_data.get('id', 'unknown')}")

        # AI analysis
        ai_result = self.ai_analyzer.analyze_commits([commit_data])

        # Rule checks
        rule_violations = self.rule_engine.check_commit_rules(commit_data)

        # Risk scoring
        risk_score = self.risk_scorer.calculate_commit_risk(ai_result, rule_violations)

        result = {
            "commit_id": commit_data.get("id"),
            "risk_score": risk_score,
            "ai_analysis": ai_result,
            "rule_violations": rule_violations
        }

        # Store commit analysis
        self.db_service.store_commit_analysis(result)

        return result

    def _generate_recommendations(self, risk_score, rule_violations):
        """Generate security recommendations based on analysis"""
        recommendations = []

        if risk_score > 0.8:
            recommendations.append("Immediate code review required")
            recommendations.append("Consider rolling back recent commits")
        elif risk_score > 0.6:
            recommendations.append("Enhanced monitoring recommended")
            recommendations.append("Review contributor access permissions")

        if "suspicious_commit_pattern" in rule_violations:
            recommendations.append("Investigate unusual commit frequency")

        if "large_file_changes" in rule_violations:
            recommendations.append("Review large code changes for malicious content")

        return recommendations

    def _trigger_alert(self, analysis_result):
        """Trigger alerts for high-risk findings"""
        from ..services.slack_service import SlackService
        from ..services.email_service import EmailService

        slack = SlackService()
        email = EmailService()

        message = f"🚨 High-risk activity detected in {analysis_result['repository']}\n"
        message += f"Risk Score: {analysis_result['risk_score']:.2f}\n"
        message += f"Violations: {len(analysis_result['rule_violations'])}"

        slack.send_alert(message)
        email.send_alert("High Risk Alert", message, ["security@company.com"])