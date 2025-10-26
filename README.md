# 🍇 Grape

> **This project is developed for the Google Cloud University Hackathon 2025.**

---

![alt text](docs/grape_cover.png)
## Overview

**Grape** is an AI-powered reasoning agent built around a **central RDF knowledge graph**.  
It aims to **break down silos between medical disciplines** by connecting symptoms, diagnoses, and treatments across heterogeneous knowledge bases.  

Unlike traditional LLM-based assistants, **Grape treats the knowledge graph as its foundation of truth**, using it for:
- Logical inference and relation verification  
- Transparent argumentation (every answer is grounded in graph data)  
- Discovering novel, cross-disciplinary connections between medical domains  

---

## Features

-  **Knowledge Graph Core:** Built on RDF/OWL for interoperability and inference  
-  **Agent Integration:** Uses reasoning to query and verify relations dynamically  
-  **Medical Insight Discovery:** Links symptoms and pathologies across specialties  
-  **Explainable AI:** Every result includes graph-backed justification  
-  **Google Cloud Integration:** Uses GCP services for storage, querying, and deployment  

---

##  Architecture

1. **Knowledge Layer (RDF Graph)** — Medical ontologies and datasets integrated into a unified graph  
2. **Inference Engine** — SPARQL queries + logical reasoning (e.g., via OWL reasoners or custom rules)  
3. **Agent Interface** — LLM interface (text or chat) connected to the reasoning backend  
4. **Cloud Infrastructure** — Hosted on Google Cloud (BigQuery + Cloud Run + Vertex AI optional)  

---

##  Example Use Case

> *A patient presents with chronic fatigue and joint pain.*  
> Grape queries its graph, finds links between rheumatology and endocrinology, and suggests potential autoimmune pathways or thyroid correlations — all **backed by verifiable graph relations**.

---

##  Tech Stack

- **Language:** Python / TypeScript  
- **Knowledge Graph:** RDF, OWL, SPARQL  
- **Storage:** Google Cloud Storage / Firestore  
- **Agent Framework:** LangChain / Semantic Kernel / custom LLM logic  
- **Infra:** Google Cloud Run + Vertex AI  

---

##  Setup

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Make (optional, but recommended)

### Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/grape.git
   cd grape
   ```

2. Configure environment variables:
   ```bash
   cp apps/backend/.env.example apps/backend/.env
   # Edit apps/backend/.env with your credentials
   ```

3. Start all services:
   ```bash
   make up
   # or
   docker-compose up -d
   ```

4. Access the applications:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Development Commands

```bash
make help        # Show all available commands
make up          # Start services
make down        # Stop services
make logs        # View logs
make test-web    # Run frontend tests
make test-api    # Run backend tests
make lint-web    # Lint frontend
make lint-api    # Lint backend
```

### Project Structure

```
grape/
├── apps/
│   ├── web/              # Next.js frontend
│   └── backend/          # FastAPI backend
├── docker-compose.yml    # Service orchestration
└── Makefile             # Development commands
```

## Legacy Setup

```bash
git clone https://github.com/<your-repo>/grape.git
cd grape
pip install -r requirements.txt
