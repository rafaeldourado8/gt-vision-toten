"""Business metrics helper."""
from prometheus_client import Counter, Gauge


class Metrics:
    """Metrics helper for Prometheus."""

    def __init__(self, prefix: str = "app"):
        self.prefix = prefix
        self._counters: dict[str, Counter] = {}
        self._gauges: dict[str, Gauge] = {}

    def counter(self, name: str, description: str, labels: list[str] | None = None) -> Counter:
        key = f"{self.prefix}_{name}"
        if key not in self._counters:
            self._counters[key] = Counter(key, description, labels or [])
        return self._counters[key]

    def gauge(self, name: str, description: str, labels: list[str] | None = None) -> Gauge:
        key = f"{self.prefix}_{name}"
        if key not in self._gauges:
            self._gauges[key] = Gauge(key, description, labels or [])
        return self._gauges[key]

    def increment(self, name: str, labels: dict | None = None) -> None:
        counter = self._counters.get(f"{self.prefix}_{name}")
        if counter:
            if labels:
                counter.labels(**labels).inc()
            else:
                counter.inc()

    def set_gauge(self, name: str, value: float, labels: dict | None = None) -> None:
        gauge = self._gauges.get(f"{self.prefix}_{name}")
        if gauge:
            if labels:
                gauge.labels(**labels).set(value)
            else:
                gauge.set(value)
