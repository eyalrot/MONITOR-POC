# Product Requirements Document: LLM Server Monitoring System

## 1. Executive Summary

This PRD outlines the requirements for implementing a comprehensive monitoring solution for LLM (Large Language Model) server infrastructure using Grafana as the primary visualization platform. The system will provide real-time insights into server health, GPU utilization (8x NVIDIA H200 GPUs), Docker container status, and LLM-specific metrics. The solution is designed for a single Ubuntu 24.04 server deployment running approximately 10 vLLM containers with varying versions, supporting 10-20 requests/minute workload. The system targets both LLM server maintainers and end users who need to understand available models and endpoints, with all components containerized and orchestrated via Docker Compose v2.

## 2. Objectives

- Provide centralized monitoring for all LLM infrastructure components
- Enable proactive issue detection and resource optimization
- Track model performance and usage metrics
- Facilitate debugging through integrated log access
- Support data-driven capacity planning
- Provide visibility of available models and endpoints for end users
- Communicate important system messages and model lifecycle updates

## 3. System Architecture

### 3.1 Core Components

1. **Grafana** - Primary dashboard and visualization platform (latest Docker image, port 23000)
2. **Prometheus** - Time-series database for metrics collection (v2.x, port 23001, 30-second scrape interval)
3. **Loki** - Log aggregation system for Docker logs (v2.x, port 23002)
4. **Promtail** - Log shipping agent for container logs
5. **Exporters** - Python 3.12/FastAPI-based metric collectors:
   - Node Exporter (system metrics, port 9100)
   - NVIDIA GPU Exporter (GPU metrics via NVML/DCGM, port 9445)
   - cAdvisor (container metrics, port 8080)
   - LiteLLM Exporter (proxy metrics, port 9901)
   - vLLM Exporter (inference metrics, port 9902)
   - LangFuse Exporter (analytics metrics, port 9903)
6. **Configuration** - Dynaconf for Python apps, environment variables for containers
7. **Orchestration** - Docker Compose v2 with systemd service integration

### 3.2 Target Users

1. **LLM Server Maintainers**
   - Need detailed technical metrics
   - Server health and resource utilization
   - Debugging capabilities

2. **End Users**
   - Model availability and endpoints
   - Usage quotas and limits
   - System announcements

### 3.3 Data Flow Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Data Sources  │────▶│    Exporters     │────▶│    Storage       │
├─────────────────┤     ├──────────────────┤     ├──────────────────┤
│ - System (Host) │     │ - Node:9100      │     │ - Prometheus     │
│ - 8x H200 GPUs  │     │ - GPU:9445       │     │   :23001         │
│ - Docker Socket │     │ - cAdvisor:8080  │     │ - Loki           │
│ - LiteLLM API   │     │ - LiteLLM:9901   │     │   :23002         │
│ - vLLM APIs     │     │ - vLLM:9902      │     │ - Docker Volumes │
│ - LangFuse      │     │ - LangFuse:9903  │     └──────────────────┘
│ - Container Logs│     │ - Promtail       │              │
└─────────────────┘     └──────────────────┘              ▼
                                                  ┌──────────────────┐
                                                  │ Grafana:23000    │
                                                  └──────────────────┘
