"""
Multi-turn chat conversation with Gemini
"""

from google import genai
import os

# Initialize client
client = genai.Client(
    vertexai=True,
    project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    location="us-central1"
)

# Start a chat session
chat = client.chats.create(model="gemini-2.0-flash-exp")

# Conversation
messages = [
    "Hi! I'm building a web application.",
    "I want to use Python. What framework should I choose?",
    "Great! How do I deploy it to GCP?",
    "What about databases?"
]

print("=== Chat Conversation ===\n")

for user_message in messages:
    print(f"You: {user_message}")

    response = chat.send_message(user_message)
    print(f"Gemini: {response.text}\n")

# View conversation history (if available)
print("\n=== Conversation Complete ===")
print(f"Total messages sent: {len(messages)}")
