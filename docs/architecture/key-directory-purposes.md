# Key Directory Purposes

## /config
Central location for all service configurations. Each service has its own subdirectory with relevant config files. This enables easy configuration management and version control.

## /dashboards
Grafana dashboard JSON files organized by category. These are automatically provisioned when Grafana starts via the provisioning configuration.

## /exporters
Custom Python exporters following a consistent structure. Each exporter:
- Inherits from the base exporter framework
- Has its own Dockerfile for containerization
- Includes service-specific configuration
- Follows the same directory structure pattern

## /scripts
Automation scripts for common tasks:
- **setup/**: Initial environment setup
- **development/**: Developer workflow automation
- **maintenance/**: Operational tasks

## /tests
Comprehensive test coverage:
- **unit/**: Test individual components
- **integration/**: Test component interactions
- **e2e/**: Full system tests using Playwright MCP

## /docker
Docker Compose configurations for different environments:
- Base configuration for core services
- Environment-specific overrides
- Mock data configuration for development
```
