# Epic 002: Mock Data Infrastructure

## Epic Goal
Implement a comprehensive mock data generation system that simulates all monitoring metrics with realistic patterns, enabling parallel dashboard development without dependencies on real exporters or infrastructure.

## Epic Description

**Purpose:**
Create mock exporters that perfectly mimic the interfaces of real exporters while generating realistic time-series data. This enables frontend development to proceed independently and provides a testing framework for dashboard validation.

**Key Deliverables:**
- Base mock exporter framework
- Mock exporters for all data sources
- Scenario management system
- Pattern generation for realistic metrics
- Configuration system for different scenarios

## User Stories

### Story 1: Base Mock Exporter Framework
**As a** developer  
**I want** a reusable base framework for mock exporters  
**So that** all mock exporters share common functionality

**Acceptance Criteria:**
- Create Python 3.12 base class using FastAPI
- Implement Prometheus metrics endpoint (/metrics)
- Add health check endpoint (/health)
- Support configurable update intervals
- Include time-based pattern generation utilities
- Add Dynaconf integration for configuration

### Story 2: System and Infrastructure Mock Exporters
**As a** dashboard developer  
**I want** mock exporters for system and GPU metrics  
**So that** I can develop infrastructure dashboards

**Acceptance Criteria:**
- Create Mock Node Exporter (port 9100)
  - CPU usage with daily patterns (20-40% base)
  - Memory patterns (20-40GB of 64GB)
  - Disk I/O and network metrics
  - Load averages with variations
- Create Mock GPU Exporter (port 9445)
  - 8x H200 GPU simulation
  - GPU utilization per container assignment
  - Memory allocation up to 80GB per GPU
  - Temperature correlated with utilization
  - Power consumption patterns

### Story 3: Container and LLM Mock Exporters
**As a** dashboard developer  
**I want** mock exporters for container and LLM metrics  
**So that** I can develop application-specific dashboards

**Acceptance Criteria:**
- Create Mock Container Exporter (port 8080)
  - ~10 vLLM containers with version tags
  - GPU device mapping simulation
  - Container lifecycle events
  - Resource usage patterns
- Create Mock LiteLLM Exporter (port 9901)
  - Model catalog with varied types
  - Request rates (10-20 rpm baseline)
  - Token usage patterns
  - Response time distributions
- Create Mock vLLM Exporter (port 9902)
  - Container discovery simulation
  - Model-to-GPU mapping
  - Inference metrics

### Story 4: Scenario Management System
**As a** tester  
**I want** to switch between different scenarios  
**So that** I can test various system states

**Acceptance Criteria:**
- Implement scenario configuration system
- Create "normal" scenario (baseline operations)
- Create "high_load" scenario (90% utilization)
- Create "degraded" scenario (errors and failures)
- Add API endpoint for scenario switching
- Support environment variable overrides
- Include anomaly injection capabilities

### Story 5: Mock Log Generation
**As a** dashboard developer  
**I want** realistic log streams  
**So that** I can develop log exploration features

**Acceptance Criteria:**
- Create mock log generator for containers
- Generate structured logs in Docker format
- Include error log injection
- Support configurable log rates
- Integrate with Promtail/Loki pipeline
- Add realistic log patterns (startup, errors, warnings)

## Technical Requirements

**Technology Stack:**
- Python 3.12 with FastAPI
- prometheus_client library
- NumPy for pattern generation
- Dynaconf for configuration
- Docker for containerization

**Patterns to Implement:**
- Daily cycles (sine wave patterns)
- Hourly variations
- Random noise generation
- Spike injection (2% probability)
- Correlated metrics (GPU temp with utilization)
- Increasing counters (network, requests)

## Dependencies
- Epic 001: Project Foundation (must be complete)

## Definition of Done
- [ ] All mock exporters match real exporter interfaces
- [ ] Metrics follow Prometheus naming conventions
- [ ] Realistic patterns verified visually
- [ ] Scenario switching works via API
- [ ] All exporters containerized
- [ ] Docker Compose integration complete
- [ ] Configuration documented
- [ ] Grafana can query all mock metrics

## Estimated Effort
- **Duration:** 1 week
- **Team Size:** 2 developers
- **Priority:** Critical (enables parallel development)

## Risk Mitigation
- **Risk:** Mock data doesn't match real data patterns
- **Mitigation:** Research actual metric patterns, implement configurable ranges
- **Risk:** Performance issues with pattern generation
- **Mitigation:** Optimize calculations, cache generated values

## Notes
- Mock exporters must be indistinguishable from real ones to Prometheus
- Focus on realistic patterns that expose edge cases
- All configuration should be adjustable without rebuilding