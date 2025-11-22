"""Retry utilities for LuminoraCore SDK."""

import asyncio
import functools
import time
from typing import Callable, Any, Optional, Union
import logging

from tenacity import (
    retry as tenacity_retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    after_log,
)

logger = logging.getLogger(__name__)


def with_retry(
    max_attempts: int = 3,
    backoff_factor: float = 1.0,
    exceptions: tuple = (Exception,),
    delay: float = 1.0,
    max_delay: float = 60.0,
):
    """
    Decorator to add retry logic to functions.
    
    Args:
        max_attempts: Maximum number of retry attempts
        backoff_factor: Factor for exponential backoff
        exceptions: Tuple of exceptions to retry on
        delay: Initial delay between retries
        max_delay: Maximum delay between retries
        
    Returns:
        Decorated function with retry logic
    """
    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @tenacity_retry(
                stop=stop_after_attempt(max_attempts),
                wait=wait_exponential(
                    multiplier=delay,
                    max=max_delay,
                    exp_base=backoff_factor
                ),
                retry=retry_if_exception_type(exceptions),
                before_sleep=before_sleep_log(logger, logging.WARNING),
                after=after_log(logger, logging.INFO),
            )
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                return await func(*args, **kwargs)
            return async_wrapper
        else:
            @tenacity_retry(
                stop=stop_after_attempt(max_attempts),
                wait=wait_exponential(
                    multiplier=delay,
                    max=max_delay,
                    exp_base=backoff_factor
                ),
                retry=retry_if_exception_type(exceptions),
                before_sleep=before_sleep_log(logger, logging.WARNING),
                after=after_log(logger, logging.INFO),
            )
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs) -> Any:
                return func(*args, **kwargs)
            return sync_wrapper
    
    return decorator


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
):
    """
    Simple retry decorator for synchronous functions.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries
        backoff_factor: Factor for exponential backoff
        exceptions: Tuple of exceptions to retry on
        
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
                except exceptions as e:
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


async def async_retry(
    func: Callable,
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
    *args,
    **kwargs
) -> Any:
    """
    Retry an async function with exponential backoff.
    
    Args:
        func: Async function to retry
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries
        backoff_factor: Factor for exponential backoff
        exceptions: Tuple of exceptions to retry on
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Result of the function call
        
    Raises:
        Last exception if all attempts fail
    """
    last_exception = None
    current_delay = delay
    
    for attempt in range(max_attempts):
        try:
            return await func(*args, **kwargs)
        except exceptions as e:
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
