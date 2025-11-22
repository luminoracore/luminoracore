"""Distributed tracing for LuminoraCore SDK."""

import asyncio
import uuid
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import json
from contextlib import asynccontextmanager

from ..utils.helpers import generate_session_id


class Span:
    """Represents a single span in a trace."""
    
    def __init__(
        self,
        trace_id: str,
        span_id: str,
        operation_name: str,
        start_time: Optional[datetime] = None,
        tags: Optional[Dict[str, Any]] = None,
        logs: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Initialize a span.
        
        Args:
            trace_id: Trace ID
            span_id: Span ID
            operation_name: Operation name
            start_time: Start time
            tags: Optional tags
            logs: Optional logs
        """
        self.trace_id = trace_id
        self.span_id = span_id
        self.operation_name = operation_name
        self.start_time = start_time or datetime.utcnow()
        self.end_time: Optional[datetime] = None
        self.duration: Optional[float] = None
        self.tags = tags or {}
        self.logs = logs or []
        self.child_spans: List[Span] = []
        self.parent_span_id: Optional[str] = None
    
    def finish(self, end_time: Optional[datetime] = None) -> None:
        """
        Finish the span.
        
        Args:
            end_time: End time (defaults to now)
        """
        self.end_time = end_time or datetime.utcnow()
        self.duration = (self.end_time - self.start_time).total_seconds()
    
    def add_tag(self, key: str, value: Any) -> None:
        """Add a tag to the span."""
        self.tags[key] = value
    
    def add_log(self, message: str, fields: Optional[Dict[str, Any]] = None) -> None:
        """Add a log entry to the span."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "fields": fields or {}
        }
        self.logs.append(log_entry)
    
    def add_child_span(self, child_span: "Span") -> None:
        """Add a child span."""
        child_span.parent_span_id = self.span_id
        self.child_spans.append(child_span)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert span to dictionary."""
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "operation_name": self.operation_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "tags": self.tags,
            "logs": self.logs,
            "child_spans": [child.to_dict() for child in self.child_spans]
        }


class Trace:
    """Represents a complete trace."""
    
    def __init__(self, trace_id: str, service_name: str = "luminoracore"):
        """
        Initialize a trace.
        
        Args:
            trace_id: Trace ID
            service_name: Service name
        """
        self.trace_id = trace_id
        self.service_name = service_name
        self.spans: List[Span] = []
        self.root_span: Optional[Span] = None
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.duration: Optional[float] = None
    
    def add_span(self, span: Span) -> None:
        """Add a span to the trace."""
        self.spans.append(span)
        
        if not self.root_span:
            self.root_span = span
            self.start_time = span.start_time
        
        if span.end_time:
            self.end_time = span.end_time
            self.duration = (self.end_time - self.start_time).total_seconds()
    
    def finish(self) -> None:
        """Finish the trace."""
        if self.spans:
            self.end_time = max(span.end_time or span.start_time for span in self.spans)
            self.duration = (self.end_time - self.start_time).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert trace to dictionary."""
        return {
            "trace_id": self.trace_id,
            "service_name": self.service_name,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "span_count": len(self.spans),
            "spans": [span.to_dict() for span in self.spans]
        }


