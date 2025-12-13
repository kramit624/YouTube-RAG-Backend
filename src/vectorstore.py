from langchain_community.vectorstores import FAISS
from src.embeddings import get_embeddings


def create_vectorstore(chunks: list[str]):
    """
    Create FAISS vector store from text chunks.
    """
    embeddings = get_embeddings()
    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore
