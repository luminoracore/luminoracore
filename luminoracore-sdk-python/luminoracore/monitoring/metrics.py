"""Metrics collection for LuminoraCore SDK."""

import asyncio
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
import logging
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collects and manages metrics for LuminoraCore SDK."""
    
    def __init__(self, max_history: int = 1000):
        """
        Initialize the metrics collector.
        
        Args:
            max_history: Maximum number of metrics to keep in history
        """
        self.max_history = max_history
        self._metrics: Dict[str, Any] = defaultdict(lambda: deque(maxlen=max_history))
        self._counters: Dict[str, int] = defaultdict(int)
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, List[float]] = defaultdict(list)
        self._lock = asyncio.Lock()
    
    async def increment_counter(self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None) -> None:
        """
        Increment a counter metric.
        
        Args:
            name: Metric name
            value: Value to increment by
            tags: Optional tags for the metric
        """
        async with self._lock:
            self._counters[name] += value
            
            # Store in history
            metric_data = {
                "timestamp": datetime.utcnow(),
                "type": "counter",
                "name": name,
                "value": value,
                "total": self._counters[name],
                "tags": tags or {}
            }
            self._metrics[name].append(metric_data)
    
    async def set_gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """
        Set a gauge metric value.
        
        Args:
            name: Metric name
            value: Gauge value
            tags: Optional tags for the metric
        """
        async with self._lock:
            self._gauges[name] = value
            
            # Store in history
            metric_data = {
                "timestamp": datetime.utcnow(),
                "type": "gauge",
                "name": name,
                "value": value,
                "tags": tags or {}
            }
            self._metrics[name].append(metric_data)
    
    async def record_histogram(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """
        Record a histogram value.
        
        Args:
            name: Metric name
            value: Value to record
            tags: Optional tags for the metric
        """
        async with self._lock:
            self._histograms[name].append(value)
            
            # Store in history
            metric_data = {
                "timestamp": datetime.utcnow(),
                "type": "histogram",
                "name": name,
                "value": value,
                "tags": tags or {}
            }
            self._metrics[name].append(metric_data)
    
    async def record_timing(self, name: str, duration: float, tags: Optional[Dict[str, str]] = None) -> None:
        """
        Record a timing metric.
        
        Args:
            name: Metric name
            duration: Duration in seconds
            tags: Optional tags for the metric
        """
        await self.record_histogram(f"{name}.duration", duration, tags)
        await self.increment_counter(f"{name}.count", tags=tags)
    
    async def get_counter(self, name: str) -> int:
        """
        Get counter value.
        
        Args:
            name: Counter name
            
        Returns:
            Counter value
        """
        async with self._lock:
            return self._counters.get(name, 0)
    
    async def get_gauge(self, name: str) -> Optional[float]:
        """
        Get gauge value.
        
        Args:
            name: Gauge name
            
        Returns:
            Gauge value or None if not set
        """
        async with self._lock:
            return self._gauges.get(name)
    
    async def get_histogram_stats(self, name: str) -> Optional[Dict[str, float]]:
        """
        Get histogram statistics.
        
        Args:
            name: Histogram name
            
        Returns:
            Histogram statistics or None if no data
        """
        async with self._lock:
            values = self._histograms.get(name, [])
            if not values:
                return None
            
            return {
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "mean": sum(values) / len(values),
                "median": sorted(values)[len(values) // 2],
                "p95": sorted(values)[int(len(values) * 0.95)],
                "p99": sorted(values)[int(len(values) * 0.99)],
            }
    
    async def get_metric_history(self, name: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get metric history.
        
        Args:
            name: Metric name
            limit: Maximum number of entries to return
            
        Returns:
            List of metric entries
        """
        async with self._lock:
            history = list(self._metrics.get(name, []))
            if limit:
                history = history[-limit:]
            return history
    
    async def get_all_metrics(self) -> Dict[str, Any]:
        """
        Get all metrics.
        
        Returns:
            Dictionary containing all metrics
        """
        async with self._lock:
            return {
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": {
                    name: await self.get_histogram_stats(name)
                    for name in self._histograms.keys()
                }
            }
    
    async def clear_metrics(self) -> None:
        """Clear all metrics."""
        async with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()
            self._metrics.clear()
    
    async def export_metrics(self, format: str = "json") -> str:
        """
        Export metrics in specified format.
        
        Args:
            format: Export format (json, prometheus)
            
        Returns:
            Exported metrics string
        """
        if format == "json":
            import json
            return json.dumps(await self.get_all_metrics(), indent=2, default=str)
        elif format == "prometheus":
            return await self._export_prometheus()
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    async def _export_prometheus(self) -> str:
        """Export metrics in Prometheus format."""
        lines = []
        
        # Export counters
        for name, value in self._counters.items():
            lines.append(f"# TYPE {name} counter")
            lines.append(f"{name} {value}")
        
        # Export gauges
        for name, value in self._gauges.items():
            lines.append(f"# TYPE {name} gauge")
            lines.append(f"{name} {value}")
        
        # Export histograms
        for name, values in self._histograms.items():
            if values:
                stats = await self.get_histogram_stats(name)
                lines.append(f"# TYPE {name} histogram")
                lines.append(f"{name}_count {stats['count']}")
                lines.append(f"{name}_sum {sum(values)}")
                lines.append(f"{name}_min {stats['min']}")
                lines.append(f"{name}_max {stats['max']}")
                lines.append(f"{name}_mean {stats['mean']}")
                lines.append(f"{name}_median {stats['median']}")
                lines.append(f"{name}_p95 {stats['p95']}")
                lines.append(f"{name}_p99 {stats['p99']}")
        
        return "\n".join(lines)
    
    async def get_metric_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all metrics.
        
        Returns:
            Metrics summary
        """
        async with self._lock:
            return {
                "total_counters": len(self._counters),
                "total_gauges": len(self._gauges),
                "total_histograms": len(self._histograms),
                "counter_names": list(self._counters.keys()),
                "gauge_names": list(self._gauges.keys()),
                "histogram_names": list(self._histograms.keys()),
                "total_metric_entries": sum(len(history) for history in self._metrics.values()),
            }


class TimingContext:
    """Context manager for timing operations."""
    
    def __init__(self, metrics_collector: MetricsCollector, name: str, tags: Optional[Dict[str, str]] = None):
        """
        Initialize timing context.
        
        Args:
            metrics_collector: Metrics collector instance
            name: Metric name
            tags: Optional tags
        """
        self.metrics_collector = metrics_collector
        self.name = name
        self.tags = tags
        self.start_time = None
    
    async def __aenter__(self):
        """Enter timing context."""
        self.start_time = time.time()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit timing context."""
        if self.start_time:
            duration = time.time() - self.start_time
            await self.metrics_collector.record_timing(self.name, duration, self.tags)


def timing(metrics_collector: MetricsCollector, name: str, tags: Optional[Dict[str, str]] = None):
    """
    Decorator for timing function execution.
    
    Args:
        metrics_collector: Metrics collector instance
        name: Metric name
        tags: Optional tags
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        async def async_wrapper(*args, **kwargs):
            async with TimingContext(metrics_collector, name, tags):
                return await func(*args, **kwargs)
        
        def sync_wrapper(*args, **kwargs):
            with TimingContext(metrics_collector, name, tags):
                return func(*args, **kwargs)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator
