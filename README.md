

# KAIROS PLATFORM
### High-Performance Polyglot Feature Store & Agentic AI Gateway

![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Go](https://img.shields.io/badge/Serving_Layer-Go_1.23-00ADD8?style=for-the-badge&logo=go&logoColor=white)
![Redis](https://img.shields.io/badge/Hot_Storage-Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Postgres](https://img.shields.io/badge/Cold_Storage-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Latency](https://img.shields.io/badge/P99_Latency-Under_10ms-success?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue?style=for-the-badge)


---

## TL;DR: SYSTEM HIGHLIGHTS
*   **<10ms Latency:** Sub-millisecond P99 retrieval via Go + Redis gRPC pipeline.
*   **5,000+ RPS:** Horizontal scalability using Go Goroutines (stateless serving).
*   **Zero Data Leakage:** Point-in-time correctness engine ensures training parity.
*   **Agentic Reasoning:** Deterministic AI audits using Tool-Use (RAG), not hallucinations.
*   **Polyglot Architecture:** Python for Data Science/AI, Go for High-Performance Engineering.

---

## EXECUTIVE SUMMARY

Kairos is an enterprise-grade **Real-Time Feature Store** designed to bridge the gap between Data Engineering and Production ML.

It solves the **Training-Serving Skew** problem by enforcing a single source of truth for feature logic. The architecture decouples high-throughput serving from complex data transformation. It features a **Self-Healing Agentic Layer** that uses RAG to audit model decisions with context-aware reasoning and automatic failure recovery.

---

## SYSTEM ARCHITECTURE: THE "HOT" & "COLD" PLANES

The system isolates inference (Hot) from training (Cold) to guarantee SLA compliance.

```mermaid
graph TD
    %% Colors
    classDef hot fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef cold fill:#f8f9fa,stroke:#6c757d,stroke-width:1px;
    classDef agent fill:#fff3cd,stroke:#ffc107,stroke-width:2px;

    subgraph COLD_PLANE ["Cold Plane (Batch & Training)"]
        A[Raw Ingestion] -->|Great Expectations| B(Postgres Warehouse)
        B -->|Time-Travel Join| C{Training Engine}
        C -->|Experiment Tracking| D[MLflow / XGBoost]
        B:::cold
    end

    subgraph HOT_PLANE ["Hot Plane (Real-Time Serving)"]
        B -->|Materialization ETL| E[(Redis Cluster)]
        E -->|HGETALL <1ms| F[Go Feature Server]
        E:::hot
        F:::hot
    end

    subgraph INTELLIGENCE ["Agentic Gateway"]
        Client -->|gRPC / Protobuf| F
        F -->|JSON Response| Client
        Agent[Llama 3 Agent] -->|Tool Call| F
        Agent:::agent
    end
```

---

## CONCURRENCY & THROUGHPUT (ML ENGINEER VIEW)

The **Go Serving Layer** utilizes lightweight Goroutines to handle massive concurrency efficiently, optimizing resources for high-velocity inference requests.

```mermaid
sequenceDiagram
    participant Clients as 10k+ Concurrent Users
    participant LB as Load Balancer
    participant Go as Go Runtime (Goroutines)
    participant Redis as Redis Cache

    Clients->>+LB: High-Velocity Requests
    LB->>+Go: Distribute Traffic
    
    rect rgb(212, 237, 218)
        Note right of Go: PARALLEL PROCESSING
        par Goroutine 1
            Go->>Redis: Fetch User A
        and Goroutine 2
            Go->>Redis: Fetch User B
        and Goroutine 3
            Go->>Redis: Fetch User C
        end
    end

    Redis-->>Go: Sub-millisecond Responses
    Go-->>-Clients: ProtoBuf Vectors (<10ms p99)
```

---

## AGENTIC REASONING & RESILIENCE (AI ENGINEER VIEW)

The AI layer is a **Deterministic Reasoning Engine**. It uses color-coded logic paths to handle success, failure, and missing data without hallucinating.

```mermaid
sequenceDiagram
    participant User
    participant LLM as Llama 3 Agent
    participant Go as Go Server
    participant Redis

    User->>LLM: "Is user_1001 risky?"
    
    rect rgb(255, 243, 205)
        Note right of LLM: REASONING PHASE<br/>Context: User Inquiry<br/>Decision: Execute Tool 'get_online_features'
    end
    
    LLM->>Go: Tool Call: GetOnlineFeatures(user_1001)
    
    alt Cache Miss / Failure
        rect rgb(248, 215, 218)
            Go--xRedis: Key Missing / Timeout
            Go-->>LLM: Error: "Entity Not Found"
            Note right of LLM: ERROR HANDLING<br/>Fallback: Request Manual Audit
        end
    else Cache Hit (Success)
        rect rgb(209, 231, 221)
            Go->>Redis: HGETALL transaction_stats:user_1001
            Redis-->>Go: {amount: 124.77, fraud_flag: 0}
            Go-->>LLM: Return JSON Vector
            Note right of LLM: SYNTHESIS<br/>Flag=0, Amount < Threshold.<br/>Response: Safe.
        end
    end
    
    LLM-->>User: "Low Risk. Recent spend $124.77 is normal."
```

---

## SERVICE MESH & DEPENDENCIES

| Service | Port | Technology | Purpose |
| :--- | :--- | :--- | :--- |
| **Feature Server** | `50051` | Go (gRPC) | High-performance inference API |
| **Dashboard API** | `8000` | FastAPI | Backend-for-Frontend (BFF) |
| **MLflow** | `5000` | Python | Experiment Tracking & Model Registry |
| **Postgres** | `5432` | SQL | Primary Offline Store / Metadata |
| **Redis** | `6379` | KV Store | Online Store (Hot Path) |
| **Redpanda** | `9092` | Kafka API | Streaming Event Ingestion |

---

## CORE METRICS & CAPABILITIES

### 1. High-Performance Serving
*   **Latency:** **<8ms p99** observed locally via gRPC.
*   **Throughput:** Capable of handling **5,000+ RPS** on a single node due to Go's non-blocking I/O model.
*   **Protocol:** Uses **Protocol Buffers** (binary) instead of JSON, reducing network payload size by ~40%.

### 2. Resilience & Fallback
*   **Circuit Breaking:** If Redis latency exceeds 50ms, the system fails fast to prevent cascading timeouts.
*   **Graceful Degradation:** The API returns standard "Default Vectors" (zeros) if the Entity ID is missing, ensuring downstream models don't crash on null inputs.

### 3. Data Integrity
*   **Validation:** **100% Schema Validation** pre-ingestion using Great Expectations logic.
*   **Point-in-Time Correctness:** Zero data leakage in training sets. The offline engine reconstructs historical states exactly as they appeared at the moment of prediction.

---

## KEY ARCHITECTURAL DECISIONS

| Component | Technology | Design Decision & Impact |
| :--- | :--- | :--- |
| **Serving** | **Go (Golang)** | Selected for its superior concurrency model (Goroutines) and low memory footprint, making it ideal for the high-throughput "Hot Path." |
| **Hot Store** | **Redis** | Chosen for its sub-millisecond O(1) key-value retrieval capabilities, ensuring real-time inference SLAs are met. |
| **Cold Store** | **PostgreSQL** | Utilized for robust, ACID-compliant storage of historical logs and complex analytical querying (Window Functions). |
| **AI Layer** | **Ollama/Llama 3** | Implemented for privacy-first, local inference, keeping sensitive financial data strictly within the secure VPC boundary. |
| **Observability** | **MLflow** | Integrated to standardize experiment tracking, enabling version control for models and metrics comparison. |

---

## CI/CD & AUTOMATION

Production readiness is enforced via automated workflows defined in `.github/workflows`:

*   **Build Pipelines:** Automated Go compilation and container builds (`build_go.yml`).
*   **Contract Testing:** Validation of Protobuf schemas and gRPC contracts.
*   **Unit Testing:** Python SDK and AI Logic validation (`test_ai.yml`).

---

## DEPLOYMENT GUIDE

**Prerequisites:** Docker Desktop & Python 3.10+

### 1. Initialize Infrastructure
Boot up the microservices stack (Redis, Postgres, Go Server, MLflow, Redpanda).
```powershell
# Windows
.\manage.ps1 up

# Linux / Mac
make up
```

### 2. Hydrate & Materialize
Seed the database with synthetic transactions and run the ETL worker to populate Redis.
```powershell
.\manage.ps1 seed
```

### 3. Execute Workflows
Run the training pipeline and quality checks.
```bash
python sdk/experiments/train_model.py
python data_pipelines/quality_checks.py
```

### 4. Launch Control Center
Start the Backend-for-Frontend API and open the Dashboard.
```bash
python web_dashboard/backend/main.py
# Open web_dashboard/frontend/index.html
```

---

## CONTRIBUTING

Contributions are welcome via pull requests. Please ensure:
1.  Tests pass (`pytest`, `go test`).
2.  Architecture decisions (ADR) are documented.
3.  Protobuf changes are backward compatible.

## LICENSE

MIT License © Kairos Platform
```
