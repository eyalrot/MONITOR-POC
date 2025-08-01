# API Specification

The monitoring system uses REST APIs following Prometheus exposition format for metrics and custom APIs for configuration and testing.

## REST API Specification

```yaml
openapi: 3.0.0
info:
  title: LLM Server Monitoring API
  version: 1.0.0
  description: APIs for metrics collection, configuration, and testing
servers:
  - url: http://localhost:{port}
    description: Local monitoring server
    variables:
      port:
        default: '9901'
        enum: ['9100', '9445', '8080', '9901', '9902', '23100']

paths:
  # Prometheus-compatible metrics endpoints
  /metrics:
    get:
      summary: Get Prometheus metrics
      description: Returns metrics in Prometheus exposition format
      tags: [Metrics]
      servers:
        - url: http://localhost:9100
          description: System metrics (Node Exporter)
        - url: http://localhost:9445
          description: GPU metrics (NVIDIA Exporter)
        - url: http://localhost:8080
          description: Container metrics (cAdvisor)
        - url: http://localhost:9901
          description: LiteLLM metrics
        - url: http://localhost:9902
          description: vLLM metrics
      responses:
        200:
          description: Metrics in Prometheus format
          content:
            text/plain:
              schema:
                type: string
                example: |
                  # HELP node_cpu_usage_percent CPU usage percentage
                  # TYPE node_cpu_usage_percent gauge
                  node_cpu_usage_percent 35.2
                  # HELP node_memory_used_bytes Memory used in bytes
                  # TYPE node_memory_used_bytes gauge
                  node_memory_used_bytes 32212254720

  # LiteLLM Exporter API
  /api/v1/models:
    get:
      summary: Get LiteLLM model status
      description: Returns current status of all models managed by LiteLLM
      tags: [LiteLLM]
      servers:
        - url: http://localhost:9901
      responses:
        200:
          description: Model status list
          content:
            application/json:
              schema:
                type: object
                properties:
                  models:
                    type: array
                    items:
                      $ref: '#/components/schemas/ModelStatus'

  # vLLM Exporter API
  /api/v1/containers:
    get:
      summary: Get vLLM container status
      description: Returns status of all vLLM containers with version info
      tags: [vLLM]
      servers:
        - url: http://localhost:9902
      responses:
        200:
          description: Container status list
          content:
            application/json:
              schema:
                type: object
                properties:
                  containers:
                    type: array
                    items:
                      $ref: '#/components/schemas/VLLMContainer'

  # Mock Data Control API
  /api/v1/scenario:
    get:
      summary: Get current mock scenario
      description: Returns the active mock data scenario
      tags: [Mock Control]
      servers:
        - url: http://localhost:9901
      responses:
        200:
          description: Current scenario
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MockScenario'
    
    put:
      summary: Change mock scenario
      description: Switch to a different mock data scenario
      tags: [Mock Control]
      servers:
        - url: http://localhost:9901
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                scenario:
                  type: string
                  enum: [normal, high_load, degraded]
                settings:
                  $ref: '#/components/schemas/MockSettings'
      responses:
        200:
          description: Scenario updated
        400:
          description: Invalid scenario

  # Grafana API (for test discovery)
  /api/search:
    get:
      summary: Search Grafana dashboards
      description: Used by Claude to discover testable dashboards
      tags: [Testing]
      servers:
        - url: http://localhost:23000
      parameters:
        - name: type
          in: query
          schema:
            type: string
            enum: [dash-db]
      responses:
        200:
          description: Dashboard list
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    uid:
                      type: string
                    title:
                      type: string
                    type:
                      type: string

components:
  schemas:
    ModelStatus:
      type: object
      properties:
        model_id:
          type: string
          example: "gpt-4"
        model_name:
          type: string
          example: "gpt-4"
        model_type:
          type: string
          enum: [llm, embedding, reranker]
        status:
          type: string
          enum: [available, loading, error]
        endpoint:
          type: string
          example: "http://localhost:4000/v1/chat/completions"
        current_rpm:
          type: number
          example: 12.5
        error_rate:
          type: number
          example: 0.02

    VLLMContainer:
      type: object
      properties:
        container_name:
          type: string
          example: "vllm-llama3-70b"
        container_id:
          type: string
          example: "a1b2c3d4e5f6"
        image:
          type: string
          example: "vllm/vllm-openai:v0.4.2"
        version:
          type: string
          example: "v0.4.2"
        model_name:
          type: string
          example: "llama3-70b"
        gpu_indices:
          type: array
          items:
            type: integer
          example: [0, 1]
        gpu_memory_used_gb:
          type: number
          example: 60.5
        status:
          type: string
          enum: [running, loading, error]
        uptime_seconds:
          type: integer
          example: 3600

    MockScenario:
      type: object
      properties:
        name:
          type: string
          example: "normal"
        description:
          type: string
          example: "Normal operating conditions"
        settings:
          $ref: '#/components/schemas/MockSettings'

    MockSettings:
      type: object
      properties:
        cpu_load:
          type: number
          example: 30
        gpu_utilization:
          type: number
          example: 60
        error_rate:
          type: number
          example: 0.1
        request_multiplier:
          type: number
          example: 1.0
        enable_anomalies:
          type: boolean
          example: true
```

## Custom Exporter Implementation Pattern

All custom exporters follow this base pattern:

```python