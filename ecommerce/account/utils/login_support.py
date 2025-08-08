import hashlib
import time
from datetime import timedelta
from functools import wraps
from typing import Any, Callable

from django.core.cache import cache
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response


class LoginSupport:
    """
    Have utils support for login api
    """
    
    def __init__(self) -> None:
        self.cache_key: str = ""
        self.max_calls: int = 0
    
    def get_client_ip(self, request: Request) -> str:
        """
        Gets the Client ip address, from request META data
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
            
        return ip

    
    # TODO: Make this using REDIS cache.
    def login_limiter(self, wrong_attempts_allowed: int, period: timedelta):
        """Limits the user to perform the decorated method for `period` time, after `wrong_attempts_allowed` are performed by user.

        Args:
            wrong_attempts_allowed (int): Number of calls to be allowed.
            period (timedelta): After how much time user can again make call, once api ratelimit is set.
        """
        def decorator(func: Callable) -> Callable:
            
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                
                request: Request | None = None
                self.max_calls = wrong_attempts_allowed
                
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
                    
                if request is None:
                    request = kwargs.get('request')
                    
                if not request or not isinstance(request, Request):
                    raise ValueError("Request Not found in parameters!!")
                
                
                ip_address: str = self.get_client_ip(request)
                print(ip_address)
                
                # Creating unique identifier for the client
                # can be used to store more data in that hash in future
                unique_hashed_id = hashlib.md5((ip_address).encode()).hexdigest()
                self.cache_key = f"rate_limit:{unique_hashed_id}"
                
                timestamps: list[float] = cache.get(self.cache_key, [])
                
                # update the timestamps
                now = time.time()
                period_seconds = period.total_seconds()
                timestamps = [t for t in timestamps if now - t < period_seconds]
                
                if len(timestamps) < wrong_attempts_allowed:
                    timestamps.append(now)
                    cache.set(
                        key=self.cache_key, 
                        value=timestamps, 
                        timeout=int(period_seconds)
                    )
                    return func(*args, **kwargs)
                
                # calculate the time to wait before the next request
                wait = period_seconds - (now - timestamps[0])
                print("Wait time: ", wait)
                
                return Response(
                    data = f"Rate limit exceeded. Retry after {wait:.2f} seconds.",
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )
                
            return wrapper
        
        return decorator



    def attempts_left(self, request: Request) -> int:
        """Gets How many more attempts left for user to login before it blocks

        Args:
            request (Request): Give request header here.

        Returns:
            int: Number of attempts left to login
        """
        timestamps : list[float] = cache.get(self.cache_key, [])
        
        return (self.max_calls - len(timestamps))

