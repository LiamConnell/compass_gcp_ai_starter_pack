from typing import Any
import google.auth
import google.auth.transport.requests
import openai

PROJECT_ID="my-project"

class VertexOpenAI(openai.OpenAI):
    def __init__(self, project_id: str, location: str = "global", **kwargs: Any) -> None:
        self.creds, _ = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        self.creds.refresh(google.auth.transport.requests.Request())
        
        super().__init__(
            base_url=f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
            api_key=self.creds.token,
            **kwargs
        )
    
    def _refresh_if_needed(self) -> None:
        if not self.creds.valid:
            self.creds.refresh(google.auth.transport.requests.Request())
            self.api_key = self.creds.token
    
    def __getattribute__(self, name: str) -> Any:
        # Refresh credentials before accessing chat, embeddings, etc.
        if name in ('chat', 'embeddings', 'completions'):
            object.__getattribute__(self, '_refresh_if_needed')()
        return super().__getattribute__(name)

# Usage with full type safety
client = VertexOpenAI(project_id=PROJECT_ID, location="us-central1")

# Type checkers know this is openai.OpenAI
response = client.chat.completions.create(
    model="google/gemini-2.5-flash",
    messages=[{"role": "user", "content": "Hello!"}]
)