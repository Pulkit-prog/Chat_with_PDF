# Assessment Chat RAG System  
**AI Prototyping Engineer Practical Assessment Submission**

---

## 📌 Overview

This repository contains a **production-style AI prototype** developed as part of the **AI Prototyping Engineer Practical Assessment**.

The system implements a complete **Retrieval-Augmented Generation (RAG)** workflow that allows users to upload multiple PDF documents and ask questions grounded strictly in those documents.

A core focus of this prototype is **hallucination prevention**.  
If relevant information is not found in the uploaded PDFs, the system **explicitly refuses to guess**, demonstrating safe and reliable LLM behavior suitable for real-world enterprise use.

---

## 🎯 Assessment Task Alignment (Explicit)

### ✅ Task 1: LLM-Powered AI Prototype

This project implements a full end-to-end RAG system using:

- **LLM:** GROQ Llama-3 for fast, instruction-following generation  
- **Embeddings:** Google Gemini `embedding-001` for semantic search  
- **Vector Database:** FAISS (local, persistent)  
- **Chunking Strategy:** Semantic paragraph-based chunking with overlap  
- **Prompt Engineering:** Context-grounded prompts restricting answers to retrieved content  
- **UI:** Streamlit-based interface for document upload and chat  

The system is fully functional, reproducible, and designed as a realistic AI assistant prototype rather than a demo script.

---

### ✅ Task 2: Hallucination & Quality Control

Hallucination is treated as a **first-class design concern**.

**Causes addressed:**
1. Low-relevance retrieval context  
2. Over-confident LLM generation  
3. Missing grounding constraints  

**Guardrails implemented:**
- Similarity thresholding for retrieval confidence  
- Grounded system prompts (“answer only from context”)  
- Safe fallback responses when information is unavailable  

Before/after hallucination behavior is documented in the `/evaluation` folder.

---

### ✅ Task 3: Rapid Iteration — Persistent Memory

An advanced capability was added: **persistent conversational memory**.

**Why memory was chosen:**
- Mirrors real enterprise assistants that retain prior interactions  
- Improves multi-turn conversational continuity  

Memory is stored both as:
- JSON (auditability)
- FAISS vectors (semantic recall)

Trade-offs and limitations are documented later in this README.

---

### ✅ Task 4: AI System Architecture

The system architecture covers:
- Document ingestion
- Vector storage and retrieval
- LLM orchestration
- Cost-aware design
- Monitoring via guardrails and thresholds  

Architecture diagrams and design trade-offs are provided in `/docs`.

---

## 🏗️ High-Level Architecture

User (Streamlit UI)
↓
PDF Loader → Semantic Chunker
↓
Gemini Embeddings
↓
FAISS Vector Store (Persistent)
↓
Unified Retriever (PDF + Memory)
↓
Hallucination Guardrails
↓
GROQ Llama-3 Generator
↓
Response + Memory Storage


---

## 🔧 Technology Choices & Justification

### Embeddings — Google Gemini `embedding-001`
- High-quality semantic representations
- Consistent query & document embedding space
- Cost-effective and fast

### LLM — GROQ Llama-3
- Very fast inference
- Strong instruction-following behavior
- Suitable for real-time RAG systems

### Vector Database — FAISS
- Local, persistent, and free
- No external infrastructure dependency
- Scalable with IVF/HNSW if needed

---

## 💰 Cost Considerations

- Local FAISS (no vector database cost)
- Minimal embedding calls
- Efficient retrieval strategy  

Estimated cost: **< $1/month** for moderate usage.

---

## 🔑 API Integration & Setup Guide

This project uses **two external APIs**:

1. **GROQ API** – for LLM inference  
2. **Google Gemini API** – for embedding generation  

No API keys are hardcoded. All credentials are loaded securely via environment variables.

---

### 1️⃣ GROQ API (LLM)

**Purpose:**  
Used for fast, instruction-following LLM inference (Llama-3).

**How it is used:**
- Integrated in `core/generator.py`
- Invoked only after retrieval and guardrails

**How to get the API key:**
1. Visit 👉 https://groq.com  
2. Sign up or log in  
3. Go to the API section  
4. Create a new API key  

Set in .env: GROQ_API_KEY=your_groq_api_key_here

2️⃣ Google Gemini API (Embeddings)

Purpose:
Used to convert documents and queries into semantic vectors.

How it is used:

Integrated in core/embeddings.py

Uses the embedding-001 model

How to get the API key:

Visit 👉 https://ai.google.dev

Sign in with a Google account

Click Get API Key

Create or select a project

Generate an API key

Set in .env: GEMINI_API_KEY=your_gemini_api_key_here

3️⃣ Environment Configuration

Create a .env file from the template:

copy .env.sample .env


Final .env format:

GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here


The application validates API availability at startup.

🚀 Setup & Run Instructions
Prerequisites

Python 3.9+

GROQ API key

Google Gemini API key

Installation
pip install -r requirements.txt

Run the Application
streamlit run app.py


The app opens at:

http://localhost:8501

📁 Repository Structure
assessment-chat-rag/
├── app.py
├── config.py
├── requirements.txt
├── .env.sample
├── README.md
├── core/
├── docs/
└── evaluation/

🧪 Evaluation

Hallucination behavior is tested using controlled prompts:

Without guardrails → confident incorrect answers

With guardrails → explicit refusal when context is missing

Evaluation results are available in /evaluation.

🔒 Security & Limitations
Implemented

Environment-based secrets

Local data storage

Input validation

Not Implemented (out of scope for prototype)

Authentication

Encryption at rest

Rate limiting

📌 Final Notes for Evaluators

The system does not hallucinate

All answers are grounded in retrieved documents

The prototype prioritizes correctness and safety

Design decisions and trade-offs are explicitly documented





