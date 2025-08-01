# AI Assistant Context - LLM Server Monitoring System

This document provides context for AI assistants (like Claude) working with this codebase.

## Project Overview

This is a comprehensive monitoring system specifically designed for LLM (Large Language Model) server infrastructure. It monitors system health, GPU utilization, container performance, and LLM-specific services.

## Key Architecture Decisions

1. **Monorepo Structure**: All components (exporters, dashboards, configurations) in a single repository
2. **Docker-First**: Everything runs in containers for consistency and isolation
3. **Internal Network Only**: No external access by default for security
4. **30-Day Retention**: Metrics retained for 30 days, configurable via environment
5. **Mock Data Support**: Built-in mock data generator for testing without real infrastructure

## Important Conventions

### Naming Standards
- Metrics: `llm_monitor_<subsystem>_<metric>_<unit>` (e.g., `llm_monitor_gpu_temperature_celsius`)
- Docker services: kebab-case (e.g., `gpu-exporter`)
- Python modules: snake_case (e.g., `nvidia_collector.py`)
- Environment variables: UPPER_SNAKE_CASE (e.g., `PROMETHEUS_PORT`)

### Port Assignments
- Grafana: 23000
- Prometheus: 23001
- Loki: 23002
- Exporters: 8080-8099 range

### Development Workflow
1. All exporters extend the base framework in `exporters/base/`
2. Configuration via Dynaconf with environment variable overrides
3. Every service must expose `/health` and `/ready` endpoints
4. Respect 30-second scrape intervals - no more frequent updates

## Common Tasks

### Adding a New Exporter
1. Create directory under `exporters/`
2. Copy structure from existing exporter
3. Extend `BaseExporter` class
4. Add to `docker-compose.yml`
5. Update Prometheus configuration

### Creating a Dashboard
1. Design in Grafana UI first
2. Export JSON to `dashboards/` appropriate subdirectory
3. Ensure all queries use proper metric names
4. Test with mock data configuration

### Testing Changes
```bash
# Development mode with hot reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Test with mock data
docker-compose -f docker-compose.yml -f docker-compose.mock.yml up
```

## Important Files

- `docs/architecture/`: Architecture documentation
- `docs/prd.md`: Product requirements
- `.env.example`: All configuration options
- `exporters/base/`: Base framework for all exporters
- `docker/docker-compose.yml`: Main orchestration file

## Common Issues and Solutions

1. **GPU Not Detected**: Ensure NVIDIA Container Toolkit is installed
2. **High Memory Usage**: Reduce `PROMETHEUS_RETENTION` in `.env`
3. **Port Conflicts**: Change ports in `.env` file
4. **Exporter Crashes**: Check logs with `docker-compose logs <service-name>`

## Testing Strategy

- Unit tests: pytest for Python components
- Integration tests: Test service interactions
- E2E tests: Playwright with MCP for dashboard testing
- Always test with mock data before real deployment

## Security Considerations

- No external network access by default
- Sensitive data must never be in metrics
- Use label cardinality limits to prevent metric explosion
- Regular updates of base images for security patches

## Performance Guidelines

- Respect 30-second scrape intervals
- Limit metric cardinality (no user IDs, request IDs, etc.)
- Use recording rules for expensive queries
- Design dashboards with 30-day retention in mind

## Getting Help

1. Check `docs/` directory for detailed documentation
2. Review existing exporter implementations
3. Test with mock data first
4. Use debug logging in development mode