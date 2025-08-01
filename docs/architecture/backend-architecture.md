# Backend Architecture

Define backend-specific architecture details for the monitoring system's data collection and processing components.

## Service Architecture

The monitoring system uses a microservices approach with containerized exporters, each responsible for specific metric collection.

### Exporter Service Organization

```
/exporters/
├── base/                           # Base exporter framework
│   ├── Dockerfile.base
│   ├── requirements.txt
│   └── src/
│       ├── base_exporter.py        # Abstract base class
│       ├── metrics_registry.py     # Prometheus registry management
│       └── config_loader.py        # Dynaconf integration
├── node/                           # System metrics exporter
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── main.py
│       ├── collectors/
│       │   ├── cpu_collector.py
│       │   ├── memory_collector.py
│       │   ├── disk_collector.py
│       │   └── network_collector.py
│       └── config/
│           └── settings.yaml
├── gpu/                            # GPU metrics exporter
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── main.py
│       ├── nvidia_collector.py
│       ├── process_mapper.py      # Map processes to containers
│       └── config/
│           └── settings.yaml
├── container/                      # Docker metrics exporter
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── main.py
│       ├── docker_collector.py
│       ├── gpu_mapper.py          # GPU device mapping
│       └── config/
│           └── settings.yaml
├── litellm/                        # LiteLLM metrics exporter
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── main.py
│       ├── api_client.py
│       ├── model_collector.py
│       └── config/
│           └── settings.yaml
├── vllm/                           # vLLM metrics exporter
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── main.py
│       ├── container_discovery.py
│       ├── metrics_collector.py
│       └── config/
│           └── settings.yaml
└── mock/                           # Mock data generator
    ├── Dockerfile
    ├── requirements.txt
    └── src/
        ├── main.py
        ├── scenario_manager.py
        ├── pattern_generator.py
        └── config/
            └── scenarios.yaml
```

### Base Exporter Template

```python