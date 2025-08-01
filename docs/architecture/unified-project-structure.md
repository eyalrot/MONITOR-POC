# Unified Project Structure

Create a monorepo structure that accommodates both frontend (dashboards) and backend (exporters) components.

```plaintext
llm-monitor/
├── .github/                        # CI/CD workflows
│   └── workflows/
│       ├── ci.yaml                 # Continuous integration
│       ├── build-images.yaml       # Docker image builds
│       └── release.yaml            # Release automation
├── config/                         # Configuration files
│   ├── prometheus/
│   │   ├── prometheus.yml          # Prometheus config
│   │   └── rules/                  # Alert rules
│   │       ├── gpu_alerts.yml
│   │       ├── system_alerts.yml
│   │       └── llm_alerts.yml
│   ├── grafana/
│   │   ├── grafana.ini             # Grafana config
│   │   └── provisioning/
│   │       ├── dashboards/
│   │       │   └── dashboard.yml   # Dashboard provisioning
│   │       └── datasources/
│   │           └── datasources.yml # Data source config
│   ├── loki/
│   │   └── loki-config.yml         # Loki configuration
│   └── promtail/
│       └── promtail-config.yml     # Log shipping config
├── dashboards/                     # Grafana dashboards
│   ├── system/
│   │   ├── server-health.json
│   │   ├── gpu-usage.json
│   │   └── docker-containers.json
│   ├── llm/
│   │   ├── litellm-status.json
│   │   ├── vllm-docker-status.json
│   │   └── model-catalog.json
│   ├── analytics/
│   │   ├── langfuse-analytics.json
│   │   └── performance-trends.json
│   ├── logs/
│   │   └── log-explorer.json
│   └── announcements/
│       └── system-status.json
├── exporters/                      # Custom exporters
│   ├── base/                       # Base exporter framework
│   │   ├── Dockerfile.base
│   │   ├── requirements.txt
│   │   ├── setup.py
│   │   └── src/
│   │       ├── __init__.py
│   │       ├── base_exporter.py
│   │       ├── metrics_registry.py
│   │       ├── config_loader.py
│   │       ├── auth_middleware.py
│   │       └── repository_pattern.py
│   ├── node/                       # System metrics
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── src/
│   │       ├── main.py
│   │       ├── collectors/
│   │       └── config/
│   │           └── settings.yaml
│   ├── gpu/                        # GPU metrics
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── src/
│   │       ├── main.py
│   │       ├── nvidia_collector.py
│   │       └── config/
│   │           └── settings.yaml
│   ├── container/                  # Container metrics
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── src/
│   │       ├── main.py
│   │       ├── docker_collector.py
│   │       └── config/
│   │           └── settings.yaml
│   ├── litellm/                    # LiteLLM metrics
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── src/
│   │       ├── main.py
│   │       ├── api_client.py
│   │       └── config/
│   │           └── settings.yaml
│   ├── vllm/                       # vLLM metrics
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── src/
│   │       ├── main.py
│   │       ├── container_discovery.py
│   │       └── config/
│   │           └── settings.yaml
│   ├── langfuse/                   # LangFuse metrics
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── src/
│   │       ├── main.py
│   │       ├── analytics_collector.py
│   │       └── config/
│   │           └── settings.yaml
│   └── mock/                       # Mock data generator
│       ├── Dockerfile
│       ├── requirements.txt
│       └── src/
│           ├── main.py
│           ├── scenario_manager.py
│           ├── patterns/
│           │   ├── __init__.py
│           │   ├── system_patterns.py
│           │   ├── gpu_patterns.py
│           │   └── llm_patterns.py
│           └── config/
│               ├── settings.yaml
│               └── scenarios.yaml
├── scripts/                        # Utility scripts
│   ├── setup/
│   │   ├── install-dependencies.sh
│   │   ├── setup-nvidia-toolkit.sh
│   │   └── create-volumes.sh
│   ├── development/
│   │   ├── start-dev.sh            # Start dev environment
│   │   ├── stop-dev.sh             # Stop all services
│   │   ├── reset-data.sh           # Clear all data
│   │   └── load-mock-data.sh       # Load test data
│   └── maintenance/
│       ├── backup-dashboards.sh
│       ├── export-metrics.sh
│       └── rotate-logs.sh
├── tests/                          # Test suites
│   ├── unit/                       # Unit tests
│   │   ├── exporters/
│   │   └── __init__.py
│   ├── integration/                # Integration tests
│   │   ├── test_prometheus_scrape.py
│   │   └── test_grafana_api.py
│   └── e2e/                        # End-to-end tests
│       ├── playwright/
│       │   ├── test_dashboards.py
│       │   └── playwright.config.ts
│       └── mcp/
│           └── test_config.yaml    # MCP test configuration
├── docs/                           # Documentation
│   ├── prd.md                      # Product requirements
│   ├── architecture.md             # This document
│   ├── deployment.md               # Deployment guide
│   ├── operation.md                # Operations manual
│   └── development.md              # Developer guide
├── docker/                         # Docker-specific files
│   ├── docker-compose.yml          # Main compose file
│   ├── docker-compose.dev.yml      # Dev overrides
│   ├── docker-compose.prod.yml     # Production config
│   └── docker-compose.mock.yml     # Mock data config
├── .env.example                    # Environment template
├── .gitignore
├── Makefile                        # Build automation
├── README.md                       # Project overview
└── CLAUDE.md                       # AI assistant context
