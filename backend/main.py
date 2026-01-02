"""
DevOps Fraud Shield Backend - Enhanced Security & Performance Monitoring
======================================================================

A comprehensive FastAPI application for CI/CD security monitoring and fraud detection
with advanced security features, performance monitoring, and blockchain integration.
"""

import os
import sys
import asyncio
import signal
from pathlib import Path
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional

# Third-party imports
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import uvicorn

# Performance monitoring
import time
import psutil
import logging
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Security
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Application imports
from src.utils.logger import get_logger
from src.utils.config import Config
from src.utils.metrics import MetricsCollector
from src.security.audit_logger import security_audit_logger
from src.security.backup_recovery import backup_manager
from src.security.secrets_manager import secret_vault

# Initialize configuration and logging
load_dotenv()
logger = get_logger(__name__)
config = Config()

# Performance metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Active connections')
SYSTEM_MEMORY = Gauge('system_memory_usage_bytes', 'System memory usage')
SYSTEM_CPU = Gauge('system_cpu_usage_percent', 'System CPU usage')

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

# Global application state
application_state = {
    "startup_time": datetime.now(timezone.utc),
    "request_count": 0,
    "error_count": 0,
    "last_health_check": None,
    "performance_metrics": {}
}

# Ensure proper Python path
_current_dir = Path(__file__).resolve().parent
_src_dir = _current_dir / "src"
for _candidate in (_current_dir, _src_dir):
    _candidate_str = str(_candidate)
    if _candidate_str not in sys.path:
        sys.path.insert(0, _candidate_str)

# Security middleware
try:
    from src.security.https_config import SecurityHeadersMiddleware
    from src.security.request_validator import RequestValidationMiddleware
    from src.security.ip_whitelist import IPWhitelistMiddleware
    security_modules_loaded = True
    logger.info("Security modules loaded successfully")
except Exception as e:
    logger.error(f"Security modules failed to load: {e}")
    security_modules_loaded = False
    SecurityHeadersMiddleware = None
    RequestValidationMiddleware = None
    IPWhitelistMiddleware = None

# Performance monitoring middleware
try:
    from src.middleware.performance_monitor import PerformanceMonitorMiddleware
    from src.middleware.cache_middleware import CacheMiddleware
    performance_modules_loaded = True
    logger.info("Performance modules loaded successfully")
except Exception as e:
    logger.error(f"Performance modules failed to load: {e}")
    performance_modules_loaded = False
    PerformanceMonitorMiddleware = None
    CacheMiddleware = None

# Initialize metrics collector
metrics_collector = MetricsCollector()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting DevOps Fraud Shield Backend...")
    
    # Startup tasks
    try:
        # Initialize security components
        if security_modules_loaded:
            await secret_vault.initialize()
            await backup_manager.initialize()
            logger.info("Security components initialized")
        
        # Initialize performance monitoring
        if performance_modules_loaded:
            await metrics_collector.start_monitoring()
            logger.info("Performance monitoring started")
        
        # Database health check
        await check_database_health()
        
        # Blockchain connectivity check
        await check_blockchain_connectivity()
        
        application_state["startup_time"] = datetime.now(timezone.utc)
        logger.info("Application startup completed successfully")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise
    
    yield
    
    # Shutdown tasks
    logger.info("Shutting down DevOps Fraud Shield Backend...")
    
    try:
        # Cleanup resources
        if performance_modules_loaded:
            await metrics_collector.stop_monitoring()
        
        if security_modules_loaded:
            await backup_manager.cleanup()
        
        logger.info("Application shutdown completed")
        
    except Exception as e:
        logger.error(f"Shutdown error: {e}")

# Create FastAPI application
app = FastAPI(
    title="DevOps Fraud Shield API",
    version="2.0.0",
    description="Advanced CI/CD security monitoring and fraud detection platform",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    contact={
        "name": "DevOps Security Team",
        "email": "security@devops-shield.com",
        "url": "https://devops-shield.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Custom rate limit exceeded handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Custom rate limit exceeded handler with security logging"""
    client_ip = get_remote_address(request)
    security_audit_logger.log_rate_limit_violation(client_ip, request.url.path)
    
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": "Too many requests, please try again later",
            "retry_after": exc.detail.retry_after if hasattr(exc, 'detail') else 60
        }
    )

