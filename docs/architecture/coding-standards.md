# Coding Standards

Define MINIMAL but CRITICAL standards for AI agents developing this system.

## Critical Monitoring System Rules

- **Metric Naming:** Follow Prometheus naming conventions: `<namespace>_<subsystem>_<name>_<unit>`
- **Label Cardinality:** Never use unbounded labels (user IDs, request IDs, timestamps)
- **Error Handling:** All exporters must handle collection failures gracefully without crashing
- **Configuration:** All settings must be configurable via environment variables with Dynaconf
- **Docker Health:** Every container must expose /health and /ready endpoints
- **Scrape Interval:** Respect 30-second scrape interval - no more frequent updates
- **Data Retention:** Design metrics with 30-day retention in mind
- **Network Isolation:** Assume internal network only - no external access
- **GPU Safety:** Never directly control GPUs - only observe metrics
- **Mock Data:** Mock exporters must clearly identify as mock in metrics

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Exporters | kebab-case | `gpu-exporter` |
| Python modules | snake_case | `nvidia_collector.py` |
| Docker services | kebab-case | `node-exporter` |
| Metrics | snake_case | `gpu_temperature_celsius` |
| Environment vars | UPPER_SNAKE | `PROMETHEUS_PORT` |
| Grafana dashboards | kebab-case | `gpu-usage.json` |

## Code Patterns

```python