# Architecture Diagrams

## System Architecture (Mermaid)

```mermaid
graph TB
    subgraph UI["User Interface (Streamlit)"]
        UPLOAD["📤 PDF Upload"]
        CHAT["💬 Chat Interface"]
        CONFIG["⚙️ Configuration"]
    end
    
    subgraph INGEST["Document Ingestion Pipeline"]
        LOADER["PDFLoader<br/>PyPDF2"]
        CHUNKER["SemanticChunker<br/>Paragraph-based"]
        EMBEDDER["EmbeddingGenerator<br/>Gemini embedding-001"]
    end
    
    subgraph STORAGE["Persistent Storage Layer"]
        FAISS_PDF["FAISS Index<br/>/data/vectors/"]
        META_PDF["Metadata<br/>Pickle"]
        FAISS_MEM["Memory Index<br/>/data/memory/"]
        CONV_JSON["Conversations<br/>JSON"]
    end
    
    subgraph QUERY["Query Processing Pipeline"]
        EMB_QUERY["Embed Query<br/>Gemini"]
        RETRIEVER["Unified Retriever<br/>PDF + Memory"]
        FILTER["Similarity Filter<br/>Threshold"]
        GUARDRAILS["Hallucination Guard<br/>Confidence Check"]
    end
    
    subgraph GENERATION["Response Generation"]
        PROMPT["Prompt Engineer<br/>Grounding Rules"]
        LLM["GROQ Generator<br/>Llama-3 70B"]
        MEMORY_ADD["Add to Memory<br/>Timestamped"]
    end
    
    subgraph OUTPUT["Output & Persistence"]
        RESPONSE["Display Response"]
        STORE_TURN["Store Turn"]
        STORE_VECTOR["Store Vector"]
    end
    
    UPLOAD -->|PDF File| LOADER
    LOADER -->|Text| CHUNKER
    CHUNKER -->|Chunks| EMBEDDER
    EMBEDDER -->|Vectors| FAISS_PDF
    EMBEDDER -->|Metadata| META_PDF
    
    CHAT -->|Query| EMB_QUERY
    EMB_QUERY -->|Query Vector| RETRIEVER
    RETRIEVER -->|Search| FAISS_PDF
    RETRIEVER -->|Search| FAISS_MEM
    RETRIEVER -->|Results| FILTER
    FILTER -->|Filtered Context| GUARDRAILS
    GUARDRAILS -->|Validated Context| PROMPT
    PROMPT -->|Grounded Prompt| LLM
    LLM -->|Response| MEMORY_ADD
    MEMORY_ADD -->|JSON| CONV_JSON
    MEMORY_ADD -->|Vector| FAISS_MEM
    MEMORY_ADD -->|Response| RESPONSE
    
    CONFIG -->|Threshold| GUARDRAILS
    CONFIG -->|Model Params| LLM
    
    style UI fill:#e1f5ff
    style INGEST fill:#fff3e0
    style STORAGE fill:#f3e5f5
    style QUERY fill:#e8f5e9
    style GENERATION fill:#fce4ec
    style OUTPUT fill:#f0f4c3
```

## Component Interaction Diagram

```mermaid
graph LR
    USER["👤 User"] -->|Query| APP["App.py"]
    
    APP -->|PDF| LOADER["loader.py"]
    LOADER -->|Text| CHUNKER["chunker.py"]
    CHUNKER -->|Chunks| EMBEDDER["embeddings.py"]
    EMBEDDER -->|Vectors| VECTORSTORE["vectorstore.py"]
    VECTORSTORE -->|Index| DISK1["💾 FAISS\nDisk Store"]
    
    APP -->|Query| RETRIEVER["retriever.py"]
    RETRIEVER -->|Search| VECTORSTORE
    RETRIEVER -->|Context| GUARDRAILS["guardrails.py"]
    GUARDRAILS -->|Safe Prompt| GENERATOR["generator.py"]
    GENERATOR -->|Response| MEMORY["memory.py"]
    MEMORY -->|JSON| DISK2["💾 Memory\nDisk Store"]
    
    GENERATOR -->|Tokens| GROQ["🤖 GROQ API"]
    EMBEDDER -->|Tokens| GEMINI["🤖 Gemini API"]
    
    MEMORY -->|Response| APP
    APP -->|Display| USER
    
    style USER fill:#fff9c4
    style APP fill:#e1f5ff
    style LOADER fill:#fff3e0
    style CHUNKER fill:#fff3e0
    style EMBEDDER fill:#fff3e0
    style VECTORSTORE fill:#f3e5f5
    style DISK1 fill:#e0e0e0
    style DISK2 fill:#e0e0e0
    style RETRIEVER fill:#e8f5e9
    style GUARDRAILS fill:#fce4ec
    style GENERATOR fill:#fce4ec
    style MEMORY fill:#f0f4c3
    style GROQ fill:#ffe0b2
    style GEMINI fill:#ffe0b2
```

