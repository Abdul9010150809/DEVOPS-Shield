"""
Optimized Database Connection Pool - High Performance Database Management
========================================================================

This module provides an optimized database connection pool with connection management,
query optimization, and performance monitoring for the DevOps Shield backend.
"""

import asyncio
import time
import logging
from typing import Dict, Any, Optional, List, Union
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
import threading
from collections import defaultdict, deque
import weakref

# Database libraries (example with asyncpg for PostgreSQL)
try:
    import asyncpg
    ASYNCPG_AVAILABLE = True
except ImportError:
    ASYNCPG_AVAILABLE = False
    logging.warning("asyncpg not available, using mock database")

logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Database configuration with performance settings"""
    host: str = "localhost"
    port: int = 5432
    database: str = "devops_shield"
    username: str = "postgres"
    password: str = ""
    min_connections: int = 5
    max_connections: int = 20
    connection_timeout: float = 30.0
    query_timeout: float = 60.0
    idle_timeout: float = 300.0  # 5 minutes
    max_lifetime: float = 3600.0  # 1 hour
    retry_attempts: int = 3
    retry_delay: float = 1.0
    health_check_interval: float = 30.0
    enable_query_cache: bool = True
    query_cache_size: int = 1000
    query_cache_ttl: float = 300.0  # 5 minutes

@dataclass
class QueryMetrics:
    """Query performance metrics"""
    query: str
    duration: float
    timestamp: datetime
    rows_affected: int
    success: bool
    error_message: Optional[str] = None

class OptimizedDatabasePool:
    """High-performance database connection pool with monitoring"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._pool = None
        self._lock = asyncio.Lock()
        self._initialized = False
        
        # Performance tracking
        self._query_metrics = deque(maxlen=1000)
        self._connection_metrics = defaultdict(int)
        self._slow_queries = deque(maxlen=100)
        self._failed_queries = deque(maxlen=100)
        
        # Query cache
        self._query_cache = {}
        self._cache_access_times = {}
        self._cache_lock = threading.RLock()
        
        # Health monitoring
        self._health_status = True
        self._last_health_check = None
        self._health_check_task = None
        
        logger.info(f"Database pool initialized with config: {config}")
    
    async def initialize(self):
        """Initialize the database connection pool"""
        if self._initialized:
            return
        
        async with self._lock:
            if self._initialized:
                return
            
            try:
                if ASYNCPG_AVAILABLE:
                    self._pool = await asyncpg.create_pool(
                        host=self.config.host,
                        port=self.config.port,
                        database=self.config.database,
                        user=self.config.username,
                        password=self.config.password,
                        min_size=self.config.min_connections,
                        max_size=self.config.max_connections,
                        command_timeout=self.config.query_timeout,
                        server_settings={
                            'application_name': 'devops_shield',
                            'jit': 'off',  # Disable JIT for better performance
                        }
                    )
                    logger.info(f"Database pool created: {self.config.min_connections}-{self.config.max_connections} connections")
                else:
                    # Mock pool for development
                    self._pool = MockDatabasePool()
                    logger.info("Mock database pool created for development")
                
                self._initialized = True
                
                # Start health monitoring
                self._health_check_task = asyncio.create_task(self._health_monitor())
                
                # Test connection
                await self._test_connection()
                
                logger.info("Database pool initialized successfully")
                
            except Exception as e:
                logger.error(f"Failed to initialize database pool: {e}")
                self._health_status = False
                raise
    
    async def execute_query(self, 
                           query: str, 
                           *args, 
                           fetch: str = "all",
                           timeout: Optional[float] = None) -> Any:
        """Execute database query with performance monitoring"""
        if not self._initialized:
            await self.initialize()
        
        start_time = time.time()
        query_timeout = timeout or self.config.query_timeout
        
        # Check query cache first
        if self.config.enable_query_cache and fetch == "all" and not args:
            cached_result = self._get_cached_query(query)
            if cached_result is not None:
                logger.debug(f"Query cache hit: {query[:50]}...")
                return cached_result
        
        try:
            async with self._pool.acquire() as connection:
                # Set query timeout
                if timeout:
                    connection = connection.timeout(timeout)
                
                # Execute query based on fetch type
                if fetch == "one":
                    result = await connection.fetchrow(query, *args)
                elif fetch == "val":
                    result = await connection.fetchval(query, *args)
                elif fetch == "many":
                    result = await connection.fetch(query, *args)
                else:  # all
                    result = await connection.fetch(query, *args)
                
                # Record metrics
                duration = time.time() - start_time
                self._record_query_metrics(query, duration, True, len(result) if isinstance(result, list) else 1)
                
                # Cache result if applicable
                if (self.config.enable_query_cache and 
                    fetch == "all" and 
                    not args and 
                    duration < 1.0):  # Only cache fast queries
                    self._cache_query(query, result)
                
                logger.debug(f"Query executed in {duration:.3f}s: {query[:50]}...")
                return result
                
        except asyncio.TimeoutError:
            duration = time.time() - start_time
            self._record_query_metrics(query, duration, False, 0, "Query timeout")
            logger.error(f"Query timeout after {duration:.3f}s: {query[:50]}...")
            raise
        except Exception as e:
            duration = time.time() - start_time
            self._record_query_metrics(query, duration, False, 0, str(e))
            logger.error(f"Query failed after {duration:.3f}s: {query[:50]}... - {str(e)}")
            raise
    
    async def execute_transaction(self, queries: List[tuple]) -> Any:
        """Execute multiple queries in a transaction"""
        if not self._initialized:
            await self.initialize()
        
        start_time = time.time()
        
        try:
            async with self._pool.acquire() as connection:
                async with connection.transaction():
                    results = []
                    for query, args, fetch_type in queries:
                        if fetch_type == "one":
                            result = await connection.fetchrow(query, *args)
                        elif fetch_type == "val":
                            result = await connection.fetchval(query, *args)
                        else:
                            result = await connection.fetch(query, *args)
                        results.append(result)
                    
                    duration = time.time() - start_time
                    logger.debug(f"Transaction executed in {duration:.3f}s with {len(queries)} queries")
                    return results
                    
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Transaction failed after {duration:.3f}s: {str(e)}")
            raise
    
    @asynccontextmanager
    async def get_connection(self):
        """Get a database connection for custom operations"""
        if not self._initialized:
            await self.initialize()
        
        async with self._pool.acquire() as connection:
            yield connection
    
    async def close(self):
        """Close the database pool"""
        if self._pool and hasattr(self._pool, 'close'):
            await self._pool.close()
        
        if self._health_check_task:
            self._health_check_task.cancel()
        
        self._initialized = False
        logger.info("Database pool closed")
    
    def _record_query_metrics(self, query: str, duration: float, success: bool, rows_affected: int, error_message: str = None):
        """Record query performance metrics"""
        metrics = QueryMetrics(
            query=query[:100],  # Truncate long queries
            duration=duration,
            timestamp=datetime.now(timezone.utc),
            rows_affected=rows_affected,
            success=success,
            error_message=error_message
        )
        
        self._query_metrics.append(metrics)
        
        # Track slow queries
        if duration > 2.0:  # 2 seconds threshold
            self._slow_queries.append({
                'query': query[:100],
                'duration': duration,
                'timestamp': metrics.timestamp.isoformat()
            })
        
        # Track failed queries
        if not success:
            self._failed_queries.append({
                'query': query[:100],
                'error': error_message,
                'timestamp': metrics.timestamp.isoformat()
            })
    
    def _get_cached_query(self, query: str) -> Optional[Any]:
        """Get cached query result"""
        with self._cache_lock:
            if query not in self._query_cache:
                return None
            
            result, timestamp = self._query_cache[query]
            
            # Check if cache is expired
            if time.time() - timestamp > self.config.query_cache_ttl:
                del self._query_cache[query]
                del self._cache_access_times[query]
                return None
            
            # Update access time
            self._cache_access_times[query] = time.time()
            return result
    
    def _cache_query(self, query: str, result: Any):
        """Cache query result"""
        with self._cache_lock:
            # Remove oldest entries if cache is full
            if len(self._query_cache) >= self.config.query_cache_size:
                self._evict_oldest_cache_entries()
            
            self._query_cache[query] = (result, time.time())
            self._cache_access_times[query] = time.time()
    
    def _evict_oldest_cache_entries(self):
        """Evict oldest cache entries"""
        entries_to_remove = max(1, self.config.query_cache_size // 10)
        
        sorted_entries = sorted(
            self._cache_access_times.items(),
            key=lambda x: x[1]
        )
        
        for query, _ in sorted_entries[:entries_to_remove]:
            if query in self._query_cache:
                del self._query_cache[query]
            if query in self._cache_access_times:
                del self._cache_access_times[query]
    
    async def _test_connection(self):
        """Test database connection"""
        try:
            await self.execute_query("SELECT 1", fetch="val")
            self._health_status = True
            self._last_health_check = datetime.now(timezone.utc)
            logger.info("Database connection test successful")
        except Exception as e:
            self._health_status = False
            logger.error(f"Database connection test failed: {e}")
            raise
    
    async def _health_monitor(self):
        """Monitor database health"""
        while True:
            try:
                await asyncio.sleep(self.config.health_check_interval)
                await self._test_connection()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Database health check failed: {e}")
                self._health_status = False
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get database performance metrics"""
        if not self._query_metrics:
            return {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'total_queries': 0,
                'avg_response_time_ms': 0,
                'slow_queries_count': 0,
                'failed_queries_count': 0,
                'cache_hit_rate': 0,
                'health_status': self._health_status
            }
        
        # Calculate metrics
        total_queries = len(self._query_metrics)
        successful_queries = sum(1 for m in self._query_metrics if m.success)
        failed_queries = total_queries - successful_queries
        
        response_times = [m.duration for m in self._query_metrics if m.success]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Cache metrics
        total_cache_requests = len(self._cache_access_times)
        cache_hit_rate = (len(self._query_cache) / total_cache_requests * 100) if total_cache_requests > 0 else 0
        
        return {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'total_queries': total_queries,
            'successful_queries': successful_queries,
            'failed_queries': failed_queries,
            'avg_response_time_ms': avg_response_time * 1000,
            'slow_queries_count': len(self._slow_queries),
            'failed_queries_count': len(self._failed_queries),
            'cache_hit_rate': cache_hit_rate,
            'cache_size': len(self._query_cache),
            'health_status': self._health_status,
            'last_health_check': self._last_health_check.isoformat() if self._last_health_check else None,
            'recent_slow_queries': list(self._slow_queries)[-5:],
            'recent_failed_queries': list(self._failed_queries)[-3:]
        }

class MockDatabasePool:
    """Mock database pool for development/testing"""
    
    def __init__(self):
        self.connections = []
    
    async def acquire(self):
        return MockConnection()
    
    async def close(self):
        pass

class MockConnection:
    """Mock database connection for development/testing"""
    
    def __init__(self):
        self.timeout = lambda x: self
    
    async def fetchrow(self, query, *args):
        return {'id': 1, 'data': 'mock'}
    
    async def fetchval(self, query, *args):
        return 1
    
    async def fetch(self, query, *args):
        return [{'id': 1, 'data': 'mock'}]
    
    def transaction(self):
        return MockTransaction()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

class MockTransaction:
    """Mock transaction for development/testing"""
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

# Global database pool instance
db_pool: Optional[OptimizedDatabasePool] = None

async def get_database_pool(config: Optional[DatabaseConfig] = None) -> OptimizedDatabasePool:
    """Get or create database pool"""
    global db_pool
    if db_pool is None:
        db_pool = OptimizedDatabasePool(config or DatabaseConfig())
        await db_pool.initialize()
    return db_pool

async def close_database_pool():
    """Close database pool"""
    global db_pool
    if db_pool:
        await db_pool.close()
        db_pool = None
