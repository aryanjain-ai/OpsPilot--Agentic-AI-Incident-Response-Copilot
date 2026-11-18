"""Legacy smoke check. Real automated tests live under tests/."""
from src.config import get_settings

settings = get_settings()
print("Configuration loaded successfully")
print("OpenAI model:", settings.openai_model)
print("Embedding model:", settings.embedding_model)
print("Embedding dimension:", settings.embedding_dimension)
print("OpenAI key configured:", bool(settings.openai_api_key))
print("Pinecone key configured:", bool(settings.pinecone_api_key))
print("Tavily key configured:", bool(settings.tavily_api_key))
