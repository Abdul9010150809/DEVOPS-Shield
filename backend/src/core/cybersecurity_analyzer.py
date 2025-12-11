"""
Advanced Cybersecurity Features
Implements behavioral analysis, insider threat detection, and cryptographic verification
"""
import hashlib
import hmac
import re
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from ..utils.logger import get_logger
import time

logger = get_logger(__name__)


class CybersecurityAnalyzer:
    """
    Advanced cybersecurity analyzer for real-world threat detection
    Combines behavioral analysis, anomaly detection, and cryptographic verification
    """
    
    def __init__(self):
        self.user_behavior_baseline = defaultdict(dict)
        self.threat_patterns = self._load_threat_patterns()
        self.insider_threat_indicators = []
        
    def _load_threat_patterns(self) -> Dict[str, Any]:
        """Load advanced threat patterns"""
        return {
            'data_exfiltration': {
                'large_file_download': r'(download|export|backup).*\.(zip|tar|gz|sql|csv)',
                'unusual_access_time': 'access_outside_business_hours',
                'bulk_operations': 'high_volume_operations'
            },
            'credential_theft': {
                'password_file_access': r'(password|credentials|secrets|keys|\.env)',
                'auth_bypass_attempt': r'(bypass|override|admin|root)',
                'suspicious_login': 'multiple_failed_attempts'
            },
            'code_injection': {
                'sql_injection': r'(union|select|insert|update|delete).*from',
                'xss_attack': r'<script>|javascript:|onerror=',
                'command_injection': r'(\||;|`|&&|\$\()',
                'path_traversal': r'\.\./|\.\.\\',
            },
            'malware_indicators': {
                'suspicious_imports': r'(eval|exec|compile|__import__|subprocess)',
                'obfuscation': r'(base64|decode|unhexlify|rot13)',
                'reverse_shell': r'(socket|nc|netcat|reverse|shell)',
            },
            'insider_threats': {
                'mass_deletion': r'(rm -rf|delete|drop|truncate)',
                'privilege_escalation': r'(sudo|su -|chmod 777)',
                'unauthorized_access': 'access_to_restricted_resources',
            }
        }
    
    def analyze_behavioral_anomaly(self, user_id: str, commit_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze user behavior for anomalies
        
        Args:
            user_id: User identifier
            commit_data: Commit information
            
        Returns:
            Behavioral analysis results
        """
        anomalies = []
        risk_score = 0.0
        
        try:
            # Get or create baseline
            if user_id not in self.user_behavior_baseline:
                self.user_behavior_baseline[user_id] = {
                    'avg_commit_size': 0,
                    'avg_files_changed': 0,
                    'typical_commit_times': [],
                    'common_file_types': set(),
                    'commit_count': 0
                }
            
            baseline = self.user_behavior_baseline[user_id]
            
            # Analyze commit size deviation
            commit_size = commit_data.get('lines_added', 0) + commit_data.get('lines_deleted', 0)
            if baseline['commit_count'] > 5:  # Need baseline
                avg_size = baseline['avg_commit_size']
                if commit_size > avg_size * 5:  # 5x larger than average
                    anomalies.append({
                        'type': 'unusually_large_commit',
                        'severity': 'high',
                        'details': f'Commit size {commit_size} is 5x larger than average {avg_size}'
                    })
                    risk_score += 0.3
            
            # Analyze commit timing
            commit_hour = datetime.fromtimestamp(commit_data.get('timestamp', time.time())).hour
            if commit_hour < 6 or commit_hour > 22:  # Late night commits
                anomalies.append({
                    'type': 'unusual_commit_time',
                    'severity': 'medium',
                    'details': f'Commit at unusual hour: {commit_hour}:00'
                })
                risk_score += 0.2
            
            # Analyze file types
            files_changed = commit_data.get('files_changed', [])
            suspicious_files = [f for f in files_changed if self._is_sensitive_file(f)]
            if suspicious_files:
                anomalies.append({
                    'type': 'sensitive_file_access',
                    'severity': 'high',
                    'details': f'Accessed sensitive files: {suspicious_files}'
                })
                risk_score += 0.4
            
            # Update baseline
            baseline['commit_count'] += 1
            baseline['avg_commit_size'] = (
                (baseline['avg_commit_size'] * (baseline['commit_count'] - 1) + commit_size) 
                / baseline['commit_count']
            )
            
            return {
                'anomalies': anomalies,
                'risk_score': min(risk_score, 1.0),
                'baseline_updated': True,
                'user_id': user_id
            }
            
        except Exception as e:
            logger.error(f"Error in behavioral analysis: {e}", exc_info=True)
            return {'anomalies': [], 'risk_score': 0.0, 'error': str(e)}
    
    def detect_insider_threat(self, user_data: Dict[str, Any], recent_activities: List[Dict]) -> Dict[str, Any]:
        """
        Detect insider threat indicators
        
        Args:
            user_data: User profile data
            recent_activities: Recent user activities
            
        Returns:
            Insider threat assessment
        """
        threat_indicators = []
        threat_score = 0.0
        
        try:
            # Check for data exfiltration patterns
            bulk_downloads = sum(1 for a in recent_activities if a.get('type') == 'bulk_download')
            if bulk_downloads > 5:
                threat_indicators.append({
                    'type': 'data_exfiltration_risk',
                    'severity': 'critical',
                    'evidence': f'{bulk_downloads} bulk download operations'
                })
                threat_score += 0.5
            
            # Check for unusual access patterns
            failed_auths = sum(1 for a in recent_activities if a.get('type') == 'failed_auth')
            if failed_auths > 10:
                threat_indicators.append({
                    'type': 'authentication_abuse',
                    'severity': 'high',
                    'evidence': f'{failed_auths} failed authentication attempts'
                })
                threat_score += 0.3
            
            # Check for privilege escalation attempts
            priv_escalation = [a for a in recent_activities if 'privilege' in str(a.get('action', '')).lower()]
            if priv_escalation:
                threat_indicators.append({
                    'type': 'privilege_escalation',
                    'severity': 'critical',
                    'evidence': f'{len(priv_escalation)} privilege escalation attempts'
                })
                threat_score += 0.6
            
            # Check for off-hours activity
            off_hours_activity = sum(1 for a in recent_activities if self._is_off_hours(a.get('timestamp', 0)))
            if off_hours_activity > len(recent_activities) * 0.5:  # >50% off-hours
                threat_indicators.append({
                    'type': 'suspicious_work_hours',
                    'severity': 'medium',
                    'evidence': f'{off_hours_activity}/{len(recent_activities)} activities during off-hours'
                })
                threat_score += 0.2
            
            return {
                'is_insider_threat': threat_score >= 0.5,
                'threat_score': min(threat_score, 1.0),
                'indicators': threat_indicators,
                'recommendation': self._get_threat_recommendation(threat_score)
            }
            
        except Exception as e:
            logger.error(f"Error in insider threat detection: {e}", exc_info=True)
            return {'is_insider_threat': False, 'threat_score': 0.0, 'error': str(e)}
    
    def scan_for_malware_signatures(self, code_content: str, filename: str) -> Dict[str, Any]:
        """
        Scan code for malware signatures and malicious patterns
        
        Args:
            code_content: Source code content
            filename: Name of the file
            
        Returns:
            Malware scan results
        """
        detections = []
        risk_level = 0.0
        
        try:
            # Check for suspicious imports and functions
            for pattern_category, patterns in self.threat_patterns.items():
                for pattern_name, pattern_regex in patterns.items():
                    if isinstance(pattern_regex, str) and pattern_regex.startswith('('):
                        matches = re.findall(pattern_regex, code_content, re.IGNORECASE)
                        if matches:
                            detections.append({
                                'category': pattern_category,
                                'pattern': pattern_name,
                                'matches': len(matches),
                                'severity': self._get_pattern_severity(pattern_category)
                            })
                            risk_level += self._get_pattern_risk(pattern_category)
            
            # Check for obfuscation
            if self._detect_obfuscation(code_content):
                detections.append({
                    'category': 'obfuscation',
                    'pattern': 'code_obfuscation',
                    'severity': 'high'
                })
                risk_level += 0.4
            
            # Check for hardcoded credentials
            if self._detect_hardcoded_secrets(code_content):
                detections.append({
                    'category': 'credential_exposure',
                    'pattern': 'hardcoded_secrets',
                    'severity': 'high'
                })
                risk_level += 0.3
            
            return {
                'detections': detections,
                'risk_level': min(risk_level, 1.0),
                'is_malicious': risk_level >= 0.7,
                'filename': filename,
                'scan_timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Error in malware scanning: {e}", exc_info=True)
            return {'detections': [], 'risk_level': 0.0, 'error': str(e)}
    
    def verify_cryptographic_signature(self, data: str, signature: str, public_key: str) -> bool:
        """
        Verify cryptographic signature for data integrity
        
        Args:
            data: Data to verify
            signature: Cryptographic signature
            public_key: Public key for verification
            
        Returns:
            True if signature is valid
        """
        try:
            # In production, use proper cryptographic libraries (e.g., cryptography, pycryptodome)
            # This is a simplified example
            expected_signature = hashlib.sha256(data.encode()).hexdigest()
            return hmac.compare_digest(signature, expected_signature)
            
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            return False
    
    def assess_supply_chain_risk(self, dependencies: List[str]) -> Dict[str, Any]:
        """
        Assess supply chain security risks in dependencies
        
        Args:
            dependencies: List of package dependencies
            
        Returns:
            Supply chain risk assessment
        """
        risks = []
        risk_score = 0.0
        
        try:
            # Known vulnerable packages (example list)
            known_vulnerable = {
                'requests': ['2.0.0', '2.1.0'],  # Example versions
                'urllib3': ['1.25.0'],
                'pillow': ['8.0.0']
            }
            
            for dep in dependencies:
                # Parse dependency (name==version)
                parts = dep.split('==')
                if len(parts) == 2:
                    package_name, version = parts
                    
                    # Check if package is in vulnerable list
                    if package_name in known_vulnerable:
                        if version in known_vulnerable[package_name]:
                            risks.append({
                                'package': package_name,
                                'version': version,
                                'type': 'known_vulnerability',
                                'severity': 'high'
                            })
                            risk_score += 0.3
            
            # Check for typosquatting
            common_packages = ['requests', 'numpy', 'pandas', 'flask', 'django']
            for dep in dependencies:
                package_name = dep.split('==')[0] if '==' in dep else dep
                for common in common_packages:
                    if self._is_typosquatting(package_name, common):
                        risks.append({
                            'package': package_name,
                            'similar_to': common,
                            'type': 'possible_typosquatting',
                            'severity': 'critical'
                        })
                        risk_score += 0.5
            
            return {
                'risks': risks,
                'risk_score': min(risk_score, 1.0),
                'total_dependencies': len(dependencies),
                'vulnerable_count': len(risks)
            }
            
        except Exception as e:
            logger.error(f"Error in supply chain assessment: {e}", exc_info=True)
            return {'risks': [], 'risk_score': 0.0, 'error': str(e)}
    
    # Helper methods
    
    def _is_sensitive_file(self, filename: str) -> bool:
        """Check if file is sensitive"""
        sensitive_patterns = [
            '.env', 'config', 'secret', 'password', 'credential',
            'private', 'key', '.pem', '.key', 'token', 'api_key'
        ]
        return any(pattern in filename.lower() for pattern in sensitive_patterns)
    
    def _is_off_hours(self, timestamp: float) -> bool:
        """Check if timestamp is during off-hours (before 6 AM or after 10 PM)"""
        hour = datetime.fromtimestamp(timestamp).hour
        return hour < 6 or hour > 22
    
    def _get_pattern_severity(self, category: str) -> str:
        """Get severity level for pattern category"""
        severity_map = {
            'data_exfiltration': 'critical',
            'credential_theft': 'critical',
            'code_injection': 'high',
            'malware_indicators': 'high',
            'insider_threats': 'critical'
        }
        return severity_map.get(category, 'medium')
    
    def _get_pattern_risk(self, category: str) -> float:
        """Get risk score for pattern category"""
        risk_map = {
            'data_exfiltration': 0.6,
            'credential_theft': 0.7,
            'code_injection': 0.5,
            'malware_indicators': 0.5,
            'insider_threats': 0.6
        }
        return risk_map.get(category, 0.3)
    
    def _detect_obfuscation(self, code: str) -> bool:
        """Detect code obfuscation"""
        obfuscation_indicators = [
            len(re.findall(r'[a-zA-Z_]{20,}', code)) > 10,  # Very long variable names
            code.count('\\x') > 10,  # Hex escape sequences
            'base64' in code.lower() and 'decode' in code.lower(),
            code.count(';') > len(code) / 10  # Excessive semicolons
        ]
        return sum(obfuscation_indicators) >= 2
    
    def _detect_hardcoded_secrets(self, code: str) -> bool:
        """Detect hardcoded secrets"""
        secret_patterns = [
            r'password\s*=\s*["\'].*["\']',
            r'api[_-]?key\s*=\s*["\'].*["\']',
            r'secret\s*=\s*["\'].*["\']',
            r'token\s*=\s*["\'][a-zA-Z0-9]{20,}["\']'
        ]
        return any(re.search(pattern, code, re.IGNORECASE) for pattern in secret_patterns)
    
    def _is_typosquatting(self, package_name: str, common_package: str) -> bool:
        """Check for typosquatting (similar package names)"""
        if package_name == common_package:
            return False
        
        # Levenshtein distance-like check
        if len(package_name) != len(common_package):
            if abs(len(package_name) - len(common_package)) == 1:
                # Check for single character difference
                return sum(c1 != c2 for c1, c2 in zip(package_name, common_package)) <= 1
        
        return False
    
    def _get_threat_recommendation(self, threat_score: float) -> str:
        """Get recommendation based on threat score"""
        if threat_score >= 0.7:
            return "IMMEDIATE ACTION REQUIRED: Revoke access, investigate activities, contact security team"
        elif threat_score >= 0.5:
            return "HIGH PRIORITY: Enhanced monitoring, restrict permissions, conduct security review"
        elif threat_score >= 0.3:
            return "MONITOR: Increase logging, review access patterns, schedule follow-up"
        else:
            return "CONTINUE MONITORING: Maintain standard security protocols"
