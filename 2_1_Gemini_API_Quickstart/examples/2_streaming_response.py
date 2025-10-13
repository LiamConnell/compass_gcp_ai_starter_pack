"""
Streaming response example - get results as they're generated
"""

from google import genai
import os

# Initialize client
client = genai.Client(
    vertexai=True,
    project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    location="us-central1"
)

# Generate content with streaming
print("Generating story...\n")

for chunk in client.models.generate_content_stream(
    model="gemini-2.0-flash-exp",
    contents="Write a short story about a robot learning to paint"
):
    print(chunk.text, end='', flush=True)

print("\n\nDone!")