## Data Flow - Document to Response

```mermaid
sequenceDiagram
    participant User
    participant Streamlit as Streamlit UI
    participant Loader as PDFLoader
    participant Chunker as SemanticChunker
    participant Embedder as EmbeddingGenerator
    participant Vectorstore as FAISSVectorStore
    participant Retriever as UnifiedRetriever
    participant Guardrails as HallucinationGuardrails
    participant LLM as GROQ
    participant Memory as ConversationMemory
    
    User->>Streamlit: Upload PDF
    Streamlit->>Loader: load_pdf()
    Loader->>Loader: Extract text
    Loader->>Chunker: chunk(text)
    Chunker->>Chunker: Split paragraphs
    Chunker->>Embedder: embed_texts()
    Embedder->>Embedder: Gemini API
    Embedder->>Vectorstore: add()
    Vectorstore->>Vectorstore: Save FAISS + pkl
    
    User->>Streamlit: Ask question
    Streamlit->>Retriever: retrieve(query)
    Retriever->>Embedder: embed_query()
    Retriever->>Vectorstore: search() [PDF + Memory]
    Vectorstore->>Retriever: Results + metadata
    Retriever->>Guardrails: check_grounding()
    Guardrails->>Guardrails: Verify confidence
    Guardrails->>Guardrails: generate_safe_prompt()
    Guardrails->>LLM: "Answer ONLY from context..."
    LLM->>LLM: GROQ inference
    LLM->>Memory: Response text
    Memory->>Memory: add_turn()
    Memory->>Memory: Save JSON + embed
    Memory->>Streamlit: Response
    Streamlit->>User: Display answer
```

## Vector Store Architecture

```mermaid
graph TB
    subgraph PDFStore["PDF Vector Store"]
        PDFI["FAISS Index<br/>Flat L2"]
        PDFM["Metadata<br/>{source, page, text}"]
        PDFD["Disk<br/>pdf_index.faiss"]
    end
    
    subgraph MemoryStore["Memory Vector Store"]
        MEMI["FAISS Index<br/>Flat L2"]
        MEMM["Metadata<br/>{timestamp, text, query}"]
        MEMD["Disk<br/>memory_index.faiss"]
    end
    
    subgraph JSONStore["Conversation Store"]
        JSON["JSON File<br/>conversations.json"]
        TURNS["[{query, response,<br/>timestamp, context}]"]
    end
    
    Embeddings["Gemini<br/>Embeddings<br/>768-D"] -->|Add Vectors| PDFI
    Embeddings -->|Add Vectors| MEMI
    
    PDFI -.->|Metadata| PDFM
    PDFM -->|Persist| PDFD
    
    MEMI -.->|Metadata| MEMM
    MEMM -->|Persist| MEMD
    
    Responses["Responses"] -->|Store| JSON
    JSON -.->|Contains| TURNS
    
    Query["Query<br/>Search"] -->|Search| PDFI
    Query -->|Search| MEMI
    
    style PDFStore fill:#fff3e0
    style MemoryStore fill:#f3e5f5
    style JSONStore fill:#e8f5e9
```

## Hallucination Guardrails Pipeline

```mermaid
graph TD
    Query["User Query"] -->|Embed| QueryVec["Query Vector"]
    QueryVec -->|Search| Retrieved["Retrieved Texts<br/>+ Similarity Scores"]
    
    Retrieved -->|Layer 1| Threshold["Check Similarity<br/>avg >= threshold?"]
    Threshold -->|False| Fallback1["Return:<br/>No Information<br/>Available"]
    Threshold -->|True| Prompt["Layer 2: Apply<br/>Grounding Prompt<br/>ONLY from context"]
    
    Prompt -->|Send| LLM["GROQ Llama-3"]
    LLM -->|Response| Detection["Layer 3: Detect<br/>No-Answer Patterns"]
    
    Detection -->|Found| Fallback2["Return:<br/>Fallback Response"]
    Detection -->|Not Found| Output["Return:<br/>Generated Response"]
    
    Output -->|Save| Memory["Store in Memory<br/>+ Timestamp"]
    Fallback1 -->|Save| Memory
    Fallback2 -->|Save| Memory
    
    Memory -->|Persist| Storage["JSON + FAISS"]
    
    style Threshold fill:#ffcdd2
    style Prompt fill:#ffcdd2
    style Detection fill:#ffcdd2
    style Fallback1 fill:#c8e6c9
    style Fallback2 fill:#c8e6c9
    style Output fill:#c8e6c9
    style Memory fill:#f0f4c3
```
