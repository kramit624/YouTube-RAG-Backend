import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def get_rag_chain(retriever):
    """
    Returns a callable function: ask(question) -> answer
    """

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=GROQ_API_KEY
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an AI assistant that answers questions ONLY using the provided context.

Rules:
- Use ONLY the context below.
- Do NOT use prior knowledge.
- If the answer is not in the context, say exactly:
  "The video does not mention this."

Context:
{context}

Question:
{question}

Answer:
"""
    )

    def ask(question: str) -> str:
        docs = retriever.invoke(question)

        if not docs:
            return "The video does not mention this."

        context = "\n\n".join(doc.page_content for doc in docs)

        response = llm.invoke(
            prompt.format(
                context=context,
                question=question
            )
        )

        return response.content.strip()

    return ask
