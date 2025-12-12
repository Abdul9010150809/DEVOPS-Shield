print("=== Starting DevOps Fraud Shield Backend ===")
print("Python path:", __file__)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import os
from dotenv import load_dotenv

print("Basic imports completed")

# ------- Logger Safe Import -------
try:
    from src.utils.logger import get_logger
    from src.utils.config import Config
    logger = get_logger(__name__)
    print("Logger loaded")
except Exception as e:
    print("Logger failed:", e)
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

load_dotenv()

# ------- Security Imports -------
try:
    from src.security.https_config import SecurityHeadersMiddleware
    from src.security.audit_logger import security_audit_logger
    from src.security.backup_recovery import backup_manager
    from src.security.secrets_manager import secret_vault
    print("Security modules loaded")
except Exception as e:
    print("Warning: Security modules failed to load:", e)
    import traceback
    traceback.print_exc()
    SecurityHeadersMiddleware = None
    security_audit_logger = None
    backup_manager = None
    secret_vault = None

# ------- Create FastAPI App -------
app = FastAPI(title="DevOps Fraud Shield API", version="1.0.0")

# ------- Security Middleware -------
# Add trusted host middleware
default_allowed_hosts = "localhost,127.0.0.1,*.onrender.com"
allowed_hosts = [host.strip() for host in os.getenv("ALLOWED_HOSTS", default_allowed_hosts).split(",") if host.strip()]
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=allowed_hosts
)

# Add security headers middleware (if available)
if SecurityHeadersMiddleware:
    try:
        app.add_middleware(SecurityHeadersMiddleware)
    except Exception as e:
        print(f"Warning: Could not add SecurityHeadersMiddleware: {e}")

# ------- Rate Limiting Middleware -------
try:
    from src.middleware.rate_limiter import RateLimiterMiddleware
    app.add_middleware(RateLimiterMiddleware)
    print("✓ Rate limiting middleware loaded")
except Exception as e:
    print(f"Warning: Rate limiting middleware failed: {e}")

# ------- CORS (Restricted) -------
allowed_origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
print(f"✓ CORS configured for: {', '.join(allowed_origins)}")

print("Including routers...")

# ------- SECURITY ROUTERS ----
try:
    from src.api.auth_routes import router as auth_router
    app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
    print("Auth router loaded successfully")
except Exception as e:
    print("Auth router error:", e)

# ---- SIMULATE ROUTER ----
try:
    from src.api import simulate_routes
    
    app.include_router(
        simulate_routes.router, 
        prefix="/api/simulate", 
        tags=["simulation"]
    )
    print("Simulate router loaded successfully (New File)")
except Exception as e:
    print("CRITICAL ERROR loading Simulate Router:", e)

try:
    from src.api.webhook_handler import router as webhook_router
    app.include_router(webhook_router, prefix="/api", tags=["webhook"])
except Exception as e:
    print("Webhook router error:", e)

try:
    from src.api.fraud_controller import router as fraud_router
    app.include_router(fraud_router, prefix="/api/fraud", tags=["fraud"])
except Exception as e:
    print("Fraud router error:", e)

try:
    from src.api.alerts_controller import router as alerts_router
    app.include_router(alerts_router, prefix="/api/alerts", tags=["alerts"])
except Exception as e:
    print("Alerts router error:", e)

try:
    from src.api.pipelines_controller import router as pipelines_router
    app.include_router(pipelines_router, prefix="/api/pipelines", tags=["pipelines"])
    print("Pipelines router loaded successfully")
except Exception as e:
    print("Pipelines router error:", e)

# ---- DATA ROUTER ----
try:
    from src.api.data_controller import router as data_router
    app.include_router(data_router, prefix="/api", tags=["data"])
    print("Data router loaded successfully")
except Exception as e:
    print("Data router error:", e)

# ---- ZERO TRUST ROUTER ----
try:
    from src.api.zero_trust_controller import router as zt_router
    app.include_router(zt_router, prefix="/api", tags=["zero-trust"])
    print("Zero Trust router loaded successfully")
except Exception as e:
    print("Zero Trust router error:", e)

# ---- BLOCKCHAIN ROUTER ----
try:
    from src.api.blockchain_controller import router as blockchain_router
    app.include_router(blockchain_router)
    print("Blockchain router loaded successfully")
except Exception as e:
    print("Blockchain router error:", e)

print("Routers loaded successfully")

# ------- Base Routes -------
@app.get("/")
async def root():
    return {"message": "DevOps Fraud Shield API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ------- Start Server -------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
