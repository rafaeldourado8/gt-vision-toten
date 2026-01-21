"""Prometheus middleware for FastAPI."""
from time import time
from typing import Callable

from fastapi import Request
from prometheus_client import Counter, Gauge, Histogram

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"],
)

http_connections_active = Gauge("http_connections_active", "Active connections")


async def prometheus_middleware(request: Request, call_next: Callable):
    """Prometheus metrics middleware."""
    http_connections_active.inc()
    start = time()

    response = await call_next(request)

    duration = time() - start
    http_requests_total.labels(
        method=request.method, endpoint=request.url.path, status=response.status_code
    ).inc()
    http_request_duration_seconds.labels(
        method=request.method, endpoint=request.url.path
    ).observe(duration)
    http_connections_active.dec()

    return response
