# LLM Server Monitoring System

A comprehensive monitoring solution for LLM (Large Language Model) server infrastructure, providing real-time insights into system health, GPU utilization, model performance, and service availability.

## Overview

This monitoring system is designed specifically for AI/ML teams running LLM servers in production. It provides:

- **System Monitoring**: CPU, memory, disk, and network metrics
- **GPU Monitoring**: Real-time GPU utilization, memory, and temperature tracking
- **Container Monitoring**: Docker container health and resource usage
- **LLM Service Monitoring**: LiteLLM and vLLM specific metrics
- **Log Aggregation**: Centralized logging with Loki and Promtail
- **Analytics Integration**: LangFuse analytics and performance tracking

## Architecture

The system follows a modular, containerized architecture:

- **Prometheus**: Time-series database for metrics storage
- **Grafana**: Visualization and dashboarding platform
- **Loki**: Log aggregation system
- **Custom Exporters**: Specialized metric collectors for LLM services
- **Docker Compose**: Orchestration for easy deployment

## Quick Start

### Prerequisites

- Ubuntu 24.04 LTS
- Docker Engine (latest)
- Docker Compose v2
- NVIDIA GPU drivers (for GPU monitoring)
- NVIDIA Container Toolkit (for GPU monitoring)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd llm-monitor
   ```

2. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` to configure your environment:
   ```bash
   nano .env
   ```

4. Start the monitoring stack:
   ```bash
   docker-compose up -d
   ```

5. Access the services:
   - Grafana: http://localhost:23000 (admin/admin)
   - Prometheus: http://localhost:23001
   - Loki: http://localhost:23002

### Development Setup

For development with hot-reload and debug logging:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Mock Data Testing

To test dashboards with simulated data:

```bash
docker-compose -f docker-compose.yml -f docker-compose.mock.yml up
```

## Configuration

### Environment Variables

Key configuration options in `.env`:

- `PROMETHEUS_PORT`: Prometheus server port (default: 23001)
- `GRAFANA_PORT`: Grafana dashboard port (default: 23000)
- `LOKI_PORT`: Loki log server port (default: 23002)
- `PROMETHEUS_RETENTION`: Data retention period (default: 30d)
- `GPU_METRICS_ENABLED`: Enable GPU monitoring (default: true)

See `.env.example` for complete configuration options.

### Adding Custom Exporters

1. Create a new directory under `exporters/`
2. Follow the base exporter framework pattern
3. Add configuration to `docker-compose.yml`
4. Update Prometheus scrape configuration

## Dashboards

Pre-configured dashboards include:

- **System Health**: Server resource utilization
- **GPU Usage**: GPU metrics and performance
- **Container Status**: Docker container monitoring
- **LLM Services**: LiteLLM and vLLM metrics
- **Log Explorer**: Centralized log viewing

## Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 23000-23002 are available
2. **GPU not detected**: Verify NVIDIA Container Toolkit installation
3. **High memory usage**: Adjust retention periods in configuration
4. **Dashboard not loading**: Check Grafana logs: `docker-compose logs grafana`

### Debug Mode

Enable debug logging:

```bash
export DEV_VERBOSE_LOGGING=true
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Logs

View service logs:

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f prometheus
```

## Development

### Project Structure

```
llm-monitor/
├── config/         # Service configurations
├── dashboards/     # Grafana dashboard definitions
├── exporters/      # Custom Prometheus exporters
├── scripts/        # Utility scripts
├── tests/          # Test suites
└── docker/         # Docker compose files
```

### Running Tests

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# End-to-end tests
pytest tests/e2e/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Security

- Internal network only - no external access by default
- Configurable authentication for production deployments
- Sensitive data excluded from metrics
- Regular security updates for base images

## Support

For issues and feature requests, please use the GitHub issue tracker.

## License

[License information to be added]