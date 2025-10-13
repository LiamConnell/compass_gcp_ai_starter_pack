"""
Simple Hello World with Gemini via Vertex AI
"""

import os
from google import genai

# Initialize client with Vertex AI
client = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
)

# Generate content
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="Explain quantum computing in one sentence"
)

print(response.text)
