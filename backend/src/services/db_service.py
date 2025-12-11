import sqlite3
import json
import os
from datetime import datetime
from threading import Lock
import time

class DBService:
    """Database service with connection pooling, retry logic, and transaction management"""
    
    MAX_RETRIES = 3
    RETRY_DELAY = 0.5  # seconds
    DB_TIMEOUT = 10  # seconds
    
    def __init__(self, db_path=None):
        
        # Use absolute path resolution
        if db_path:
            self.db_path = db_path
        elif os.getenv("DB_PATH"):
            self.db_path = os.getenv("DB_PATH")
        else:
            # From backend/src/services/ -> backend/database/
            self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../database/fraud_logs.db'))

        # Don't initialize database during import - do it lazily
        self._initialized = False
        self._logger = None
        self._lock = Lock()

    @property
    def logger(self):
        """Lazy logger initialization"""
        if self._logger is None:
            from ..utils.logger import get_logger
            self._logger = get_logger(__name__)
        return self._logger
    
    def _get_connection(self, timeout=None):
        """Get database connection with proper configuration"""
        if timeout is None:
            timeout = self.DB_TIMEOUT
        
        conn = sqlite3.connect(self.db_path, timeout=timeout, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _execute_with_retry(self, operation, *args, **kwargs):
        """Execute database operation with retry logic"""
        last_error = None
        
        for attempt in range(self.MAX_RETRIES):
            try:
                return operation(*args, **kwargs)
            except sqlite3.OperationalError as e:
                last_error = e
                if attempt < self.MAX_RETRIES - 1:
                    wait_time = self.RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                    self.logger.warning(f"Database operation failed, retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"Database operation failed after {self.MAX_RETRIES} attempts: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error in database operation: {e}")
                raise
        
        raise last_error

    def _ensure_tables(self):
        """Create database tables if they don't exist"""
        if self._initialized:
            return

        def _create_tables():
            # Ensure database directory exists
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)

            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Analysis results table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS analysis_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        repository TEXT NOT NULL,
                        timestamp REAL,
                        risk_score REAL,
                        ai_analysis TEXT,
                        rule_violations TEXT,
                        recommendations TEXT,
                        created_at REAL DEFAULT (datetime('now'))
                    )
                ''')

                # Commit analysis table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS commit_analysis (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        commit_id TEXT NOT NULL UNIQUE,
                        risk_score REAL,
                        ai_analysis TEXT,
                        rule_violations TEXT,
                        created_at REAL DEFAULT (datetime('now'))
                    )
                ''')

                # Alerts table with proper indexing
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS alerts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT NOT NULL,
                        severity TEXT,
                        message TEXT,
                        repository TEXT,
                        commit_id TEXT,
                        resolved BOOLEAN DEFAULT FALSE,
                        created_at REAL DEFAULT (datetime('now'))
                    )
                ''')
                
                # Create indexes for faster queries
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_resolved ON alerts(resolved)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_created ON alerts(created_at)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_analysis_timestamp ON analysis_results(timestamp)')

                conn.commit()
                self._initialized = True
                self.logger.info("Database tables ensured")
        
        with self._lock:
            if not self._initialized:
                self._execute_with_retry(_create_tables)

    def store_analysis_result(self, result):
        """Store repository analysis result with validation and error handling"""
        if not result:
            self.logger.warning("Attempted to store empty analysis result")
            return False
        
        self._ensure_tables()
        
        try:
            # Validate required fields
            repository = result.get('repository')
            if not repository or not isinstance(repository, str) or len(repository) > 255:
                self.logger.error(f"Invalid repository name: {repository}")
                return False
            
            risk_score = result.get('risk_score', 0.0)
            if not isinstance(risk_score, (int, float)) or risk_score < 0 or risk_score > 1:
                self.logger.error(f"Invalid risk score: {risk_score}")
                return False
            
            def _insert():
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO analysis_results
                        (repository, timestamp, risk_score, ai_analysis, rule_violations, recommendations)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        repository,
                        result.get('timestamp'),
                        risk_score,
                        json.dumps(result.get('ai_analysis', {})),
                        json.dumps(result.get('rule_violations', [])),
                        json.dumps(result.get('recommendations', []))
                    ))
                    conn.commit()
            
            self._execute_with_retry(_insert)
            self.logger.info(f"Stored analysis result for {repository}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing analysis result: {e}", exc_info=True)
            return False

    def store_commit_analysis(self, result):
        """Store individual commit analysis with validation"""
        if not result:
            self.logger.warning("Attempted to store empty commit analysis")
            return False
            
        self._ensure_tables()
        
        try:
            commit_id = result.get('commit_id')
            if not commit_id or not isinstance(commit_id, str) or len(commit_id) > 255:
                self.logger.error(f"Invalid commit ID: {commit_id}")
                return False
            
            risk_score = result.get('risk_score', 0.0)
            if not isinstance(risk_score, (int, float)) or risk_score < 0 or risk_score > 1:
                self.logger.error(f"Invalid risk score: {risk_score}")
                return False
            
            def _insert():
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT OR REPLACE INTO commit_analysis
                        (commit_id, risk_score, ai_analysis, rule_violations)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        commit_id,
                        risk_score,
                        json.dumps(result.get('ai_analysis', {})),
                        json.dumps(result.get('rule_violations', []))
                    ))
                    conn.commit()
            
            self._execute_with_retry(_insert)
            self.logger.info(f"Stored commit analysis for {commit_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing commit analysis: {e}", exc_info=True)
            return False

    def store_alert(self, alert_type, severity, message, repository=None, commit_id=None):
        """Store an alert with validation"""
        self._ensure_tables()
        
        try:
            # Validate inputs
            if not alert_type or not isinstance(alert_type, str) or len(alert_type) > 100:
                self.logger.error(f"Invalid alert type: {alert_type}")
                return False
            
            if severity not in ['low', 'medium', 'high', 'critical']:
                self.logger.error(f"Invalid severity: {severity}")
                return False
            
            if not message or not isinstance(message, str) or len(message) > 500:
                self.logger.error(f"Invalid message: {message}")
                return False
            
            def _insert():
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO alerts (type, severity, message, repository, commit_id)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (alert_type, severity, message, repository, commit_id))
                    conn.commit()
            
            self._execute_with_retry(_insert)
            self.logger.info(f"Stored alert: {alert_type} (severity: {severity})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing alert: {e}", exc_info=True)
            return False

    def get_recent_alerts(self, limit=50):
        """Get recent alerts with error handling"""
        if not isinstance(limit, int) or limit < 1 or limit > 1000:
            self.logger.warning(f"Invalid limit: {limit}, using default 50")
            limit = 50
        
        self._ensure_tables()
        
        try:
            def _fetch():
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT id, type, severity, message, repository, commit_id, resolved, created_at
                        FROM alerts
                        WHERE resolved = FALSE
                        ORDER BY created_at DESC
                        LIMIT ?
                    ''', (limit,))
                    return cursor.fetchall()
            
            rows = self._execute_with_retry(_fetch)
            alerts = []
            for row in rows:
                alerts.append({
                    "id": row[0],
                    "type": row[1],
                    "severity": row[2],
                    "message": row[3],
                    "repository": row[4],
                    "commit_id": row[5],
                    "resolved": bool(row[6]),
                    "created_at": row[7]
                })
            return alerts
            
        except Exception as e:
            self.logger.error(f"Error getting recent alerts: {e}", exc_info=True)
            return []

    def get_fraud_stats(self):
        """Get overall fraud statistics with error handling"""
        self._ensure_tables()
        
        try:
            def _fetch_stats():
                with self._get_connection() as conn:
                    cursor = conn.cursor()

                    # Get total analyses
                    cursor.execute('SELECT COUNT(*) FROM analysis_results')
                    total_analyses = cursor.fetchone()[0] or 0

                    # Get high-risk analyses
                    cursor.execute('SELECT COUNT(*) FROM analysis_results WHERE risk_score > 0.7')
                    high_risk = cursor.fetchone()[0] or 0

                    # Get recent alerts count
                    cursor.execute('SELECT COUNT(*) FROM alerts WHERE resolved = FALSE')
                    active_alerts = cursor.fetchone()[0] or 0

                    # Get average risk score
                    cursor.execute('SELECT AVG(risk_score) FROM analysis_results')
                    avg_risk = cursor.fetchone()[0] or 0.0

                    return {
                        "total_analyses": total_analyses,
                        "high_risk_analyses": high_risk,
                        "active_alerts": active_alerts,
                        "average_risk_score": round(avg_risk, 3)
                    }
            
            return self._execute_with_retry(_fetch_stats)
            
        except Exception as e:
            self.logger.error(f"Error getting fraud stats: {e}", exc_info=True)
            return {
                "total_analyses": 0,
                "high_risk_analyses": 0,
                "active_alerts": 0,
                "average_risk_score": 0.0
            }

    def resolve_alert(self, alert_id):
        """Mark an alert as resolved with validation"""
        if not isinstance(alert_id, int) or alert_id < 1:
            self.logger.error(f"Invalid alert ID: {alert_id}")
            return False
        
        try:
            def _update():
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE alerts SET resolved = TRUE WHERE id = ?', (alert_id,))
                    conn.commit()
            
            self._execute_with_retry(_update)
            self.logger.info(f"Resolved alert {alert_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error resolving alert: {e}", exc_info=True)
            return False