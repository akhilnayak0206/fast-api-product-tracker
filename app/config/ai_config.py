from openai import OpenAI
from .settings import settings

# Initialize OpenAI client
ai_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=settings.api_kaiey
)