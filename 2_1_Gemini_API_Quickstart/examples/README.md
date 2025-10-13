# Gemini API Examples

Practical code examples using the `google-genai` Python SDK with Vertex AI.

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Authenticate
gcloud auth application-default login

# Set environment variables (REQUIRED)
export GOOGLE_CLOUD_PROJECT="your-project-id"  # Replace with your GCP project ID
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_LOCATION="us-central1"

# Or use your current gcloud project
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_LOCATION="us-central1"
```

**IMPORTANT:** Most examples use environment variables for configuration. Make sure to set these before running the examples.

## Examples

### 1. Hello World
Basic text generation with Gemini.

```bash
python 1_hello_world.py
```

### 2. Streaming Response
Get real-time streaming output as the model generates.

```bash
python 2_streaming_response.py
```

### 3. Chat Conversation
Multi-turn conversation with context retention.

```bash
python 3_chat_conversation.py
```

### 4. Image Analysis
Analyze images with Gemini's multimodal capabilities.

```bash
# Edit the file to add your image path
python 4_image_analysis.py
```

### 5. Function Calling
Let Gemini call Python functions to get information.

```bash
python 5_function_calling.py
```

### 6. Structured Output (NEW!)
Get guaranteed JSON responses with Pydantic models.

```bash
python 6_structured_output.py
```

Examples include:
- Contact information extraction
- Product review analysis
- Recipe extraction
- Meeting minutes generation
- Invoice data extraction

### 7. PDF Analysis
Extract information from PDF documents.

```bash
# Edit the file to add your PDF path or GCS URI
python 7_pdf_analysis.py
```

### 8. FastAPI Chat API
Production-ready chat API that can be deployed to Cloud Run.

```bash
# Run locally
python 8_fastapi_chat_api.py

# Test it
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user123",
    "message": "Hello, how are you?"
  }'
```

### 9. Image Generation (NEW!)
Generate images from text prompts using Gemini's image generation capabilities.

```bash
python 9_image_generation.py
```

Features:
- Text-to-image generation
- Save generated images as PNG files
- Support for detailed prompts

### 10. Image Editing (NEW!)
Edit existing images using text prompts.

```bash
# Edit the file to add your image path
python 10_image_editing.py
```

**Deploy to Cloud Run:**

```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY 8_fastapi_chat_api.py .
CMD python 8_fastapi_chat_api.py
EOF

# Deploy
gcloud run deploy gemini-chat-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

## Common Patterns

### Simple Generation
```python
from google import genai

client = genai.Client(
    vertexai=True,
    project="your-project-id",
    location="us-central1"
)

response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="Your prompt here"
)
print(response.text)
```

### With Configuration
```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="Write something creative",
    config=types.GenerateContentConfig(
        temperature=0.9,
        top_p=0.95,
        max_output_tokens=1024,
    )
)
```

### Structured Output with Pydantic
```python
from google.genai import types
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    email: str

response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="Extract person info: John Doe, 30, john@example.com",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=Person
    )
)

person = Person.model_validate_json(response.text)
```

### Error Handling
```python
from google.api_core import exceptions

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="Hello"
    )
    print(response.text)
except exceptions.ResourceExhausted:
    print("Rate limit hit, wait a moment")
except exceptions.InvalidArgument as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## Next Steps

- Deploy the FastAPI example to Cloud Run
- Build a custom application using these patterns
- See the main [Gemini API Quickstart](../README.md) for more details
