from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.chunking import chunk_text
from src.vectorstore import create_vectorstore
from src.rag import get_rag_chain
from src.transcript import get_transcript_with_cache
from src.summary import summarize_video
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="YouTube RAG Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
CURRENT_SESSION = {
    "video_id": None,
    "ask": None,
    "transcript": None
}


class VideoRequest(BaseModel):
    video_id: str


class QuestionRequest(BaseModel):
    question: str


@app.post("/process-video")
def process_video(req: VideoRequest):
    text = get_transcript_with_cache(req.video_id)

    if not text:
        raise HTTPException(status_code=404, detail="Transcript not available")

    chunks = chunk_text(text)
    vectorstore = create_vectorstore(chunks)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    ask = get_rag_chain(retriever)

    CURRENT_SESSION["video_id"] = req.video_id
    CURRENT_SESSION["ask"] = ask
    CURRENT_SESSION["transcript"] = text

    return {
        "message": "Video processed successfully",
        "options": ["ask", "summarize", "exit"]
    }


@app.post("/ask")
def ask_question(req: QuestionRequest):
    if CURRENT_SESSION["ask"] is None:
        raise HTTPException(status_code=400, detail="No active video")

    return {"answer": CURRENT_SESSION["ask"](req.question)}


@app.post("/summarize")
def summarize():
    if CURRENT_SESSION["transcript"] is None:
        raise HTTPException(status_code=400, detail="No active video")

    return {"summary": summarize_video(CURRENT_SESSION["transcript"])}
