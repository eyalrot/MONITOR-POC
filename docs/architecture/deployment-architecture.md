# Deployment Architecture

Define deployment strategy for the monitoring system on Ubuntu 24.04 server.

## Deployment Strategy

**Frontend Deployment:**
- **Platform:** Docker container on Ubuntu 24.04
- **Build Command:** `docker build -t grafana-custom dashboards/`
- **Output Directory:** `/var/lib/grafana`
- **CDN/Edge:** Not applicable (internal network)

**Backend Deployment:**
- **Platform:** Docker containers on Ubuntu 24.04
- **Build Command:** `make build-exporters`
- **Deployment Method:** Docker Compose with systemd service

## CI/CD Pipeline

```yaml