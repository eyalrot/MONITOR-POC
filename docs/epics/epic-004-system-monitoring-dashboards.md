# Epic 004: Basic System Monitoring Dashboards

## Epic Goal
Create comprehensive system monitoring dashboards for infrastructure health, GPU utilization, and container status using mock data, establishing visualization patterns that will seamlessly transition to real data.

## Epic Description

**Purpose:**
Develop the foundational monitoring dashboards that provide visibility into system health, GPU resources, and container operations. These dashboards form the core operational view for maintaining LLM infrastructure.

**Key Deliverables:**
- System Health Dashboard with CPU, memory, disk, network metrics
- GPU Usage Dashboard for 8x H200 monitoring
- Docker Container Dashboard with GPU/non-GPU split view
- Consistent visual design patterns
- Alert panels and thresholds

## User Stories

### Story 1: System Health Dashboard
**As a** system administrator  
**I want** a comprehensive system health dashboard  
**So that** I can monitor server resources at a glance

**Acceptance Criteria:**
- Create dashboard with organized panel layout
- Add CPU utilization graphs (per-core and aggregate)
- Add memory usage gauges and trends
- Add disk I/O and space utilization
- Add network traffic in/out graphs
- Add system load average panel
- Configure auto-refresh (30 seconds)
- Add alert status summary panel
- Use consistent color schemes for thresholds
- Add drill-down links to detailed views

### Story 2: GPU Usage Dashboard (8x H200)
**As a** ML engineer  
**I want** detailed GPU monitoring for all 8 H200s  
**So that** I can optimize GPU resource allocation

**Acceptance Criteria:**
- Create 8-GPU grid layout (2x4 or 4x2)
- Add GPU utilization percentage per card
- Add GPU memory usage (80GB scale)
- Add temperature monitoring with thresholds
  - Normal: <75°C (green)
  - Warning: 75-85°C (yellow)
  - Critical: >85°C (red)
- Add power consumption graphs
- Add GPU-to-container mapping table
- Show process list per GPU
- Add GPU clock speeds panel
- Include GPU UUID and name labels
- Add utilization heatmap across all GPUs

### Story 3: Docker Container Dashboard
**As a** DevOps engineer  
**I want** container monitoring split by GPU usage  
**So that** I can manage both ML and support containers

**Acceptance Criteria:**
- Create two-section layout (GPU vs non-GPU)
- GPU-Enabled Containers section:
  - Container status indicators
  - GPU memory allocation
  - GPU indices mapping
  - Model loading status
  - CUDA version info
- Non-GPU Containers section:
  - Container health status
  - CPU/memory usage
  - Network I/O stats
  - Restart counts
- Add container lifecycle timeline
- Include version tags for vLLM containers
- Add container log quick links

### Story 4: Dashboard Templates and Variables
**As a** dashboard user  
**I want** interactive filtering capabilities  
**So that** I can focus on specific resources

**Acceptance Criteria:**
- Create dashboard variables for:
  - Time range selection
  - GPU selection (0-7, All)
  - Container name filtering
  - Metric aggregation intervals
- Add variable dropdowns to all dashboards
- Implement drill-down navigation
- Create dashboard links between related views
- Add export functionality
- Configure mobile-responsive layouts

### Story 5: Alert Visualization Panels
**As a** on-call engineer  
**I want** clear alert status visualization  
**So that** I can quickly identify issues

**Acceptance Criteria:**
- Add alert status panels to each dashboard
- Create unified alert overview dashboard
- Implement color-coded severity levels
- Add alert history graphs
- Include threshold breach indicators
- Create alert annotation overlays
- Add silence/acknowledge functionality
- Include alert routing information

## Technical Requirements

**Grafana Features:**
- Panel types: Graph, Gauge, Stat, Table, Heatmap
- Variables and templating
- Dashboard provisioning via JSON
- Annotation support
- Alert visualization

**Query Patterns:**
- PromQL for metrics aggregation
- Rate calculations for counters
- Histogram quantiles
- Multi-series graphs
- Table transformations

**Visual Standards:**
- Consistent color palette
- Threshold-based coloring
- Responsive grid layouts
- Dark theme optimization
- Accessibility considerations

## Dependencies
- Epic 002: Mock Data Infrastructure (providing data)
- Epic 003: Core Monitoring Stack (Grafana ready)

## Definition of Done
- [ ] All three dashboards created and tested
- [ ] Mock data properly visualized
- [ ] Variables and filtering working
- [ ] Alert panels configured
- [ ] Visual consistency verified
- [ ] Performance acceptable (<2s load)
- [ ] JSON exports saved to /dashboards
- [ ] Documentation with screenshots

## Estimated Effort
- **Duration:** 1 week
- **Team Size:** 1-2 developers
- **Priority:** High (core functionality)

## Risk Mitigation
- **Risk:** Dashboard performance with many panels
- **Mitigation:** Optimize queries, use recording rules
- **Risk:** Visual inconsistency across dashboards
- **Mitigation:** Create style guide, reuse components
- **Risk:** Mock data not realistic enough
- **Mitigation:** Iterate with domain experts

## Notes
- These dashboards set the visual standard for all others
- Design for both technical and non-technical users
- Consider colorblind-friendly palettes
- Test on different screen sizes