class DistributedTracer:
    """Distributed tracer for LuminoraCore SDK."""
    
    def __init__(self, service_name: str = "luminoracore"):
        """
        Initialize the distributed tracer.
        
        Args:
            service_name: Service name
        """
        self.service_name = service_name
        self._traces: Dict[str, Trace] = {}
        self._active_spans: Dict[str, Span] = {}
        self._lock = asyncio.Lock()
    
    def start_trace(self, operation_name: str, trace_id: Optional[str] = None) -> str:
        """
        Start a new trace.
        
        Args:
            operation_name: Operation name
            trace_id: Optional trace ID
            
        Returns:
            Trace ID
        """
        if not trace_id:
            trace_id = generate_session_id()
        
        trace = Trace(trace_id, self.service_name)
        span = Span(trace_id, generate_session_id(), operation_name)
        
        trace.add_span(span)
        self._traces[trace_id] = trace
        self._active_spans[trace_id] = span
        
        return trace_id
    
    def start_span(
        self,
        operation_name: str,
        trace_id: str,
        parent_span_id: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Start a new span.
        
        Args:
            operation_name: Operation name
            trace_id: Trace ID
            parent_span_id: Optional parent span ID
            tags: Optional tags
            
        Returns:
            Span ID
        """
        span_id = generate_session_id()
        span = Span(trace_id, span_id, operation_name, tags=tags)
        
        if parent_span_id:
            span.parent_span_id = parent_span_id
        
        # Add to trace
        if trace_id in self._traces:
            self._traces[trace_id].add_span(span)
            
            # Add as child span if parent exists
            if parent_span_id:
                for existing_span in self._traces[trace_id].spans:
                    if existing_span.span_id == parent_span_id:
                        existing_span.add_child_span(span)
                        break
        
        self._active_spans[span_id] = span
        return span_id
    
    def finish_span(self, span_id: str) -> None:
        """
        Finish a span.
        
        Args:
            span_id: Span ID
        """
        if span_id in self._active_spans:
            self._active_spans[span_id].finish()
            del self._active_spans[span_id]
    
    def finish_trace(self, trace_id: str) -> None:
        """
        Finish a trace.
        
        Args:
            trace_id: Trace ID
        """
        if trace_id in self._traces:
            self._traces[trace_id].finish()
    
    def add_span_tag(self, span_id: str, key: str, value: Any) -> None:
        """
        Add a tag to a span.
        
        Args:
            span_id: Span ID
            key: Tag key
            value: Tag value
        """
        if span_id in self._active_spans:
            self._active_spans[span_id].add_tag(key, value)
    
    def add_span_log(self, span_id: str, message: str, fields: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a log entry to a span.
        
        Args:
            span_id: Span ID
            message: Log message
            fields: Optional log fields
        """
        if span_id in self._active_spans:
            self._active_spans[span_id].add_log(message, fields)
    
    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """
        Get a trace by ID.
        
        Args:
            trace_id: Trace ID
            
        Returns:
            Trace or None if not found
        """
        return self._traces.get(trace_id)
    
    def get_span(self, span_id: str) -> Optional[Span]:
        """
        Get a span by ID.
        
        Args:
            span_id: Span ID
            
        Returns:
            Span or None if not found
        """
        return self._active_spans.get(span_id)
    
    def list_traces(self) -> List[str]:
        """
        List all trace IDs.
        
        Returns:
            List of trace IDs
        """
        return list(self._traces.keys())
    
    def export_trace(self, trace_id: str, format: str = "json") -> Optional[str]:
        """
        Export a trace in specified format.
        
        Args:
            trace_id: Trace ID
            format: Export format (json, jaeger)
            
        Returns:
            Exported trace string or None if trace not found
        """
        trace = self.get_trace(trace_id)
        if not trace:
            return None
        
        if format == "json":
            return json.dumps(trace.to_dict(), indent=2)
        elif format == "jaeger":
            return self._export_jaeger(trace)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_jaeger(self, trace: Trace) -> str:
        """Export trace in Jaeger format."""
        # This is a simplified Jaeger export
        # In a real implementation, you'd use the Jaeger Python client
        jaeger_data = {
            "traceID": trace.trace_id,
            "spans": []
        }
        
        for span in trace.spans:
            jaeger_span = {
                "traceID": span.trace_id,
                "spanID": span.span_id,
                "operationName": span.operation_name,
                "startTime": int(span.start_time.timestamp() * 1000000),  # microseconds
                "duration": int((span.duration or 0) * 1000000),  # microseconds
                "tags": [
                    {"key": k, "value": str(v), "type": "string"}
                    for k, v in span.tags.items()
                ],
                "logs": [
                    {
                        "timestamp": int(datetime.fromisoformat(log["timestamp"]).timestamp() * 1000000),
                        "fields": [
                            {"key": k, "value": str(v), "type": "string"}
                            for k, v in log["fields"].items()
                        ]
                    }
                    for log in span.logs
                ]
            }
            
            if span.parent_span_id:
                jaeger_span["references"] = [
                    {
                        "refType": "CHILD_OF",
                        "traceID": span.trace_id,
                        "spanID": span.parent_span_id
                    }
                ]
            
            jaeger_data["spans"].append(jaeger_span)
        
        return json.dumps(jaeger_data, indent=2)
    
    def clear_traces(self) -> None:
        """Clear all traces."""
        self._traces.clear()
        self._active_spans.clear()
    
    def get_trace_summary(self) -> Dict[str, Any]:
        """
        Get summary of all traces.
        
        Returns:
            Trace summary
        """
        return {
            "total_traces": len(self._traces),
            "active_spans": len(self._active_spans),
            "trace_ids": list(self._traces.keys()),
            "active_span_ids": list(self._active_spans.keys()),
        }


@asynccontextmanager
async def trace_operation(
    tracer: DistributedTracer,
    operation_name: str,
    trace_id: Optional[str] = None,
    tags: Optional[Dict[str, Any]] = None
):
    """
    Context manager for tracing an operation.
    
    Args:
        tracer: Tracer instance
        operation_name: Operation name
        trace_id: Optional trace ID
        tags: Optional tags
        
    Yields:
        Span ID
    """
    span_id = tracer.start_span(operation_name, trace_id or generate_session_id(), tags=tags)
    
    try:
        yield span_id
    finally:
        tracer.finish_span(span_id)


def trace_function(
    tracer: DistributedTracer,
    operation_name: str,
    trace_id: Optional[str] = None,
    tags: Optional[Dict[str, Any]] = None
):
    """
    Decorator for tracing function execution.
    
    Args:
        tracer: Tracer instance
        operation_name: Operation name
        trace_id: Optional trace ID
        tags: Optional tags
        
    Returns:
        Decorated function
    """
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            span_id = tracer.start_span(operation_name, trace_id or generate_session_id(), tags=tags)
            
            try:
                result = await func(*args, **kwargs)
                tracer.add_span_tag(span_id, "success", True)
                return result
            except Exception as e:
                tracer.add_span_tag(span_id, "success", False)
                tracer.add_span_tag(span_id, "error", str(e))
                raise
            finally:
                tracer.finish_span(span_id)
        
        def sync_wrapper(*args, **kwargs):
            span_id = tracer.start_span(operation_name, trace_id or generate_session_id(), tags=tags)
            
            try:
                result = func(*args, **kwargs)
                tracer.add_span_tag(span_id, "success", True)
                return result
            except Exception as e:
                tracer.add_span_tag(span_id, "success", False)
                tracer.add_span_tag(span_id, "error", str(e))
                raise
            finally:
                tracer.finish_span(span_id)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator
