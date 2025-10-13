"""
FastAPI chat API with Gemini
Deploy this to Cloud Run for a production chat endpoint
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
import os

# Initialize FastAPI
app = FastAPI(title="Gemini Chat API")

# Initialize Gemini client
client = genai.Client(
    vertexai=True,
    project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    location="us-central1"
)

# Store chat sessions in memory (in production, use a database)
chat_sessions = {}


class ChatMessage(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str


@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Gemini Chat API",
        "version": "1.0"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatMessage):
    """
    Send a message and get a response

    Args:
        session_id: Unique identifier for the conversation
        message: User's message

    Returns:
        Response from Gemini
    """
    try:
        # Get or create chat session
        if request.session_id not in chat_sessions:
            chat_sessions[request.session_id] = client.chats.create(
                model="gemini-2.0-flash-exp"
            )

        chat = chat_sessions[request.session_id]

        # Send message
        response = chat.send_message(request.message)

        return ChatResponse(
            session_id=request.session_id,
            response=response.text
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/chat/{session_id}")
def delete_session(session_id: str):
    """Delete a chat session"""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return {"status": "deleted", "session_id": session_id}
    return {"status": "not_found", "session_id": session_id}


@app.get("/sessions")
def list_sessions():
    """List active chat sessions"""
    return {
        "active_sessions": list(chat_sessions.keys()),
        "count": len(chat_sessions)
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
