from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_video(transcript: str) -> str:
    prompt = f"""
    You are an expert summarizer.

    Summarize the following YouTube video transcript in clear English.
    Use bullet points and keep it concise.

    Transcript:
    {transcript}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You summarize videos accurately."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
