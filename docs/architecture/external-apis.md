# External APIs

The monitoring system integrates with several external APIs to collect LLM-specific metrics and analytics data.

## LiteLLM Admin API

- **Purpose:** Retrieve model routing information, request metrics, and proxy health status
- **Documentation:** https://docs.litellm.ai/docs/proxy/cli
- **Base URL(s):** http://localhost:${LITELLM_PORT} (configurable via environment)
- **Authentication:** API key (optional for internal network)
- **Rate Limits:** None for self-hosted

**Key Endpoints Used:**
- `GET /model/info` - List all configured models with routing info
- `GET /metrics` - Get aggregated metrics (requests, tokens, latency)
- `GET /health` - Proxy health check
- `GET /model/{model_name}/stats` - Per-model statistics

**Integration Notes:** 
- Poll every 30 seconds to match Prometheus scrape interval
- Cache model list for 5 minutes to reduce API calls
- Handle connection failures gracefully (proxy may restart)

## vLLM Metrics API

- **Purpose:** Collect inference engine metrics directly from vLLM containers
- **Documentation:** https://docs.vllm.ai/en/latest/serving/metrics.html
- **Base URL(s):** http://{container_name}:8000 (per vLLM instance)
- **Authentication:** None (internal network)
- **Rate Limits:** None

**Key Endpoints Used:**
- `GET /metrics` - Prometheus-compatible metrics endpoint
- `GET /v1/models` - List loaded models
- `GET /health` - Container health status

**Integration Notes:**
- Each vLLM container exposes metrics independently
- Discover containers dynamically via Docker API
- Extract version from container image tag
- Map container to GPU indices via Docker labels

## Docker Engine API

- **Purpose:** Discover and monitor running containers, extract metadata
- **Documentation:** https://docs.docker.com/engine/api/v1.43/
- **Base URL(s):** unix:///var/run/docker.sock
- **Authentication:** Socket access (mounted in container)
- **Rate Limits:** None

**Key Endpoints Used:**
- `GET /containers/json` - List all containers with details
- `GET /containers/{id}/stats` - Real-time resource usage
- `GET /containers/{id}/logs` - Container logs (for Loki)
- `GET /info` - Docker system information

**Integration Notes:**
- Use filters to identify vLLM containers by image name
- Extract GPU device mappings from HostConfig
- Monitor container lifecycle events for dynamic updates

## LangFuse API

- **Purpose:** Extract LLM usage analytics and quality metrics
- **Documentation:** https://langfuse.com/docs/api
- **Base URL(s):** http://localhost:${LANGFUSE_PORT} (self-hosted)
- **Authentication:** API key via header
- **Rate Limits:** None for self-hosted

**Key Endpoints Used:**
- `GET /api/public/metrics/daily` - Daily usage aggregates
- `GET /api/public/traces` - Recent trace data
- `GET /api/public/sessions` - User session analytics
- `GET /api/public/scores` - Model quality scores

**Integration Notes:**
- Consider direct database access for better performance
- Aggregate data before exposing as Prometheus metrics
- Respect data retention policies
- Handle null scores gracefully

## NVIDIA Management Library (NVML)

- **Purpose:** Direct GPU metrics collection via Python bindings
- **Documentation:** https://developer.nvidia.com/nvidia-management-library-nvml
- **Base URL(s):** N/A (library interface)
- **Authentication:** Root/sudo access required
- **Rate Limits:** Hardware polling limits

**Key Endpoints Used:**
- `nvmlDeviceGetUtilizationRates()` - GPU/Memory utilization
- `nvmlDeviceGetTemperature()` - Temperature sensors
- `nvmlDeviceGetPowerUsage()` - Power consumption
- `nvmlDeviceGetComputeRunningProcesses()` - Process list

**Integration Notes:**
- Initialize NVML once at exporter startup
- Handle driver version compatibility
- Map process PIDs to container names
- Cache device handles for performance

## Hugging Face Model API

- **Purpose:** Retrieve model metadata for display in dashboards
- **Documentation:** https://huggingface.co/docs/api-inference/index
- **Base URL(s):** https://huggingface.co/api/models
- **Authentication:** None for public models
- **Rate Limits:** 1000 requests/hour unauthenticated

**Key Endpoints Used:**
- `GET /api/models/{model_id}` - Model metadata
- `GET /api/models/{model_id}/tree/main` - Model files info

**Integration Notes:**
- Cache model metadata for 24 hours
- Only fetch when new models detected
- Extract model size, quantization info
- Handle private model access gracefully

## Claude API (Testing Only)

- **Purpose:** Power AI-driven dashboard testing via MCP
- **Documentation:** https://docs.anthropic.com/claude/reference/api
- **Base URL(s):** https://api.anthropic.com/v1
- **Authentication:** API key via header
- **Rate Limits:** Based on tier (handle 429s)

**Key Endpoints Used:**
- `POST /messages` - Send test instructions and receive analysis

**Integration Notes:**
- Only used by MCP Test Server component
- Implement exponential backoff for rate limits
- Stream responses for long test executions
- Include screenshots in vision-enabled requests