# Security middleware
app.state.limiter = limiter

# Trusted host middleware
default_allowed_hosts = "localhost,127.0.0.1,*.onrender.com,*.devops-shield.com"
allowed_hosts = [host.strip() for host in os.getenv("ALLOWED_HOSTS", default_allowed_hosts).split(",") if host.strip()]
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=allowed_hosts
)

# Security headers middleware
if security_modules_loaded and SecurityHeadersMiddleware:
    try:
        app.add_middleware(SecurityHeadersMiddleware)
        logger.info("Security headers middleware added")
    except Exception as e:
        logger.error(f"Failed to add security headers middleware: {e}")

# Request validation middleware
if security_modules_loaded and RequestValidationMiddleware:
    try:
        app.add_middleware(RequestValidationMiddleware)
        logger.info("Request validation middleware added")
    except Exception as e:
        logger.error(f"Failed to add request validation middleware: {e}")

# IP whitelist middleware (if enabled)
if security_modules_loaded and IPWhitelistMiddleware and os.getenv("IP_WHITELIST_ENABLED", "false").lower() == "true":
    try:
        app.add_middleware(IPWhitelistMiddleware)
        logger.info("IP whitelist middleware added")
    except Exception as e:
        logger.error(f"Failed to add IP whitelist middleware: {e}")

# Performance monitoring middleware
if performance_modules_loaded and PerformanceMonitorMiddleware:
    try:
        app.add_middleware(PerformanceMonitorMiddleware)
        logger.info("Performance monitoring middleware added")
    except Exception as e:
        logger.error(f"Failed to add performance monitoring middleware: {e}")

# Cache middleware
if performance_modules_loaded and CacheMiddleware:
    try:
        app.add_middleware(CacheMiddleware)
        logger.info("Cache middleware added")
    except Exception as e:
        logger.error(f"Failed to add cache middleware: {e}")

# CORS middleware (restricted)
allowed_origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000,https://devops-shield.com").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Rate-Limit-Remaining"],
    max_age=3600
)

# API Routers
def include_router_safely(router_path: str, prefix: str, tags: list, router_name: str):
    """Safely include a router with error handling"""
    try:
        if router_path.endswith('.controller'):
            module_path = f"src.api.{router_path}"
        else:
            module_path = f"src.api.{router_path}_routes"
        
        module = __import__(module_path, fromlist=['router'])
        router = getattr(module, 'router')
        
        app.include_router(router, prefix=prefix, tags=tags)
        logger.info(f"{router_name} router loaded successfully")
        return True
    except Exception as e:
        logger.error(f"{router_name} router error: {e}")
        return False

# Include all routers
routers_config = [
    ("auth_routes", "/api/auth", ["authentication"], "Authentication"),
    ("simulate_routes", "/api/simulate", ["simulation"], "Simulation"),
    ("fraud_controller", "/api/fraud", ["fraud"], "Fraud Detection"),
    ("alerts_controller", "/api/alerts", ["alerts"], "Alert Management"),
    ("pipelines_controller", "/api/pipelines", ["pipelines"], "Pipeline Monitoring"),
    ("data_controller", "/api", ["data"], "Data Management"),
    ("zero_trust_controller", "/api", ["zero-trust"], "Zero Trust"),
    ("blockchain_controller", "/api/blockchain", ["blockchain"], "Blockchain"),
    ("webhook_handler", "/api/webhooks", ["webhooks"], "Webhook Handler"),
]

for router_path, prefix, tags, router_name in routers_config:
    include_router_safely(router_path, prefix, tags, router_name)

