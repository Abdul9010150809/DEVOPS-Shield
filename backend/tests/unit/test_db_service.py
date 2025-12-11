"""
Unit tests for database service with improved error handling
"""
import pytest
import sqlite3
import os
import tempfile
import json
from src.services.db_service import DBService


@pytest.fixture
def temp_db():
    """Create temporary database for testing"""
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield db_path
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def db_service(temp_db):
    """Create DBService instance with temp database"""
    return DBService(db_path=temp_db)


class TestDatabaseConnection:
    """Test database connection and retry logic"""
    
    def test_connection_initialization(self, db_service):
        """Test database initialization"""
        assert db_service.db_path is not None
        assert db_service._initialized == False
    
    def test_ensure_tables(self, db_service):
        """Test table creation"""
        db_service._ensure_tables()
        assert db_service._initialized == True
        
        # Verify tables exist
        with db_service._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {row[0] for row in cursor.fetchall()}
            assert 'analysis_results' in tables
            assert 'commit_analysis' in tables
            assert 'alerts' in tables


class TestAnalysisResultStorage:
    """Test analysis result storage with validation"""
    
    def test_store_valid_analysis(self, db_service):
        """Test storing valid analysis result"""
        result = {
            'repository': 'test-repo',
            'timestamp': 1234567890,
            'risk_score': 0.75,
            'ai_analysis': {'anomaly_score': 0.7},
            'rule_violations': ['rule1'],
            'recommendations': ['review code']
        }
        
        success = db_service.store_analysis_result(result)
        assert success == True
        
        # Verify stored
        db_service._ensure_tables()
        with db_service._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM analysis_results WHERE repository = ?", ("test-repo",))
            count = cursor.fetchone()[0]
            assert count == 1
    
    def test_store_invalid_repository_name(self, db_service):
        """Test storing with invalid repository name"""
        result = {
            'repository': None,
            'timestamp': 1234567890,
            'risk_score': 0.75
        }
        
        success = db_service.store_analysis_result(result)
        assert success == False
    
    def test_store_invalid_risk_score(self, db_service):
        """Test storing with invalid risk score"""
        result = {
            'repository': 'test-repo',
            'timestamp': 1234567890,
            'risk_score': 1.5  # Invalid: > 1.0
        }
        
        success = db_service.store_analysis_result(result)
        assert success == False
    
    def test_store_empty_result(self, db_service):
        """Test storing empty result"""
        success = db_service.store_analysis_result(None)
        assert success == False


class TestCommitAnalysisStorage:
    """Test commit analysis storage"""
    
    def test_store_valid_commit(self, db_service):
        """Test storing valid commit analysis"""
        result = {
            'commit_id': 'abc123',
            'risk_score': 0.5,
            'ai_analysis': {'anomaly_score': 0.4},
            'rule_violations': []
        }
        
        success = db_service.store_commit_analysis(result)
        assert success == True
    
    def test_store_invalid_commit_id(self, db_service):
        """Test storing with invalid commit ID"""
        result = {
            'commit_id': None,
            'risk_score': 0.5
        }
        
        success = db_service.store_commit_analysis(result)
        assert success == False
    
    def test_duplicate_commit_replaced(self, db_service):
        """Test that duplicate commits are replaced"""
        result1 = {'commit_id': 'abc123', 'risk_score': 0.3}
        result2 = {'commit_id': 'abc123', 'risk_score': 0.7}
        
        db_service.store_commit_analysis(result1)
        db_service.store_commit_analysis(result2)
        
        # Verify only one entry with latest score
        db_service._ensure_tables()
        with db_service._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT risk_score FROM commit_analysis WHERE commit_id = ?", ("abc123",))
            rows = cursor.fetchall()
            assert len(rows) == 1
            assert rows[0][0] == 0.7


class TestAlertStorage:
    """Test alert storage"""
    
    def test_store_valid_alert(self, db_service):
        """Test storing valid alert"""
        success = db_service.store_alert(
            'test_alert',
            'high',
            'Test alert message',
            repository='test-repo',
            commit_id='abc123'
        )
        assert success == True
    
    def test_store_invalid_severity(self, db_service):
        """Test storing with invalid severity"""
        success = db_service.store_alert(
            'test_alert',
            'invalid_severity',
            'Test message'
        )
        assert success == False
    
    def test_get_recent_alerts(self, db_service):
        """Test retrieving recent alerts"""
        db_service.store_alert('alert1', 'high', 'Message 1')
        db_service.store_alert('alert2', 'medium', 'Message 2')
        
        alerts = db_service.get_recent_alerts(limit=10)
        assert len(alerts) >= 2
    
    def test_resolve_alert(self, db_service):
        """Test resolving an alert"""
        db_service.store_alert('alert1', 'high', 'Message')
        
        # Get the alert ID
        alerts = db_service.get_recent_alerts()
        alert_id = alerts[0]['id']
        
        # Resolve it
        success = db_service.resolve_alert(alert_id)
        assert success == True


class TestFraudStats:
    """Test fraud statistics retrieval"""
    
    def test_get_fraud_stats(self, db_service):
        """Test getting fraud statistics"""
        # Add some data
        db_service.store_analysis_result({
            'repository': 'repo1',
            'risk_score': 0.8,
            'timestamp': 1234567890
        })
        
        db_service.store_analysis_result({
            'repository': 'repo2',
            'risk_score': 0.3,
            'timestamp': 1234567891
        })
        
        db_service.store_alert('alert1', 'high', 'Message')
        
        stats = db_service.get_fraud_stats()
        assert stats['total_analyses'] == 2
        assert stats['high_risk_analyses'] == 1
        assert stats['active_alerts'] == 1
        assert stats['average_risk_score'] == pytest.approx(0.55, abs=0.01)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
