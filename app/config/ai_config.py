from openai import OpenAI
from .settings import settings

# Initialize OpenAI client
ai_client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key=settings.api_kaiey
)