```

## 4. Dashboard Requirements

### 4.1 Server Health Dashboard

**Purpose**: Monitor overall server infrastructure health

**Metrics to Display**:
- CPU utilization (per core and aggregate)
- Memory usage (used/available/cached)
- Disk I/O (read/write rates, IOPS)
- Network traffic (in/out bandwidth)
- System load averages (1/5/15 min)
- Uptime and availability
- Temperature sensors (if available)
- Process count and zombie processes

**Visualizations**:
- Time series graphs for CPU/Memory trends
- Gauge panels for current utilization
- Heatmap for CPU core utilization
- Alert status panel

### 4.2 GPU Usage Dashboard

**Purpose**: Monitor 8x NVIDIA H200 GPU resources critical for LLM operations

**Metrics to Display**:
- GPU utilization percentage (per GPU, 0-7)
- GPU memory usage (allocated/free, 80GB per H200)
- GPU temperature (threshold: warning >75°C, critical >85°C)
- Power consumption (up to 700W per H200)
- GPU clock speeds (graphics and memory)
- CUDA core utilization
- Tensor core utilization
- GPU process list with container mapping
- GPU UUID and name identification

**Visualizations**:
- 8-GPU grid layout comparison panels
- Memory allocation stacked charts (80GB scale)
- Temperature heatmap with thresholds
- GPU-to-container mapping table
- Power consumption trends
- Process memory allocation by container

### 4.3 Docker Container Dashboard

**Purpose**: Monitor containerized services with GPU/non-GPU classification

**Metrics to Display**:

**GPU-Enabled Containers**:
- Container name and status
- GPU memory allocation
- GPU utilization per container
- CUDA version
- Model loading status

**Non-GPU Containers**:
- Container name and status
- CPU usage per container
- Memory usage per container
- Network I/O
- Restart count

**Common Metrics**:
- Container health status
- Uptime
- Resource limits vs usage
- Volume mount status

**Visualizations**:
- Split view panels (GPU vs non-GPU)
- Container resource usage tables
- Status indicators (running/stopped/restarting)
- Resource allocation pie charts

### 4.4 LiteLLM Status Dashboard

**Purpose**: Monitor LiteLLM proxy and model routing (model-agnostic)

**Metrics to Display**:
- Active models and their status (supports any model type: LLMs, embeddings, rerankers)
- Model endpoints and availability
- Request count per model (per minute/hour/day)
- Token usage per model (input/output, per minute/hour/day)
- Response times per model
- Error rates and types
- Queue length
- Model health checks
- Model type classification (LLM/Embedding/Reranker)
- Model size and quantization info
- Hugging Face model ID/source

**Visualizations**:
- Model availability matrix with endpoint URLs
- Request rate time series (with time aggregation selector)
- Token usage graphs (with time aggregation selector)
- Response time histograms
- Error rate trending
- Model catalog table with metadata

### 4.5 vLLM Docker Status Dashboard

**Purpose**: Monitor vLLM inference servers and GPU usage per model

**Metrics to Display**:
- vLLM container status
- GPU memory allocation per model
- GPU utilization percentage per model
- Model loading status
- Batch processing metrics
- Inference latency
- Throughput (requests/sec)
- Queue depth
- KV cache utilization
- Active sequence count
- Model-specific GPU usage over time

**Visualizations**:
- GPU usage per model stacked chart
- Memory allocation per model pie chart
- GPU utilization heatmap by model
- Latency percentile graphs
- Throughput time series
- Model state indicators

### 4.6 LangFuse Analytics Dashboard

**Purpose**: Track LLM usage analytics and quality metrics

**Metrics to Display**:
- Total traces and observations
- Token usage trends
- Cost analysis by model/user
- Latency distributions
- Error tracking
- User activity metrics
- Prompt/completion quality scores
- Model comparison metrics

**Visualizations**:
- Usage trend lines
- Cost breakdown charts
- Quality score distributions
- User activity heatmaps

### 4.7 System Announcements Dashboard

**Purpose**: Communicate important messages to users and maintainers

**Features to Display**:
- Scheduled maintenance windows
- Current system status (operational/degraded/down)
- Model deprecation notices with timelines
- New model availability announcements
- Endpoint changes or updates
- Performance advisories
- Changelog/release notes
- Model migration guides

**Components**:
- Announcement banner (for critical messages)
- Timeline view for scheduled events
- Model lifecycle calendar
- Status indicators for each service
- Message priority levels (Critical/Warning/Info)
- Subscription mechanism for updates

**Data Source**:
- Manual entry through Grafana annotations
- Integration with ticketing system (if available)
- RSS/JSON feed for automated updates

## 5. Data Collection Strategy

### 5.1 Phase 1: Mock Data Architecture

**Mock Exporter Implementation**:
All mock exporters will be implemented as Python 3.12 services using FastAPI, providing Prometheus-compatible metrics endpoints. They will run as separate containers mimicking real exporters.

**Mock Data Components**:
1. **Mock System Metrics Exporter (port 9100)**
   - Simulates Node Exporter metrics
   - CPU usage with daily patterns (20-40% base load)
   - Memory usage patterns (20-40GB of 64GB total)
   - Disk I/O patterns (200-400GB used of 1TB)
   - Network traffic counters
   - Load averages with realistic variations

2. **Mock GPU Metrics Exporter (port 9445)**
   - Simulates 8x H200 GPU metrics
   - GPU utilization based on assigned containers
   - Memory allocation (up to 80GB per GPU)
   - Temperature correlated with utilization
   - Power consumption patterns
   - Process-to-container mapping

3. **Mock Container Metrics Exporter (port 8080)**
   - Simulates ~10 vLLM containers with version tags
   - Container resource usage patterns
   - GPU device mapping
   - Container lifecycle events
   - Network I/O per container

4. **Mock LLM Metrics Exporters (ports 9901-9902)**
   - Request rates (10-20 rpm baseline)
   - Token usage patterns
   - Model-specific latencies
   - Error injection (configurable)
   - Model catalog with metadata

5. **Mock Log Generator**
   - Container log streams
   - Error log injection
   - Structured log formats
   - Configurable log rates

**Scenario Management**:
- Normal operation mode
- High load scenario
- Degraded performance mode
- Maintenance window simulation
- Configurable via environment variables

### 5.2 Phase 2: Data Collection Strategy

**Components to Develop**:

1. **Base Metrics Collection**
   - System metrics collector
   - GPU metrics collector
   - Docker metrics collector

2. **Custom Exporters**
   - LiteLLM metrics exporter
   - vLLM metrics exporter
   - Model metadata collector

3. **Integration Points**:
   - LangFuse API connector
   - Log aggregation setup
   - Announcement management system

## 6. Docker Log Viewing Feature

### 6.1 Requirements

- Select container from dropdown
- View real-time logs
- Search and filter capabilities
- Time range selection
- Log level filtering
- Export functionality

### 6.2 Implementation

**Grafana Loki Integration**:
1. Add Loki as data source
2. Create explore view for logs
3. Build container selector variable
4. Configure log panel with filters

**Query Example**:
```
{container_name="$container"} |= "$search_term"
```

## 7. Alert Configuration

### 7.1 Critical Alerts

- GPU temperature > 85°C
- GPU memory > 95%
- Server CPU > 90% for 5 minutes
- Disk space < 10%
- Container restart loops
- Model loading failures
- High error rates (> 5%)

### 7.2 Warning Alerts

- GPU temperature > 75°C
- Memory usage > 80%
- Response time > 2x baseline
- Cost exceeding budget thresholds

## 8. Implementation Timeline

### Phase 1: Foundation & Mock Development (Week 1-3)
- Initialize monorepo structure with defined directories
- Set up Docker Compose v2 configurations
- Deploy Prometheus, Loki, and Grafana stack
- Implement base mock exporter framework (Python 3.12/FastAPI)
- Create all mock data generators with scenario management
- Develop and deploy all dashboards using mock data
- Validate visualizations with realistic data patterns

### Phase 2: Dashboard Development (Week 3-5) *Can run parallel with Phase 3*
- System Health Dashboard with multi-core CPU views
- GPU Usage Dashboard (8x H200 grid layout)
- Docker Container Dashboard (GPU/non-GPU split view)
- LiteLLM Status Dashboard with model catalog
- vLLM Docker Status Dashboard with version tracking
- LangFuse Analytics Dashboard
- Log Explorer with Loki integration
- System Announcements Dashboard

### Phase 3: Real Exporter Development (Week 3-6) *Can run parallel with Phase 2*
- Implement base exporter framework with Dynaconf
- Develop Node Exporter (port 9100)
- Create GPU Exporter with NVML/DCGM (port 9445)
- Build Container Exporter with docker-py (port 8080)
- Implement LiteLLM Exporter (port 9901)
- Create vLLM Exporter with container discovery (port 9902)
- Develop LangFuse Exporter (port 9903)

### Phase 4: Integration & Testing (Week 6-7)
- Replace mock exporters with real ones incrementally
- Configure Prometheus scraping (30-second intervals)
- Set up Promtail for log collection
- Implement AI-driven E2E testing with MCP
- Configure Percy for visual regression testing
- Performance optimization and alert configuration

### Phase 5: Operationalization (Week 8)
- Create production Docker Compose configs
- Set up systemd service integration
- Implement backup/restore procedures
- Configure 30-day retention policies
- Create maintenance scripts
- Documentation and training

## 9. Technical Requirements

### 9.1 Hardware Requirements

**Monitoring Server**:
- Platform: Ubuntu 24.04 Server
- CPU: 4+ cores (monitoring overhead minimal)
- RAM: 16GB minimum (for Prometheus/Grafana/Loki)
- Storage: 100GB SSD (30-day retention for metrics and logs)
- Network: 1Gbps (internal network only)
- GPUs: 8x NVIDIA H200 (80GB each) - monitored, not used by monitoring

### 9.2 Software Requirements

**Base Platform**:
- Ubuntu 24.04 LTS
- Docker Engine (latest) with Compose plugin v2
- NVIDIA Container Toolkit (for GPU metric access)
- systemd (for service management)

**Technology Stack**:
- All components containerized
- Python 3.12 for custom exporters
- FastAPI for exporter HTTP endpoints
- Dynaconf for configuration management
- prometheus_client for metrics exposition
- docker-py for container discovery
- py3nvml or dcgm-exporter for GPU metrics
- httpx for API integrations

### 9.3 Access Requirements

- Read access to LiteLLM admin API
- Docker socket access for container metrics
- NVIDIA GPU driver access through container runtime
- LangFuse API credentials or database access
- Hugging Face model metadata access

### 9.4 Data Retention

- Metrics retention: 1 month (30 days)
- Log retention: 1 month (30 days)
- Automatic cleanup of older data

## 10. Security Considerations

- Basic authentication for Grafana (username/password)
- Internal network only - no external access
- API credentials stored in .env files
- No TLS required for POC phase (internal network)
- Standard Docker security practices

## 11. Repository Structure

The project follows a monorepo structure with clear separation of concerns:

```
llm-monitor/
├── exporters/           # Custom Python exporters
│   ├── base/           # Base exporter framework
│   ├── node/           # System metrics exporter
│   ├── gpu/            # GPU metrics exporter
│   ├── container/      # Docker metrics exporter
│   ├── litellm/        # LiteLLM metrics exporter
│   ├── vllm/           # vLLM metrics exporter
│   ├── langfuse/       # LangFuse metrics exporter
│   └── mock/           # Mock data generators
├── config/             # Configuration files
│   ├── prometheus/     # Prometheus configs and rules
│   ├── grafana/        # Grafana provisioning
│   ├── loki/           # Loki configuration
│   └── promtail/       # Log shipping config
├── dashboards/         # Grafana dashboard JSON files
├── docker/             # Dockerfiles and compose files
├── scripts/            # Utility and setup scripts
├── tests/              # Test suites
│   ├── unit/           # Unit tests (pytest)
│   ├── integration/    # Integration tests
│   └── e2e/            # E2E tests (Playwright + MCP)
└── docs/               # Documentation

