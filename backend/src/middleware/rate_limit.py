from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from collections import defaultdict
from datetime import datetime, timedelta
import time


class RateLimiter:
    def __init__(self, requests: int = 100, window: int = 3600):
        """
        Initialize the rate limiter
        
        Args:
            requests: Number of requests allowed per window
            window: Time window in seconds
        """
        self.requests = requests
        self.window = window
        self.requests_log = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if the request is allowed based on rate limits
        
        Args:
            identifier: Unique identifier for the client (e.g., IP address)
        
        Returns:
            bool: True if request is allowed, False otherwise
        """
        now = time.time()
        # Clean old requests outside the current window
        self.requests_log[identifier] = [
            req_time for req_time in self.requests_log[identifier]
            if now - req_time < self.window
        ]
        
        # Check if the client has exceeded the limit
        if len(self.requests_log[identifier]) >= self.requests:
            return False
        
        # Add the current request to the log
        self.requests_log[identifier].append(now)
        return True


# Global rate limiter instance (in production, you might use Redis for distributed rate limiting)
rate_limiter = RateLimiter(requests=100, window=3600)  # 100 requests per hour


def check_rate_limit(request: Request) -> None:
    """
    Check rate limit for the incoming request
    
    Args:
        request: FastAPI request object
        
    Raises:
        HTTPException: If rate limit is exceeded
    """
    # Use client IP as identifier
    client_ip = request.client.host
    
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )