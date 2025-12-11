import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
from ..utils.logger import get_logger

logger = get_logger(__name__)

class EmailService:
    """Email service with retry logic and proper error handling"""
    
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    TIMEOUT = 10  # seconds
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL", "")
        self.sender_password = os.getenv("SENDER_PASSWORD", "")
        self.use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    
    def _validate_email(self, email_list):
        """Validate email addresses"""
        if not isinstance(email_list, list) or not email_list:
            return None
        
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        valid_emails = []
        
        for email in email_list:
            if isinstance(email, str) and re.match(email_pattern, email.strip()):
                valid_emails.append(email.strip())
            else:
                logger.warning(f"Invalid email format: {email}")
        
        return valid_emails if valid_emails else None
    
    def _send_smtp(self, msg, recipients):
        """Send email via SMTP with retry logic"""
        last_error = None
        
        for attempt in range(self.MAX_RETRIES):
            try:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=self.TIMEOUT)
                try:
                    if self.use_tls:
                        server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.sendmail(self.sender_email, recipients, msg.as_string())
                    server.quit()
                    return True
                except Exception as e:
                    server.quit()
                    raise e
                    
            except smtplib.SMTPAuthenticationError as e:
                logger.error(f"SMTP authentication failed: {e}")
                return False  # Don't retry on auth failure
            except (smtplib.SMTPException, OSError, TimeoutError) as e:
                last_error = e
                if attempt < self.MAX_RETRIES - 1:
                    wait_time = self.RETRY_DELAY * (2 ** attempt)
                    logger.warning(f"SMTP error, retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"SMTP failed after {self.MAX_RETRIES} attempts: {e}")
            except Exception as e:
                logger.error(f"Unexpected error sending email: {e}")
                return False
        
        return False

    def send_alert(self, subject, message, recipients):
        """Send an alert email with validation"""
        if not self.sender_email or not self.sender_password:
            logger.warning("Email credentials not configured, skipping email alert")
            return False
        
        # Validate recipients
        valid_recipients = self._validate_email(recipients if isinstance(recipients, list) else [recipients])
        if not valid_recipients:
            logger.error(f"No valid email recipients provided")
            return False
        
        try:
            # Sanitize subject and message
            subject = str(subject)[:100] if subject else "Security Alert"
            message = str(message)[:2000] if message else ""
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ", ".join(valid_recipients)
            msg['Subject'] = f"🚨 DevOps Fraud Shield Alert: {subject}"

            # Add body
            body = f"""
DevOps Fraud Shield Security Alert

{message}

This is an automated message from the DevOps Fraud Shield system.
Please investigate immediately.

---
DevOps Fraud Shield
Security Monitoring System
"""
            msg.attach(MIMEText(body, 'plain'))

            # Send email
            if self._send_smtp(msg, valid_recipients):
                logger.info(f"Alert email sent to {len(valid_recipients)} recipients")
                return True
            else:
                logger.error("Failed to send alert email")
                return False

        except Exception as e:
            logger.error(f"Error preparing alert email: {e}", exc_info=True)
            return False

    def send_report(self, subject, report_data, recipients):
        """Send a detailed security report with validation"""
        if not report_data or not isinstance(report_data, dict):
            logger.error("Invalid report data")
            return False
        
        try:
            # Validate recipients
            valid_recipients = self._validate_email(recipients if isinstance(recipients, list) else [recipients])
            if not valid_recipients:
                logger.error("No valid email recipients for report")
                return False
            
            # Sanitize subject
            subject = str(subject)[:100] if subject else "Security Report"
            
            # Format report data safely
            total_analyses = report_data.get('total_analyses', 0)
            high_risk_analyses = report_data.get('high_risk_analyses', 0)
            active_alerts = report_data.get('active_alerts', 0)
            avg_risk_score = report_data.get('average_risk_score', 0.0)
            
            message = f"""
DevOps Fraud Shield Security Report

Summary:
- Total Analyses: {total_analyses}
- High Risk Detections: {high_risk_analyses}
- Active Alerts: {active_alerts}
- Average Risk Score: {avg_risk_score:.3f}

Please review the dashboard for detailed information.
"""
            return self.send_alert(subject, message, valid_recipients)

        except Exception as e:
            logger.error(f"Error preparing report email: {e}", exc_info=True)
            return False

    def test_connection(self):
        """Test email server connection"""
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            if self.use_tls:
                server.starttls()
            if self.sender_email and self.sender_password:
                server.login(self.sender_email, self.sender_password)
            server.quit()
            logger.info("Email server connection test successful")
            return True
        except Exception as e:
            logger.error(f"Email server connection test failed: {e}")
            return False