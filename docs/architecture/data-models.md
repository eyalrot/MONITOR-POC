# Data Models

Core data models that will be collected and stored in the monitoring system. These models represent the primary entities tracked across all components.

## System Metrics

**Purpose:** Track overall server health and resource utilization

**Key Attributes:**
- timestamp: datetime - Collection time
- hostname: string - Server identifier
- cpu_usage_percent: float - CPU utilization (0-100)
- memory_used_bytes: int - Memory usage in bytes
- memory_total_bytes: int - Total memory in bytes
- disk_used_bytes: int - Disk usage in bytes
- disk_total_bytes: int - Total disk space in bytes
- network_rx_bytes: int - Network received bytes/sec
- network_tx_bytes: int - Network transmitted bytes/sec
- load_1m: float - 1-minute load average
- load_5m: float - 5-minute load average
- load_15m: float - 15-minute load average

**TypeScript Interface:**
```typescript
interface SystemMetrics {
  timestamp: string;
  hostname: string;
  cpu_usage_percent: number;
  memory_used_bytes: number;
  memory_total_bytes: number;
  disk_used_bytes: number;
  disk_total_bytes: number;
  network_rx_bytes: number;
  network_tx_bytes: number;
  load_1m: number;
  load_5m: number;
  load_15m: number;
}
```

**Relationships:**
- One-to-many with Container Metrics (host contains containers)
- One-to-many with GPU Metrics (host contains GPUs)

## GPU Metrics

**Purpose:** Monitor GPU health and utilization for all 8 H200 GPUs

**Key Attributes:**
- timestamp: datetime - Collection time
- gpu_id: int - GPU index (0-7)
- gpu_uuid: string - GPU unique identifier
- gpu_name: string - GPU model name (H200)
- utilization_percent: float - GPU utilization (0-100)
- memory_used_bytes: int - GPU memory used
- memory_total_bytes: int - Total GPU memory
- temperature_celsius: float - GPU temperature
- power_watts: float - Power consumption
- clock_graphics_mhz: int - Graphics clock speed
- clock_memory_mhz: int - Memory clock speed
- processes: array - List of processes using GPU

**TypeScript Interface:**
```typescript
interface GPUMetrics {
  timestamp: string;
  gpu_id: number;
  gpu_uuid: string;
  gpu_name: string;
  utilization_percent: number;
  memory_used_bytes: number;
  memory_total_bytes: number;
  temperature_celsius: number;
  power_watts: number;
  clock_graphics_mhz: number;
  clock_memory_mhz: number;
  processes: GPUProcess[];
}

interface GPUProcess {
  pid: number;
  name: string;
  memory_used_bytes: number;
}
```

**Relationships:**
- Many-to-one with System Metrics (GPUs belong to host)
- One-to-many with vLLM Containers (GPU used by containers)

## Container Metrics

**Purpose:** Track resource usage and health of all Docker containers

**Key Attributes:**
- timestamp: datetime - Collection time
- container_id: string - Docker container ID
- container_name: string - Container name
- image: string - Docker image name with tag
- status: string - running/stopped/restarting
- cpu_usage_percent: float - Container CPU usage
- memory_used_bytes: int - Container memory usage
- memory_limit_bytes: int - Container memory limit
- network_rx_bytes: int - Network received
- network_tx_bytes: int - Network transmitted
- restart_count: int - Number of restarts
- created_at: datetime - Container creation time
- gpu_enabled: boolean - Whether container uses GPU
- gpu_indices: array<int> - GPU indices if GPU-enabled

**TypeScript Interface:**
```typescript
interface ContainerMetrics {
  timestamp: string;
  container_id: string;
  container_name: string;
  image: string;
  status: 'running' | 'stopped' | 'restarting';
  cpu_usage_percent: number;
  memory_used_bytes: number;
  memory_limit_bytes: number;
  network_rx_bytes: number;
  network_tx_bytes: number;
  restart_count: number;
  created_at: string;
  gpu_enabled: boolean;
  gpu_indices: number[];
}
```

**Relationships:**
- Many-to-one with System Metrics (containers run on host)
- Many-to-many with GPU Metrics (containers can use multiple GPUs)
- One-to-one with vLLM Model Metrics (for vLLM containers)

## LLM Model Metrics

**Purpose:** Track LLM-specific metrics for models served by LiteLLM and vLLM

**Key Attributes:**
- timestamp: datetime - Collection time
- model_id: string - Unique model identifier
- model_name: string - Model name (e.g., "llama-3-8b")
- model_type: string - LLM/Embedding/Reranker
- provider: string - vLLM/LiteLLM
- endpoint: string - API endpoint URL
- status: string - available/loading/error
- requests_per_minute: float - Request rate
- tokens_per_minute_input: int - Input token rate
- tokens_per_minute_output: int - Output token rate
- avg_latency_ms: float - Average response time
- error_rate_percent: float - Error percentage
- model_size_bytes: int - Model size on disk
- quantization: string - Quantization type (e.g., "int8")
- version: string - Model version
- container_name: string - Associated container (for vLLM)

**TypeScript Interface:**
```typescript
interface LLMModelMetrics {
  timestamp: string;
  model_id: string;
  model_name: string;
  model_type: 'LLM' | 'Embedding' | 'Reranker';
  provider: 'vLLM' | 'LiteLLM';
  endpoint: string;
  status: 'available' | 'loading' | 'error';
  requests_per_minute: number;
  tokens_per_minute_input: number;
  tokens_per_minute_output: number;
  avg_latency_ms: number;
  error_rate_percent: number;
  model_size_bytes: number;
  quantization: string;
  version: string;
  container_name?: string;
}
```

**Relationships:**
- Many-to-one with Container Metrics (for vLLM models)
- One-to-many with Request Logs (model serves requests)