```

## 12. Testing Strategy

### 12.1 Unit Testing
- pytest 8.x for Python exporter testing
- Mock external dependencies (APIs, Docker socket)
- Test metric generation logic
- Validate Prometheus exposition format

### 12.2 Integration Testing
- Test Prometheus scraping of all exporters
- Validate data flow from exporters to storage
- Test Grafana data source queries
- Verify log aggregation pipeline

### 12.3 AI-Driven E2E Testing
- Use existing MCP servers (Playwright, Screenshot, Filesystem)
- Claude-based test orchestration
- Automated dashboard interaction testing
- Visual regression with Percy
- Test scenarios:
  - Dashboard loading and rendering
  - Metric data validation
  - Alert triggering
  - Log search functionality
  - Time range navigation

### 12.4 Mock Data Testing
- Validate all mock exporters match real exporter interfaces
- Test scenario switching
- Verify realistic data patterns
- Test edge cases and error conditions

## 13. Maintenance & Operations

### 13.1 Regular Tasks

- Daily health checks of all exporters
- Weekly metrics retention cleanup (>30 days)
- Monthly dashboard performance review
- Quarterly threshold adjustments
- Container image updates
- Security patch management
- Alert rule optimization

### 13.2 Backup Strategy

- Daily Grafana dashboard exports
- Prometheus data snapshots
- Configuration version control

## 14. Success Metrics

- 99% monitoring system uptime
- < 30 second metric collection delay (Prometheus scrape interval)
- < 10% false positive alert rate
- 100% critical incident detection
- < 5 minute MTTR for issue identification
- User satisfaction with model visibility
- Successful parallel development of dashboards and exporters

## 15. Deliverables

### Phase 1 Deliverables
1. **Grafana Instance** with all dashboards configured
2. **Mock Data Generator** producing realistic metrics
3. **Complete Dashboard Set**:
   - Server Health Dashboard
   - GPU Usage Dashboard
   - Docker Container Dashboard (GPU/Non-GPU split)
   - LiteLLM Status Dashboard
   - vLLM Docker Status Dashboard
   - LangFuse Analytics Dashboard
   - System Announcements Dashboard
4. **Dashboard Documentation** with screenshots and usage guide
5. **Feedback Report** from user testing

### Phase 2 & 3 Deliverables (Parallel Development)
1. **Custom Python Exporters** (all containerized):
   - Base exporter framework (FastAPI + Dynaconf)
   - Node Exporter (port 9100)
   - GPU Exporter with NVML/DCGM (port 9445)
   - Container Exporter with docker-py (port 8080)
   - LiteLLM Exporter (port 9901)
   - vLLM Exporter with discovery (port 9902)
   - LangFuse Exporter (port 9903)
2. **Complete Dashboard Suite** (8 dashboards)
3. **Docker Compose Configurations** (dev, prod, mock)

### Phase 4 & 5 Deliverables
1. **Integrated Monitoring System** with real data
2. **AI-Driven Testing Suite** using MCP
3. **Visual Regression Tests** with Percy
4. **systemd Service Integration**
5. **Operations Manual** with runbooks
6. **Maintenance Scripts** in /scripts
7. **CLAUDE.md** for AI assistant context

## 16. Future Enhancements

- Machine learning for anomaly detection
- Predictive scaling recommendations
- Cost optimization suggestions
- Automated remediation actions
- Multi-cluster monitoring support

## 15. Implementation Epics

### Epic 1: Infrastructure Setup & Base Monitoring
**Goal**: Establish core monitoring infrastructure with Prometheus, Grafana, and basic system metrics

**Stories**:
1. **Project Initialization**
   - Create project repository structure
   - Initialize Docker Compose configuration
   - Set up .env template with required variables
   - Create README with setup instructions

2. **Prometheus Setup**
   - Configure Prometheus container
   - Set up prometheus.yml with scrape configs
   - Configure data retention (30 days)
   - Test Prometheus UI access on port 23001

3. **Grafana Setup**
   - Deploy Grafana container (latest)
   - Configure basic authentication
   - Set up Prometheus as data source
   - Configure Grafana on port 23000

4. **System Metrics Collection**
   - Deploy Node Exporter for system metrics
   - Configure Prometheus to scrape Node Exporter
   - Verify metrics collection
   - Create basic system health dashboard

5. **Container Metrics Setup**
   - Deploy cAdvisor for container metrics
   - Configure Docker socket access
   - Set up Prometheus scraping for cAdvisor
   - Test container metrics visibility

### Epic 2: GPU Monitoring Integration
**Goal**: Enable comprehensive GPU monitoring for all 8 H200 GPUs

**Stories**:
1. **NVIDIA GPU Exporter Setup**
   - Deploy NVIDIA GPU exporter container
   - Configure NVIDIA runtime access
   - Set up Prometheus scraping
   - Verify GPU metrics collection

2. **GPU Dashboard Creation**
   - Design multi-GPU visualization layout
   - Create GPU utilization panels
   - Add GPU memory tracking
   - Implement temperature monitoring
   - Add power consumption metrics

3. **GPU Process Monitoring**
   - Track GPU processes and memory allocation
   - Create per-container GPU usage views
   - Add CUDA version tracking
   - Implement GPU allocation tables

### Epic 3: Log Management System
**Goal**: Implement centralized log collection and viewing with Loki

**Stories**:
1. **Loki Setup**
   - Deploy Loki container
   - Configure storage and retention
   - Set up on designated port (23002)
   - Test Loki API access

2. **Promtail Configuration**
   - Deploy Promtail for log collection
   - Configure Docker log scraping
   - Set up log parsing rules
   - Test log ingestion

3. **Grafana Log Integration**
   - Add Loki as Grafana data source
   - Create log exploration dashboard
   - Implement container log filtering
   - Add search and filter capabilities

### Epic 4: LLM-Specific Monitoring
**Goal**: Create custom monitoring for LiteLLM and vLLM services

**Stories**:
1. **LiteLLM Metrics Exporter**
   - Develop custom exporter for LiteLLM API
   - Collect model availability metrics
   - Track request rates and token usage
   - Export response times and error rates

2. **vLLM Metrics Collection**
   - Create vLLM metrics exporter
   - Monitor model loading status
   - Track inference latency
   - Collect batch processing metrics

3. **LLM Dashboards**
   - Create LiteLLM status dashboard
   - Build vLLM performance dashboard
   - Add model catalog view
   - Implement request/token analytics

4. **Model Metadata Integration**
   - Integrate Hugging Face model info
   - Display model types and sizes
   - Show quantization details
   - Track model versioning

### Epic 5: Analytics & Observability
**Goal**: Integrate LangFuse analytics and create comprehensive monitoring views

**Stories**:
1. **LangFuse Integration**
   - Connect to self-hosted LangFuse
   - Create metrics exporter for LangFuse data
   - Set up API authentication
   - Test data collection

2. **Analytics Dashboard**
   - Create usage analytics views
   - Build cost analysis panels
   - Add quality metrics tracking
   - Implement user activity monitoring

3. **Alerting System**
   - Configure Prometheus alerting rules
   - Set up critical alerts (GPU >85°C, etc.)
   - Create warning alerts
   - Test alert notifications

### Epic 6: User Experience & Documentation
**Goal**: Polish dashboards and create comprehensive documentation

**Stories**:
1. **Dashboard Organization**
   - Create dashboard folders structure
   - Set up navigation between dashboards
   - Configure default home dashboard
   - Add dashboard descriptions

2. **System Announcements**
   - Create announcements dashboard
   - Implement manual announcement entry
   - Add status indicators
   - Create maintenance calendar view

3. **Documentation**
   - Write operations manual
   - Create troubleshooting guide
   - Document dashboard usage
   - Prepare training materials

4. **Testing & Validation**
   - Test all dashboards with real data
   - Validate alert thresholds
   - Performance optimization
   - User acceptance testing

### Epic 7: Mock Data Development (Parallel Track)
**Goal**: Create realistic mock data for early dashboard development

**Stories**:
1. **Mock Data Generator**
   - Build configurable data generator
   - Create realistic metric patterns
   - Implement anomaly injection
   - Support all metric types

2. **Mock Data Integration**
   - Set up mock Prometheus endpoints
   - Create fake log streams
   - Simulate model metrics
   - Test with Grafana

### Development Sequence:
1. Epic 1 & Epic 7 (parallel) - Week 1-2
2. Epic 2 & Epic 3 - Week 2-3
3. Epic 4 - Week 3-4
4. Epic 5 - Week 4-5
5. Epic 6 - Week 5-6
6. Integration & Testing - Week 6-7
7. Documentation & Handover - Week 8