# Enhanced health check
@app.get("/health")
@limiter.limit("100/minute")
async def health_check(request: Request) -> Dict[str, Any]:
    """Comprehensive health check endpoint with detailed system status"""
    start_time = time.time()
    
    try:
        health_status = {
            "status": "healthy",
            "service": "DevOps Shield Backend",
            "version": "2.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": (datetime.now(timezone.utc) - application_state["startup_time"]).total_seconds(),
            "request_count": application_state["request_count"],
            "error_count": application_state["error_count"],
            "cors_origins": allowed_origins,
            "rate_limiting": "enabled",
            "security_features": {
                "security_headers": security_modules_loaded,
                "request_validation": security_modules_loaded and RequestValidationMiddleware is not None,
                "ip_whitelist": security_modules_loaded and IPWhitelistMiddleware is not None,
                "audit_logging": True
            },
            "performance_features": {
                "monitoring": performance_modules_loaded,
                "caching": performance_modules_loaded and CacheMiddleware is not None,
                "metrics": True
            },
            "system_resources": {
                "memory_usage_percent": psutil.virtual_memory().percent,
                "cpu_usage_percent": psutil.cpu_percent(),
                "disk_usage_percent": psutil.disk_usage('/').percent,
                "active_connections": ACTIVE_CONNECTIONS._value.get()
            },
            "database": await check_database_status(),
            "blockchain": await check_blockchain_status(),
            "external_services": await check_external_services()
        }
        
        # Update performance metrics
        REQUEST_DURATION.observe(time.time() - start_time)
        application_state["last_health_check"] = datetime.now(timezone.utc)
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        application_state["error_count"] += 1
        
        return JSONResponse(
            status_code=503,
            content={
                "status": "degraded",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "uptime_seconds": (datetime.now(timezone.utc) - application_state["startup_time"]).total_seconds()
            }
        )

# Metrics endpoint for Prometheus
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    try:
        # Update system metrics
        SYSTEM_MEMORY.set(psutil.virtual_memory().used)
        SYSTEM_CPU.set(psutil.cpu_percent())
        
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
    except Exception as e:
        logger.error(f"Metrics collection failed: {e}")
        return Response("Metrics collection failed", status_code=500)

