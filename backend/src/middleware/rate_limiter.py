"""Rate limiting middleware for FastAPI"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict
from threading import Lock
from ..utils.logger import get_logger

logger = get_logger(__name__)

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, requests_per_minute=100):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
        self.lock = Lock()
    
    def is_allowed(self, client_id):
        """Check if client is allowed based on rate limit"""
        current_time = time.time()
        cutoff_time = current_time - 60  # Last 60 seconds
        
        with self.lock:
            # Clean old requests
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if req_time > cutoff_time
            ]
            
            # Check limit
            if len(self.requests[client_id]) >= self.requests_per_minute:
                return False
            
            # Add current request
            self.requests[client_id].append(current_time)
            return True
    
    def get_remaining(self, client_id):
        """Get remaining requests for client"""
        current_time = time.time()
        cutoff_time = current_time - 60
        
        with self.lock:
            requests = [
                req_time for req_time in self.requests[client_id]
                if req_time > cutoff_time
            ]
            return max(0, self.requests_per_minute - len(requests))


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce rate limiting"""
    
    def __init__(self, app, requests_per_minute=100, exclude_paths=None):
        super().__init__(app)
        self.rate_limiter = RateLimiter(requests_per_minute)
        self.exclude_paths = exclude_paths or {"/health", "/docs", "/openapi.json"}
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)
        
        # Get client identifier
        client_id = request.client.host if request.client else "unknown"
        
        # Check rate limit
        if not self.rate_limiter.is_allowed(client_id):
            logger.warning(f"Rate limit exceeded for client {client_id}")
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Maximum 100 requests per minute."}
            )
        
        # Add remaining requests to response headers
        remaining = self.rate_limiter.get_remaining(client_id)
        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Limit"] = "100"
        response.headers["X-RateLimit-Window"] = "60"
        
        return response


class WebhookRateLimiter:
    """Specialized rate limiter for webhooks"""
    
    def __init__(self, requests_per_minute=50):
        self.requests_per_minute = requests_per_minute
        self.webhook_requests = defaultdict(list)
        self.lock = Lock()
    
    def is_allowed(self, webhook_id, source_id):
        """Check if webhook from source is allowed"""
        current_time = time.time()
        cutoff_time = current_time - 60
        
        key = f"{webhook_id}:{source_id}"
        
        with self.lock:
            # Clean old requests
            self.webhook_requests[key] = [
                req_time for req_time in self.webhook_requests[key]
                if req_time > cutoff_time
            ]
            
            # Check limit
            if len(self.webhook_requests[key]) >= self.requests_per_minute:
                logger.warning(f"Webhook rate limit exceeded for {key}")
                return False
            
            # Add current request
            self.webhook_requests[key].append(current_time)
            return True
