# Core Workflows

Key system workflows illustrating component interactions for primary use cases.

## Metric Collection Workflow

```mermaid
sequenceDiagram
    participant P as Prometheus
    participant NE as Node Exporter
    participant GE as GPU Exporter
    participant VE as vLLM Exporter
    participant LE as LiteLLM Exporter
    participant G as Grafana

    loop Every 30 seconds
        P->>NE: GET /metrics
        NE->>NE: Collect system metrics
        NE-->>P: Return metrics
        
        P->>GE: GET /metrics
        GE->>GE: Query NVML
        GE-->>P: Return GPU metrics
        
        P->>VE: GET /metrics
        VE->>VE: Query Docker API
        VE->>VE: Query vLLM endpoints
        VE-->>P: Return container metrics
        
        P->>LE: GET /metrics
        LE->>LE: Query LiteLLM API
        LE-->>P: Return proxy metrics
    end

    G->>P: Query metrics
    P-->>G: Return time-series data
    G->>G: Render dashboards
```

## GPU Alert Workflow

```mermaid
sequenceDiagram
    participant GE as GPU Exporter
    participant P as Prometheus
    participant G as Grafana
    participant U as User

    GE->>GE: Detect GPU temp > 85°C
    GE->>P: Export metric nvidia_gpu_temperature_celsius{gpu_id="0"} 87
    
    P->>P: Evaluate alert rules
    P->>P: Trigger GPU_HIGH_TEMP alert
    
    G->>P: Query alert status
    P-->>G: Return active alerts
    
    G->>G: Update dashboard
    G->>G: Show alert banner
    G-->>U: Display critical alert
```

## vLLM Container Discovery Workflow

```mermaid
sequenceDiagram
    participant VE as vLLM Exporter
    participant D as Docker API
    participant V as vLLM Container
    participant P as Prometheus

    VE->>D: GET /containers/json?filters={"label":["vllm=true"]}
    D-->>VE: Return container list
    
    loop For each container
        VE->>D: GET /containers/{id}/inspect
        D-->>VE: Return details (image, GPU devices)
        
        VE->>VE: Extract version from image tag
        VE->>VE: Map GPU devices
        
        VE->>V: GET http://{container}:8000/v1/models
        V-->>VE: Return loaded model info
        
        VE->>V: GET http://{container}:8000/metrics
        V-->>VE: Return vLLM metrics
    end
    
    VE->>VE: Aggregate metrics
    P->>VE: GET /metrics
    VE-->>P: Return all vLLM metrics with labels
```

## Mock Data Scenario Change Workflow

```mermaid
sequenceDiagram
    participant U as User
    participant ME as Mock Exporter
    participant P as Prometheus
    participant G at Grafana

    U->>ME: PUT /api/v1/scenario
    Note right of U: {"scenario": "high_load"}
    
    ME->>ME: Load high_load config
    ME->>ME: Update generation parameters
    ME-->>U: 200 OK
    
    loop Every update cycle
        ME->>ME: Generate high load metrics
        Note right of ME: CPU: 80%, GPU: 90%
    end
    
    P->>ME: GET /metrics (next scrape)
    ME-->>P: Return high load metrics
    
    G->>P: Query latest metrics
    P-->>G: Return updated data
    G->>G: Dashboards show high load
```

## AI-Driven Test Execution Workflow

```mermaid
sequenceDiagram
    participant U as User
    participant C as Claude + MCP
    participant PW as Playwright MCP
    participant SS as Screenshot MCP
    participant G as Grafana
    participant ME as Mock Exporter

    U->>C: "Test GPU temperature alerts"
    
    C->>ME: PUT /api/v1/scenario
    Note right of C: Set high GPU temp
    ME-->>C: Scenario updated
    
    C->>PW: Navigate to GPU dashboard
    PW->>G: Open http://localhost:23000
    G-->>PW: Dashboard loaded
    
    C->>PW: Wait for alert banner
    PW->>G: Check for alert element
    G-->>PW: Alert visible
    
    C->>SS: Capture screenshot
    SS->>G: Screenshot dashboard
    SS-->>C: Return image
    
    C->>C: Analyze results
    C-->>U: Test passed + screenshot
```

## Log Collection Workflow

```mermaid
sequenceDiagram
    participant D as Docker Container
    participant PT as Promtail
    participant L as Loki
    participant G as Grafana
    participant U as User

    D->>D: Generate log line
    Note right of D: [ERROR] Model loading failed
    
    PT->>D: Tail container logs
    D-->>PT: Stream log lines
    
    PT->>PT: Parse and label logs
    Note right of PT: {container="vllm-llama3", level="error"}
    
    PT->>L: POST /loki/api/v1/push
    L->>L: Store with timestamp
    L-->>PT: 204 Success
    
    U->>G: Open Logs dashboard
    G->>L: Query: {container="vllm-llama3"} |= "ERROR"
    L-->>G: Return matching logs
    G-->>U: Display log lines
```

## Model Metadata Enrichment Workflow

```mermaid
sequenceDiagram
    participant LE as LiteLLM Exporter
    participant LA as LiteLLM API
    participant HF as Hugging Face API
    participant Cache as Local Cache

    LE->>LA: GET /model/info
    LA-->>LE: Return model list
    
    loop For each new model
        LE->>Cache: Check if metadata cached
        Cache-->>LE: Not found
        
        LE->>HF: GET /api/models/{model_id}
        HF-->>LE: Return model metadata
        Note right of LE: Size, license, downloads
        
        LE->>Cache: Store metadata (24h TTL)
    end
    
    LE->>LE: Enrich metrics with metadata
    Note right of LE: model_size_bytes, quantization
```

## Dashboard Auto-Discovery Workflow (for Testing)

```mermaid
sequenceDiagram
    participant C as Claude + MCP
    participant PW as Playwright MCP
    participant FS as Filesystem MCP
    participant G as Grafana

    C->>PW: Navigate to Grafana
    PW->>G: GET http://localhost:23000
    G-->>PW: Login page
    
    C->>PW: Login with credentials
    PW->>G: POST /login
    G-->>PW: Authenticated
    
    C->>PW: Navigate to dashboards
    PW->>G: GET /dashboards
    G-->>PW: Dashboard list
    
    C->>PW: Extract dashboard info
    PW-->>C: Dashboard names and URLs
    
    C->>FS: Write test plan
    Note right of C: test-plan.json
    FS-->>C: File saved
    
    C->>C: Execute tests per plan
```

These workflows demonstrate the key interactions between components, showing both normal operations and special scenarios like testing and alerting.