# Enhanced root endpoint
@app.get("/")
@limiter.limit("60/minute")
async def root(request: Request) -> Dict[str, Any]:
    """Enhanced root endpoint with application information"""
    client_info = {
        "ip": get_remote_address(request),
        "user_agent": request.headers.get("user-agent", "Unknown"),
        "request_id": request.headers.get("x-request-id", "N/A")
    }
    
    application_state["request_count"] += 1
    REQUEST_COUNT.labels(method="GET", endpoint="/", status="200").inc()
    
    return {
        "message": "DevOps Fraud Shield API - Advanced CI/CD Security Platform",
        "status": "running",
        "version": "2.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "api_docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "health_check": "/health",
        "metrics": "/metrics",
        "features": {
            "security_monitoring": True,
            "fraud_detection": True,
            "blockchain_auditing": os.getenv("BLOCKCHAIN_ENABLED", "false").lower() == "true",
            "real_time_alerts": True,
            "attack_simulation": True,
            "zero_trust_architecture": True
        },
        "client_info": client_info,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Security audit endpoint
@app.get("/api/security/audit")
@limiter.limit("30/minute")
async def security_audit(request: Request) -> Dict[str, Any]:
    """Security audit information (admin only)"""
    # In production, add proper authentication check
    client_ip = get_remote_address(request)
    
    audit_info = {
        "security_features": {
            "rate_limiting": "enabled",
            "security_headers": security_modules_loaded,
            "request_validation": security_modules_loaded and RequestValidationMiddleware is not None,
            "ip_whitelist": os.getenv("IP_WHITELIST_ENABLED", "false").lower() == "true",
            "audit_logging": True
        },
        "recent_violations": await security_audit_logger.get_recent_violations(limit=10),
        "blocked_ips": await security_audit_logger.get_blocked_ips(),
        "rate_limit_status": "active",
        "audit_timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    security_audit_logger.log_security_audit_access(client_ip)
    return audit_info

# Helper functions
async def check_database_health() -> Dict[str, Any]:
    """Check database connectivity and health"""
    try:
        # Implement actual database health check
        # For now, return mock data
        return {
            "status": "healthy",
            "connection_pool": "operational",
            "response_time_ms": "< 50",
            "last_check": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "last_check": datetime.now(timezone.utc).isoformat()
        }

async def check_database_status() -> Dict[str, Any]:
    """Detailed database status"""
    return await check_database_health()

async def check_blockchain_connectivity() -> bool:
    """Check blockchain connectivity"""
    try:
        if os.getenv("BLOCKCHAIN_ENABLED", "false").lower() == "true":
            # Implement actual blockchain connectivity check
            return True
        return False
    except Exception as e:
        logger.error(f"Blockchain connectivity check failed: {e}")
        return False

async def check_blockchain_status() -> Dict[str, Any]:
    """Detailed blockchain status"""
    try:
        if os.getenv("BLOCKCHAIN_ENABLED", "false").lower() == "true":
            return {
                "status": "connected",
                "network": os.getenv("ETHEREUM_NETWORK", "mainnet"),
                "last_block": "12345",
                "gas_price": "20 gwei",
                "last_check": datetime.now(timezone.utc).isoformat()
            }
        else:
            return {
                "status": "disabled",
                "message": "Blockchain features are disabled"
            }
    except Exception as e:
        logger.error(f"Blockchain status check failed: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

async def check_external_services() -> Dict[str, Any]:
    """Check external service connectivity"""
    services = {}
    
    # Check GitHub API
    try:
        # Implement actual GitHub API check
        services["github"] = {"status": "healthy", "response_time_ms": "< 100"}
    except Exception as e:
        services["github"] = {"status": "unhealthy", "error": str(e)}
    
    # Check Slack webhook
    try:
        # Implement actual Slack webhook check
        services["slack"] = {"status": "healthy", "last_notification": datetime.now(timezone.utc).isoformat()}
    except Exception as e:
        services["slack"] = {"status": "unhealthy", "error": str(e)}
    
    return services

# Performance monitoring middleware
@app.middleware("http")
async def performance_monitoring_middleware(request: Request, call_next):
    """Performance monitoring middleware"""
    start_time = time.time()
    
    # Update active connections
    ACTIVE_CONNECTIONS.inc()
    
    try:
        response = await call_next(request)
        
        # Record metrics
        duration = time.time() - start_time
        REQUEST_DURATION.observe(duration)
        REQUEST_COUNT.labels(
            method=request.method, 
            endpoint=request.url.path, 
            status=response.status_code
        ).inc()
        
        # Add performance headers
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        response.headers["X-Request-ID"] = f"{int(time.time() * 1000)}"
        
        return response
        
    except Exception as e:
        application_state["error_count"] += 1
        REQUEST_COUNT.labels(
            method=request.method, 
            endpoint=request.url.path, 
            status="500"
        ).inc()
        raise
    finally:
        ACTIVE_CONNECTIONS.dec()

# Graceful shutdown handling
def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    
    # Perform cleanup
    asyncio.create_task(shutdown_app())

async def shutdown_app():
    """Graceful shutdown tasks"""
    try:
        # Save application state
        logger.info("Saving application state...")
        
        # Close database connections
        logger.info("Closing database connections...")
        
        # Stop monitoring
        if performance_modules_loaded:
            await metrics_collector.stop_monitoring()
        
        logger.info("Graceful shutdown completed")
        
    except Exception as e:
        logger.error(f"Shutdown error: {e}")

# Register signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Server configuration
def create_server_config() -> Dict[str, Any]:
    """Create server configuration"""
    return {
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": int(os.getenv("PORT", 8080)),
        "workers": int(os.getenv("WORKERS", 1)),
        "reload": os.getenv("ENVIRONMENT", "development") == "development",
        "log_level": os.getenv("LOG_LEVEL", "info").lower(),
        "access_log": os.getenv("ACCESS_LOG", "true").lower() == "true",
        "ssl_keyfile": os.getenv("SSL_KEYFILE"),
        "ssl_certfile": os.getenv("SSL_CERTFILE"),
        "timeout_keep_alive": int(os.getenv("TIMEOUT_KEEP_ALIVE", 65)),
        "timeout_graceful_shutdown": int(os.getenv("TIMEOUT_GRACEFUL_SHUTDOWN", 30))
    }

# Run server
if __name__ == "__main__":
    config = create_server_config()
    
    logger.info(f"Starting DevOps Fraud Shield Backend on {config['host']}:{config['port']}")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Security modules: {'enabled' if security_modules_loaded else 'disabled'}")
    logger.info(f"Performance monitoring: {'enabled' if performance_modules_loaded else 'disabled'}")
    
    uvicorn.run(
        app,
        host=config["host"],
        port=config["port"],
        workers=config["workers"],
        reload=config["reload"],
        log_level=config["log_level"],
        access_log=config["access_log"],
        ssl_keyfile=config["ssl_keyfile"],
        ssl_certfile=config["ssl_certfile"],
        timeout_keep_alive=config["timeout_keep_alive"],
        timeout_graceful_shutdown=config["timeout_graceful_shutdown"]
    )
