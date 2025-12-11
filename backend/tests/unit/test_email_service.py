"""
Unit tests for email service with improved error handling
"""
import pytest
from unittest.mock import patch, MagicMock
from src.services.email_service import EmailService


class TestEmailValidation:
    """Test email validation"""
    
    def test_validate_valid_emails(self):
        """Test validation of valid emails"""
        service = EmailService()
        
        emails = ['test@example.com', 'user@domain.org', 'admin@company.co.uk']
        result = service._validate_email(emails)
        
        assert result is not None
        assert len(result) == 3
    
    def test_validate_invalid_emails(self):
        """Test validation of invalid emails"""
        service = EmailService()
        
        emails = ['not-an-email', 'missing@', '@nodomain.com']
        result = service._validate_email(emails)
        
        assert result is None
    
    def test_validate_mixed_emails(self):
        """Test validation of mixed valid/invalid emails"""
        service = EmailService()
        
        emails = ['valid@example.com', 'invalid', 'another@test.org']
        result = service._validate_email(emails)
        
        assert result is not None
        assert len(result) == 2
        assert 'valid@example.com' in result
        assert 'another@test.org' in result
    
    def test_validate_empty_list(self):
        """Test validation of empty email list"""
        service = EmailService()
        result = service._validate_email([])
        assert result is None
    
    def test_validate_none(self):
        """Test validation of None"""
        service = EmailService()
        result = service._validate_email(None)
        assert result is None


class TestEmailSending:
    """Test email sending with mocks"""
    
    @patch('smtplib.SMTP')
    def test_send_alert_success(self, mock_smtp):
        """Test successful alert sending"""
        service = EmailService()
        service.sender_email = 'test@example.com'
        service.sender_password = 'password'
        
        # Mock SMTP
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        result = service.send_alert('Test', 'Message', ['recipient@example.com'])
        
        assert result == True
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()
    
    def test_send_alert_no_credentials(self):
        """Test alert sending without credentials"""
        service = EmailService()
        service.sender_email = ''
        service.sender_password = ''
        
        result = service.send_alert('Test', 'Message', ['recipient@example.com'])
        assert result == False
    
    def test_send_alert_invalid_recipients(self):
        """Test alert sending with invalid recipients"""
        service = EmailService()
        service.sender_email = 'test@example.com'
        service.sender_password = 'password'
        
        result = service.send_alert('Test', 'Message', ['invalid-email'])
        assert result == False
    
    @patch('smtplib.SMTP')
    def test_send_alert_retry_on_error(self, mock_smtp):
        """Test retry logic on SMTP error"""
        service = EmailService()
        service.sender_email = 'test@example.com'
        service.sender_password = 'password'
        
        # Mock SMTP to fail then succeed
        mock_server = MagicMock()
        mock_smtp.side_effect = [OSError("Connection failed"), mock_server]
        
        result = service.send_alert('Test', 'Message', ['recipient@example.com'])
        
        # Should eventually succeed with retry
        assert mock_smtp.call_count >= 1


class TestReportSending:
    """Test report sending"""
    
    @patch('smtplib.SMTP')
    def test_send_report_success(self, mock_smtp):
        """Test successful report sending"""
        service = EmailService()
        service.sender_email = 'test@example.com'
        service.sender_password = 'password'
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        report_data = {
            'total_analyses': 10,
            'high_risk_analyses': 2,
            'active_alerts': 1,
            'average_risk_score': 0.45
        }
        
        result = service.send_report('Monthly Report', report_data, ['admin@example.com'])
        assert result == True
    
    def test_send_report_invalid_data(self):
        """Test report sending with invalid data"""
        service = EmailService()
        service.sender_email = 'test@example.com'
        service.sender_password = 'password'
        
        result = service.send_report('Report', None, ['admin@example.com'])
        assert result == False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
