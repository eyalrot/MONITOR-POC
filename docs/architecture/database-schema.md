# Database Schema

Transform the conceptual data models into concrete database schemas for Prometheus time-series storage and Loki log aggregation.

## Prometheus Time-Series Schema

Prometheus uses a multi-dimensional data model with metrics identified by name and key-value pairs (labels). All metrics are stored as time series.

### Metric Naming Convention

```