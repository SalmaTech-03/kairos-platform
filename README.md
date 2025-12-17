# ⏳ Kairos: The Enterprise AI Feature Store

> **A Next-Generation Feature Platform merging High-Performance Serving (Go/Redis) with Agentic AI (LangGraph/AutoGen).**

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Tech Stack](https://img.shields.io/badge/stack-Go%20%7C%20Python%20%7C%20BigQuery%20%7C%20LangGraph-blue)]()

## 🧠 What is Kairos?
Kairos is a **Virtual Feature Store** designed to solve the two hardest problems in MLOps:
1.  **Point-in-Time Correctness:** Serving historical data for training without data leakage.
2.  **The "Black Box" Problem:** Using **Agentic AI** to allow Data Scientists to query feature lineage and statistics using natural language.

It separates the **Control Plane** (Python SDK & AI Agents) from the **Data Plane** (High-concurrency Go gRPC Server).

---

## 🏗️ Architecture & Tech Stack

### 1. ⚡ High-Performance Data Plane (Serving)
*   **Language:** Go (Golang 1.22)
*   **Protocol:** gRPC (Protobuf v3) for sub-10ms latency.
*   **Online Store:** Redis (Cluster mode compatible).
*   **Infrastructure:** Kubernetes (GKE) & Docker.

### 2. 🌊 Big Data & Offline Storage
*   **Data Warehouse:** **Google BigQuery** (Primary) & **Snowflake** (Adapter support).
*   **ETL Pipelines:** Python, Pandas, and SQL.
*   **Infrastructure as Code:** Terraform (GCP).

### 3. 🤖 Agentic AI Layer (GenAI)
*   **Orchestration:** **LangChain** & **LangGraph**.
*   **Multi-Agent System:** **Microsoft AutoGen** (SQL Writer Agent ↔ Critic Agent).
*   **NLP Core:** **BERT** (Embeddings) & **spaCy** (NER).
*   **LLM:** OpenAI GPT-4o / Ollama (Local Llama 3).

---

## 📂 Project Structure

| Directory | Purpose |
| :--- | :--- |
| `ai_agents/` | **GenAI Layer:** AutoGen swarms, LangGraph workflows, and BERT embeddings. |
| `api/` | **The Contract:** gRPC Protobuf definitions (`.proto`) and OpenAPI specs. |
| `cloud_infra/` | **IaC:** Terraform scripts for GCP BigQuery and GKE. |
| `data_pipelines/` | **Data Engineering:** Ingestion scripts for BigQuery/Snowflake. |
| `sdk/` | **Python Client:** Data Scientist-facing SDK (`pip install kairos`). |
| `services/` | **Microservices:** The high-performance Go Feature Server. |

## 🚀 Getting Started

### Prerequisites
*   Docker & Docker Compose
*   Python 3.10+
*   Go 1.22+

### 1. Start Infrastructure
```bash
make up
# Starts Redis and Postgres (Metadata)