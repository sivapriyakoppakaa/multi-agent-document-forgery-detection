import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

llm = LLM(
    model="gemini/gemini-3.5-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY")
)