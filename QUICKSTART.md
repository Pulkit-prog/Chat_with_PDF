# Assessment Chat RAG - Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd assessment-chat-rag
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Create .env file from template
copy .env.sample .env

# Edit .env and add your API keys:
# GROQ_API_KEY=gsk_... (from groq.com)
# GEMINI_API_KEY=AIzaSy... (from ai.google.com)
```

### Step 3: Run Application
```bash
streamlit run app.py
```

App opens at: `http://localhost:8501`

---

## 🎯 First Steps

### 1. Upload a PDF
- Click **"Upload PDFs"** tab
- Select 1+ PDF file
- Click **"Process & Index PDFs"**
- Wait for embedding (1-2 sec per MB)

### 2. Ask a Question
- Click **"Chat"** tab
- Type your question
- Read grounded response
- View context used

### 3. Check History
- Click **"Knowledge Base"** tab
- See past conversations
- View vector statistics

---

## 🔑 API Keys

### Get GROQ API Key
1. Visit: https://groq.com
2. Sign up (free tier available)
3. Create API key
4. Copy to .env file

### Get Gemini API Key
1. Visit: https://ai.google.com
2. Click "Get API Key"
3. Create new project
4. Copy key to .env file

---

## 🛠️ Troubleshooting

### "GROQ_API_KEY not set"
→ Check .env file exists and has valid key

### "PDF loading fails"
→ Ensure PDF is valid (not corrupted/encrypted)

### "Low memory after restart"
→ Memory stored in /data/memory/ - check files exist

### "Response is too short"
→ Increase LLM_MAX_TOKENS in config.py

---

## 📊 Understanding the Interface

### Chat Tab
- **Query Input**: Type your question
- **Response**: Grounded answer from documents
- **Context Used**: Expand to see sources
- **History**: Persists across sessions

### Upload Tab
- **File Selector**: Multi-PDF upload
- **Process Button**: Triggers indexing
- **Progress**: Shows chunking status
- **Success Message**: Shows chunks indexed

### Knowledge Base Tab
- **Statistics**: Vector counts, memory size
- **Conversations**: Timestamped history
- **PDFs**: List of uploaded files
- **Recent Context**: Last 10 turns

---

## ⚙️ Configuration

### Key Settings (config.py)

| Setting | Default | What It Does |
|---------|---------|--------------|
| CHUNK_SIZE | 500 | Words per chunk |
| SIMILARITY_THRESHOLD | 0.6 | Min similarity to use context |
| TOP_K_RETRIEVAL | 5 | PDFs per query |
| MEMORY_TOP_K | 3 | Memory results per query |
| LLM_TEMPERATURE | 0.3 | Lower = more deterministic |
| LLM_MAX_TOKENS | 1024 | Max response length |

### Adjust in .env
```bash
CHUNK_SIZE=750
SIMILARITY_THRESHOLD=0.5
TOP_K_RETRIEVAL=3
```

---

## 📈 Scaling

### Current Capacity
- Flat FAISS: ~100K vectors
- Memory: ~10K conversations
- Latency: ~2.3 sec per query

### Future Phases
- **Phase 2**: IVF indexing for 100K+ vectors
- **Phase 3**: HNSW for 1M+ vectors
- **Phase 4**: Distributed deployment

See `docs/design.md` for scaling roadmap.

---

## 🔒 Data Locations

All data stored locally:
- **PDFs**: `/data/pdfs/`
- **Vector Index**: `/data/vectors/pdf_index.faiss`
- **Memory**: `/data/memory/conversations.json`

No data sent to external servers (except API calls).

---

## 📚 Documentation

- **README.md** - Complete guide (10+ sections)
- **docs/architecture.md** - System diagrams (4 Mermaid)
- **docs/design.md** - Design decisions (detailed)
- **evaluation/** - Hallucination test results

---

## ❓ Frequently Asked

**Q: Can I use different LLM?**
A: Yes, edit `core/generator.py` + `config.py`

**Q: What file formats supported?**
A: Currently PDF only. Extensible to .docx, .txt

**Q: Can I filter search by date?**
A: Not in current version. See roadmap.

**Q: How do I clear memory?**
A: Use sidebar button "Clear Memory"

**Q: Can multiple users use same instance?**
A: No, single-user. Deploy Docker for multi-user.

---

## 🚀 Next Steps

1. **Read**: README.md for detailed guide
2. **Explore**: Try with sample PDFs
3. **Configure**: Adjust settings for your use case
4. **Deploy**: Follow Docker instructions if needed
5. **Monitor**: Check /evaluation/ for test results

---

## 📞 Support

**Error in app?**
→ Check logs in terminal

**Wrong answers?**
→ Check guardrail threshold (sidebar)

**Low memory?**
→ Check /data/memory/ directory

**API failures?**
→ Verify keys in .env file

---

**Happy RAG-ing! 🚀**
