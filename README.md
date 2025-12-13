
# 📺 YouTube RAG Backend (FastAPI + LangChain + Redis)

A **Retrieval-Augmented Generation (RAG)** backend that allows users to:

- 🔗 Paste a YouTube video ID  
- 📝 Automatically fetch & translate subtitles to English  
- 🧠 Ask context-aware questions about the video  
- ✨ Generate concise video summaries  
- ⚡ Cache transcripts using Redis (to save API usage)

Built with **FastAPI**, **LangChain**, **Groq LLM**, **FAISS**, and **Redis**.

---

## 🚀 Features

- ✅ YouTube subtitle extraction via RapidAPI
- 🌍 Automatic translation to English (only if needed)
- 🔎 Semantic search using FAISS vector store
- 🤖 LLM-powered Q&A with strict context grounding
- 📝 One-click video summarization
- ⚡ Redis-based transcript caching
- 📡 REST API (Postman / Frontend ready)
- ☁️ Deployable on Railway / Render / Fly.io

---

## 🧠 Architecture Overview
```
Frontend (React / Postman)
        |
        v
FastAPI Backend
        |
        ├── Transcript Fetcher (RapidAPI)
        ├── Redis Cache (transcripts)
        ├── Text Chunking
        ├── Embeddings (HuggingFace)
        ├── FAISS Vector Store
        ├── Retriever
        └── Groq LLM (Q&A / Summary)
```
---

## 🗂️ Project Structure

```
ProjetcLLMS/
├── src/
│   ├── redis_client.py
│   ├── transcript.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vectorstore.py
│   ├── rag.py
│   ├── summary.py
│   └── __init__.py
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🔑 Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key
RAPIDAPI_KEY=your_rapidapi_key
REDIS_HOST=your_redis_host
REDIS_PORT=your_redis_port
REDIS_PASSWORD=your_redis_password
```

---

## ▶️ Run Backend

```
uvicorn app:app --reload
```

API Docs: http://127.0.0.1:8000/docs

---

## 🔌 API Endpoints - EXAMPLE

### Process Video
POST `/process-video`

```
{
  "video_id": "_3ezSpJw2E8"
}
```

### Ask Question
POST `/ask`

```
{
  "question": "What is LangChain?"
}
```

### Summarize Video
POST `/summarize`

---

## ☁️ Deployment

- Backend: Railway (recommended)
- Cache: Redis Cloud (Free Tier)
- Frontend: Vercel / Netlify

---

## 🧑‍💻 Author

Amit Sharma  
AI / ML Engineer – LLMs & RAG Systems
