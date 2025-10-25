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

```bash
git clone https://github.com/<your-repo>/grape.git
cd grape
pip install -r requirements.txt
