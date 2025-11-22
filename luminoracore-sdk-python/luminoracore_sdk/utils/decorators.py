"""Decorators for LuminoraCore SDK."""

import asyncio
import functools
import time
from typing import Callable, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)


def timeout(seconds: float):
    """
    Decorator to add timeout to functions.
    
    Args:
        seconds: Timeout in seconds
        
    Returns:
        Decorated function with timeout
    """
    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs) -> Any:
                # For sync functions, we can't easily implement timeout
                # This is a placeholder - in practice, you'd need threading
                return func(*args, **kwargs)
            return sync_wrapper
    return decorator


def async_timeout(seconds: float):
    """
    Decorator to add timeout to async functions.
    
    Args:
        seconds: Timeout in seconds
        
    Returns:
        Decorated async function with timeout
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
        return wrapper
    return decorator


def validate(*validators):
    """
    Decorator to add validation to functions.
    
    Args:
        *validators: Validation functions to apply
        
    Returns:
        Decorated function with validation
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for validator in validators:
                validator(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def retry(max_attempts: int = 3, delay: float = 1.0, backoff_factor: float = 2.0):
    """
    Decorator to add retry logic to functions.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries
        backoff_factor: Factor for exponential backoff
        
    Returns:
        Decorated function with retry logic
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        raise e
                    
                    logger.warning(
                        f"Attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {current_delay} seconds..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff_factor
            
            raise last_exception
        return wrapper
    return decorator


def async_retry(max_attempts: int = 3, delay: float = 1.0, backoff_factor: float = 2.0):
    """
    Decorator to add retry logic to async functions.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries
        backoff_factor: Factor for exponential backoff
        
    Returns:
        Decorated async function with retry logic
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        raise e
                    
                    logger.warning(
                        f"Attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {current_delay} seconds..."
                    )
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff_factor
            
            raise last_exception
        return wrapper
    return decorator


def measure_time(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    
    Returns:
        Decorated function that logs execution time
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.3f} seconds")
    
    return wrapper


def async_measure_time(func: Callable) -> Callable:
    """
    Decorator to measure async function execution time.
    
    Returns:
        Decorated async function that logs execution time
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.3f} seconds")
    
    return wrapper


def cache_result(ttl: Optional[float] = None):
    """
    Decorator to cache function results.
    
    Args:
        ttl: Time to live in seconds
        
    Returns:
        Decorated function with caching
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Create cache key from args and kwargs
            key = str(args) + str(sorted(kwargs.items()))
            
            if key in cache:
                if ttl is None:
                    return cache[key]
                
                # Check if cache entry is still valid
                entry_time, result = cache[key]
                if time.time() - entry_time < ttl:
                    return result
                else:
                    del cache[key]
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache[key] = (time.time(), result)
            
            return result
        
        return wrapper
    return decorator
