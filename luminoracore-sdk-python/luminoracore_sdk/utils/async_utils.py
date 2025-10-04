"""Async utilities for LuminoraCore SDK."""

import asyncio
import functools
from typing import Any, Callable, Optional, Union, List, Dict
import logging

logger = logging.getLogger(__name__)


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


async def async_timeout(func: Callable, timeout: float, *args, **kwargs) -> Any:
    """
    Execute an async function with timeout.
    
    Args:
        func: Async function to execute
        timeout: Timeout in seconds
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Result of the function call
        
    Raises:
        asyncio.TimeoutError: If function times out
    """
    return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)


async def async_batch(
    func: Callable,
    items: List[Any],
    batch_size: int = 10,
    *args,
    **kwargs
) -> List[Any]:
    """
    Execute an async function on items in batches.
    
    Args:
        func: Async function to execute
        items: List of items to process
        batch_size: Number of items per batch
        *args: Additional arguments to pass to the function
        **kwargs: Additional keyword arguments to pass to the function
        
    Returns:
        List of results
    """
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        tasks = [func(item, *args, **kwargs) for item in batch]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        results.extend(batch_results)
    
    return results


async def async_parallel(
    func: Callable,
    items: List[Any],
    max_concurrent: int = 10,
    *args,
    **kwargs
) -> List[Any]:
    """
    Execute an async function on items in parallel with concurrency limit.
    
    Args:
        func: Async function to execute
        items: List of items to process
        max_concurrent: Maximum number of concurrent executions
        *args: Additional arguments to pass to the function
        **kwargs: Additional keyword arguments to pass to the function
        
    Returns:
        List of results
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def limited_func(item: Any) -> Any:
        async with semaphore:
            return await func(item, *args, **kwargs)
    
    tasks = [limited_func(item) for item in items]
    return await asyncio.gather(*tasks, return_exceptions=True)


async def async_retry_with_backoff(
    func: Callable,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: tuple = (Exception,),
    *args,
    **kwargs
) -> Any:
    """
    Retry an async function with exponential backoff and jitter.
    
    Args:
        func: Async function to retry
        max_attempts: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        backoff_factor: Factor for exponential backoff
        jitter: Whether to add random jitter
        exceptions: Tuple of exceptions to retry on
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Result of the function call
        
    Raises:
        Last exception if all attempts fail
    """
    import random
    
    last_exception = None
    current_delay = base_delay
    
    for attempt in range(max_attempts):
        try:
            return await func(*args, **kwargs)
        except exceptions as e:
            last_exception = e
            if attempt == max_attempts - 1:
                raise e
            
            # Calculate delay with jitter
            delay = min(current_delay, max_delay)
            if jitter:
                delay *= (0.5 + random.random() * 0.5)  # Add 0-50% jitter
            
            logger.warning(
                f"Attempt {attempt + 1} failed: {e}. "
                f"Retrying in {delay:.2f} seconds..."
            )
            
            await asyncio.sleep(delay)
            current_delay *= backoff_factor
    
    raise last_exception


async def async_circuit_breaker(
    func: Callable,
    failure_threshold: int = 5,
    timeout: float = 60.0,
    exceptions: tuple = (Exception,),
    *args,
    **kwargs
) -> Any:
    """
    Execute an async function with circuit breaker pattern.
    
    Args:
        func: Async function to execute
        failure_threshold: Number of failures before circuit opens
        timeout: Timeout in seconds before circuit closes
        exceptions: Tuple of exceptions that count as failures
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Result of the function call
        
    Raises:
        Exception: If circuit is open or function fails
    """
    # This is a simplified implementation
    # In production, you'd want a proper circuit breaker with state management
    
    try:
        return await func(*args, **kwargs)
    except exceptions as e:
        logger.error(f"Circuit breaker triggered by exception: {e}")
        raise e


async def async_rate_limit(
    func: Callable,
    rate_limit: float,
    *args,
    **kwargs
) -> Any:
    """
    Execute an async function with rate limiting.
    
    Args:
        func: Async function to execute
        rate_limit: Rate limit in calls per second
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Result of the function call
    """
    # Simple rate limiting with asyncio.sleep
    delay = 1.0 / rate_limit
    await asyncio.sleep(delay)
    return await func(*args, **kwargs)


async def async_retry_forever(
    func: Callable,
    delay: float = 1.0,
    backoff_factor: float = 1.0,
    max_delay: float = 300.0,
    exceptions: tuple = (Exception,),
    *args,
    **kwargs
) -> Any:
    """
    Retry an async function forever until it succeeds.
    
    Args:
        func: Async function to retry
        delay: Initial delay in seconds
        backoff_factor: Factor for exponential backoff
        max_delay: Maximum delay in seconds
        exceptions: Tuple of exceptions to retry on
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Result of the function call
    """
    current_delay = delay
    
    while True:
        try:
            return await func(*args, **kwargs)
        except exceptions as e:
            logger.warning(
                f"Function failed: {e}. "
                f"Retrying in {current_delay} seconds..."
            )
            
            await asyncio.sleep(current_delay)
            current_delay = min(current_delay * backoff_factor, max_delay)


async def async_retry_with_condition(
    func: Callable,
    condition: Callable[[Exception], bool],
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    *args,
    **kwargs
) -> Any:
    """
    Retry an async function based on a condition.
    
    Args:
        func: Async function to retry
        condition: Function that determines if an exception should be retried
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries
        backoff_factor: Factor for exponential backoff
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
        except Exception as e:
            last_exception = e
            if attempt == max_attempts - 1 or not condition(e):
                raise e
            
            logger.warning(
                f"Attempt {attempt + 1} failed: {e}. "
                f"Retrying in {current_delay} seconds..."
            )
            
            await asyncio.sleep(current_delay)
            current_delay *= backoff_factor
    
    raise last_exception
