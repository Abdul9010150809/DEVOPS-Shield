"""
Tests for rate limiting middleware
"""
import pytest
from src.middleware.rate_limiter import RateLimiter, WebhookRateLimiter
import time


class TestRateLimiter:
    """Test rate limiter functionality"""
    
    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization"""
        limiter = RateLimiter(requests_per_minute=100)
        assert limiter.requests_per_minute == 100
    
    def test_allow_first_request(self):
        """Test allowing first request"""
        limiter = RateLimiter(requests_per_minute=5)
        
        result = limiter.is_allowed("client1")
        assert result == True
    
    def test_allow_within_limit(self):
        """Test allowing requests within limit"""
        limiter = RateLimiter(requests_per_minute=5)
        
        for i in range(5):
            result = limiter.is_allowed("client1")
            assert result == True
    
    def test_block_exceeding_limit(self):
        """Test blocking requests exceeding limit"""
        limiter = RateLimiter(requests_per_minute=3)
        
        # Allow 3 requests
        for i in range(3):
            limiter.is_allowed("client1")
        
        # 4th should be blocked
        result = limiter.is_allowed("client1")
        assert result == False
    
    def test_get_remaining(self):
        """Test getting remaining requests"""
        limiter = RateLimiter(requests_per_minute=5)
        
        limiter.is_allowed("client1")
        remaining = limiter.get_remaining("client1")
        assert remaining == 4
    
    def test_different_clients_independent(self):
        """Test that different clients have independent limits"""
        limiter = RateLimiter(requests_per_minute=3)
        
        # Client 1 uses all requests
        for i in range(3):
            limiter.is_allowed("client1")
        
        # Client 2 should still have requests available
        result = limiter.is_allowed("client2")
        assert result == True
    
    def test_cleanup_old_requests(self):
        """Test cleanup of old requests after 60 seconds"""
        limiter = RateLimiter(requests_per_minute=3)
        
        # Add requests
        for i in range(3):
            limiter.is_allowed("client1")
        
        # Should be blocked
        assert limiter.is_allowed("client1") == False
        
        # Mock time advancement
        limiter.requests["client1"][0] = time.time() - 61  # Mark as old
        
        # Should now be allowed (old request cleaned up)
        result = limiter.is_allowed("client1")
        assert result == True


class TestWebhookRateLimiter:
    """Test webhook-specific rate limiting"""
    
    def test_webhook_limiter_initialization(self):
        """Test webhook rate limiter initialization"""
        limiter = WebhookRateLimiter(requests_per_minute=50)
        assert limiter.requests_per_minute == 50
    
    def test_webhook_allow_within_limit(self):
        """Test allowing webhook requests within limit"""
        limiter = WebhookRateLimiter(requests_per_minute=5)
        
        for i in range(5):
            result = limiter.is_allowed("webhook1", "github")
            assert result == True
    
    def test_webhook_block_exceeding_limit(self):
        """Test blocking webhook requests exceeding limit"""
        limiter = WebhookRateLimiter(requests_per_minute=3)
        
        # Allow 3 requests
        for i in range(3):
            limiter.is_allowed("webhook1", "github")
        
        # 4th should be blocked
        result = limiter.is_allowed("webhook1", "github")
        assert result == False
    
    def test_webhook_different_sources_independent(self):
        """Test that different webhook sources are tracked independently"""
        limiter = WebhookRateLimiter(requests_per_minute=3)
        
        # Use all requests for one source
        for i in range(3):
            limiter.is_allowed("webhook1", "github")
        
        # Different source should have its own limit
        result = limiter.is_allowed("webhook1", "gitlab")
        assert result == True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
