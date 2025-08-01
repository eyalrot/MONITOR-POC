# Frontend Architecture

Define frontend-specific architecture details for the monitoring system's Grafana-based user interface.

## Component Architecture

Grafana provides the complete frontend for the monitoring system, with customizations via dashboards, panels, and plugins.

### Dashboard Organization

```
/dashboards/
├── system/
│   ├── server-health.json          # CPU, Memory, Disk, Network
│   ├── gpu-usage.json              # 8x H200 GPU monitoring
│   └── docker-containers.json      # Container status and resources
├── llm/
│   ├── litellm-status.json         # LiteLLM proxy and routing
│   ├── vllm-docker-status.json     # vLLM containers and versions
│   └── model-catalog.json          # Available models and endpoints
├── analytics/
│   ├── langfuse-analytics.json     # Usage analytics and costs
│   └── performance-trends.json     # Historical performance data
├── logs/
│   └── log-explorer.json           # Loki log search interface
└── announcements/
    └── system-status.json          # Announcements and maintenance
