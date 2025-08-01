# High Level Architecture

## Technical Summary

The LLM Server Monitoring System is a containerized monitoring solution deployed on Ubuntu 24.04, utilizing Prometheus for metrics collection and Grafana for visualization. The architecture follows a pull-based monitoring pattern where Prometheus scrapes metrics from various exporters at 30-second intervals. The system monitors 8 H200 GPUs, ~10 vLLM containers with varying versions, system resources, and LLM-specific metrics. All components run as Docker containers orchestrated via Docker Compose, with Python 3.12-based custom exporters using Dynaconf for configuration management. The solution operates entirely on an internal network with basic authentication, designed for single-maintainer use with periodic dashboard refresh suitable for the 10-20 requests/minute workload.

## Platform and Infrastructure Choice

**Platform:** On-premise Ubuntu 24.04 Server
**Key Services:** Docker Engine with Compose plugin, NVIDIA Container Toolkit, Prometheus, Grafana, Loki
**Deployment Host and Regions:** Single server deployment, internal network only

## Repository Structure

**Structure:** Monorepo with Docker Compose orchestration
**Monorepo Tool:** Not applicable - single repository with docker-compose.yml
**Package Organization:** 
- `/exporters` - Custom Python exporters
- `/config` - Prometheus, Grafana, Loki configurations  
- `/dashboards` - Grafana dashboard JSON files
- `/docker` - Dockerfiles for custom components
- `/scripts` - Utility and setup scripts

## High Level Architecture Diagram

```mermaid
graph TB
    subgraph "Data Sources"
        S1[System Metrics<br/>CPU/Memory/Disk]
        S2[GPU Metrics<br/>8x H200]
        S3[Docker Metrics<br/>All Containers]
        S4[LiteLLM API<br/>Configurable Port]
        S5[vLLM Metrics<br/>~10 Instances]
        S6[LangFuse API/DB]
    end

    subgraph "Collectors"
        C1[Node Exporter<br/>:9100]
        C2[NVIDIA GPU Exporter<br/>:9445]
        C3[cAdvisor<br/>:8080]
        C4[LiteLLM Exporter<br/>:9901]
        C5[vLLM Exporter<br/>:9902]
        C6[LangFuse Exporter<br/>:9903]
        C7[Promtail<br/>Log Collector]
    end

    subgraph "Storage"
        P[Prometheus<br/>:23001]
        L[Loki<br/>:23002]
        V1[grafana-storage<br/>Docker Volume]
        V2[prometheus-data<br/>Docker Volume]
        V3[loki-data<br/>Docker Volume]
    end

    subgraph "Visualization"
        G[Grafana<br/>:23000]
        D1[System Health<br/>Dashboard]
        D2[GPU Usage<br/>Dashboard]
        D3[Docker Container<br/>Dashboard]
        D4[LiteLLM Status<br/>Dashboard]
        D5[vLLM Docker<br/>Dashboard]
        D6[LangFuse Analytics<br/>Dashboard]
        D7[Logs View]
    end

    S1 --> C1
    S2 --> C2
    S3 --> C3
    S4 --> C4
    S5 --> C5
    S6 --> C6
    S3 --> C7

    C1 --> P
    C2 --> P
    C3 --> P
    C4 --> P
    C5 --> P
    C6 --> P
    C7 --> L

    P --> G
    L --> G
    G --> D1
    G --> D2
    G --> D3
    G --> D4
    G --> D5
    G --> D6
    G --> D7

    P --> V2
    L --> V3
    G --> V1
```

## Architectural Patterns

- **Pull-Based Monitoring:** Prometheus actively scrapes metrics from exporters - *Rationale:* Simplifies firewall rules and provides consistent collection intervals
- **Exporter Pattern:** Each data source has dedicated exporter - *Rationale:* Separation of concerns and independent scaling
- **Time-Series Storage:** Prometheus for metrics, Loki for logs - *Rationale:* Purpose-built databases for each data type
- **Container-First Design:** All components run as Docker containers - *Rationale:* Consistent deployment and easy updates
- **Configuration as Code:** Dynaconf for Python apps, environment variables for containers - *Rationale:* Flexible configuration management with override capability
- **Single Pane of Glass:** Grafana as unified visualization layer - *Rationale:* Reduces context switching for monitoring tasks
- **Volume-Based Persistence:** Docker volumes for all stateful data - *Rationale:* Data survives container restarts and enables backups
