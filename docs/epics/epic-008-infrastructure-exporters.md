# Epic 008: Infrastructure Exporters

## Epic Goal
Implement production-ready exporters for system metrics, GPU monitoring, and container metrics that collect real data from the infrastructure, replacing mock exporters while maintaining the same interfaces.

## Epic Description

**Purpose:**
Develop the core infrastructure exporters that monitor system resources, GPU utilization, and container metrics. These exporters have no external API dependencies and form the foundation of infrastructure monitoring.

**Key Deliverables:**
- Node Exporter for system metrics
- GPU Exporter for NVIDIA H200 monitoring  
- Container Exporter for Docker metrics
- Proper error handling and recovery
- Production-ready containerization

## User Stories

### Story 1: Node Exporter Implementation
**As a** system administrator  
**I want** real system metrics collection  
**So that** I can monitor server health accurately

**Acceptance Criteria:**
- Implement exporter inheriting from base framework
- Collect system metrics:
  - CPU usage per core and total
  - Memory (used, free, cached, buffers)
  - Disk I/O (read/write bytes, IOPS)
  - Network I/O per interface
  - Load averages (1, 5, 15 min)
  - System uptime
- Handle metric collection errors gracefully
- Optimize for minimal resource usage
- Match Prometheus node_exporter format
- Add Linux /proc parsing
- Include temperature sensors if available
- Test on Ubuntu 24.04

### Story 2: GPU Exporter with NVML
**As a** ML engineer  
**I want** detailed GPU metrics for all H200s  
**So that** I can monitor GPU resource usage

**Acceptance Criteria:**
- Implement exporter using py3nvml or dcgm
- Collect metrics for all 8 GPUs:
  - GPU utilization percentage
  - Memory used/free (80GB total)
  - Temperature readings
  - Power consumption
  - Clock speeds (graphics, memory)
  - Process list with memory usage
  - GPU UUID and index mapping
- Map processes to containers
- Handle NVIDIA driver errors
- Support GPU hot-plug events
- Add GPU health status
- Include ECC error counts

### Story 3: Container Metrics Exporter
**As a** DevOps engineer  
**I want** Docker container metrics  
**So that** I can monitor container resource usage

**Acceptance Criteria:**
- Implement exporter using docker-py
- Collect container metrics:
  - CPU usage (seconds, percentage)
  - Memory usage and limits
  - Network I/O statistics
  - Block I/O statistics
  - Container status and health
  - Restart count
  - Created/started timestamps
- Identify GPU-enabled containers
- Extract container labels and tags
- Handle Docker API errors
- Support container lifecycle events
- Add image version tracking

### Story 4: Exporter Containerization
**As a** platform engineer  
**I want** properly containerized exporters  
**So that** deployment is consistent and secure

**Acceptance Criteria:**
- Create optimized Dockerfiles:
  - Multi-stage builds
  - Minimal base images
  - Security scanning
  - Non-root user
- Configure for each exporter:
  - Node: Host network, read-only mounts
  - GPU: NVIDIA runtime, device access
  - Container: Docker socket mount
- Add health check commands
- Implement resource limits
- Create docker-compose entries
- Test container restart behavior

### Story 5: Integration Testing Suite
**As a** QA engineer  
**I want** comprehensive integration tests  
**So that** exporters work reliably in production

**Acceptance Criteria:**
- Create integration test suite:
  - Metric format validation
  - Prometheus scraping tests
  - Performance benchmarks
  - Resource leak detection
  - Error injection tests
- Add mock infrastructure:
  - Fake /proc filesystem
  - Mock NVIDIA libraries
  - Docker API simulator
- Implement CI/CD tests
- Add load testing scenarios
- Create monitoring dashboards
- Document test coverage

## Technical Requirements

**System Metrics:**
- Parse /proc filesystem
- Handle counter overflows
- Support multiple network interfaces
- Calculate rates correctly

**GPU Metrics:**
- NVIDIA driver 550+
- Handle multi-GPU systems
- Support MIG instances
- Binary compatibility

**Container Metrics:**
- Docker API v1.41+
- Handle API version negotiation
- Support cgroup v2
- Label extraction

**Performance:**
- <100ms collection time
- <50MB memory usage
- Minimal CPU overhead
- Efficient API calls

## Dependencies
- Epic 007: Base Exporter Framework
- Host system access requirements
- NVIDIA driver installation
- Docker API access

## Definition of Done
- [ ] All three exporters implemented
- [ ] Metrics match mock exporter format
- [ ] Error handling comprehensive
- [ ] Performance requirements met
- [ ] Containers built and tested
- [ ] Integration tests passing
- [ ] Documentation complete
- [ ] Prometheus scraping verified

## Estimated Effort
- **Duration:** 1.5 weeks
- **Team Size:** 2 developers
- **Priority:** High (core infrastructure)

## Risk Mitigation
- **Risk:** System compatibility issues
- **Mitigation:** Test on target Ubuntu 24.04, handle edge cases
- **Risk:** NVIDIA driver incompatibility
- **Mitigation:** Support multiple driver versions, graceful degradation
- **Risk:** Docker API changes
- **Mitigation:** Version negotiation, compatibility layer

## Notes
- These exporters run on every monitored system
- Optimize for reliability over features
- Consider security implications of access
- Plan for horizontal scaling