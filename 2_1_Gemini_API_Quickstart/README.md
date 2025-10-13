# Gemini API Quickstart

Get started with Gemini, Google's most capable AI model, in under 5 minutes.

## Two Ways to Use Gemini

### Option 1: Vertex AI (Recommended)
- ✅ **Use with GCP authentication** - no API keys to manage
- ✅ **Works automatically on Cloud Run** - already authenticated
- ✅ **More features** - tuning, evaluation, grounding
- ✅ **Enterprise-ready** - better quotas and SLAs

### Option 2: Gemini API
- Use with API key
- Faster initial setup
- Good for local prototyping

**This guide covers Option 1 (Vertex AI)** - the recommended approach for GCP.

## Your First API Call (Python)

### Install the SDK

```bash
pip install google-cloud-aiplatform
```

### Hello World

```python
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
vertexai.init(project="YOUR_PROJECT_ID", location="us-central1")

# Create a model instance
model = GenerativeModel("gemini-1.5-flash")

# Generate content
response = model.generate_content("Explain quantum computing in one sentence")
print(response.text)
```

Run it:
```bash
# Make sure you're authenticated
gcloud auth application-default login

# Run the script
python hello_gemini.py
```

That's it! No API keys needed - it uses your GCP authentication automatically.

## Your First API Call (Node.js)

### Install the SDK

```bash
npm install @google-cloud/vertexai
```

### Hello World

```javascript
const {VertexAI} = require('@google-cloud/vertexai');

// Initialize Vertex AI
const vertexAI = new VertexAI({
  project: 'YOUR_PROJECT_ID',
  location: 'us-central1'
});

const model = vertexAI.getGenerativeModel({
  model: 'gemini-1.5-flash'
});

async function run() {
  const result = await model.generateContent(
    'Explain quantum computing in one sentence'
  );
  console.log(result.response.candidates[0].content.parts[0].text);
}

run();
```

Run it:
```bash
# Make sure you're authenticated
gcloud auth application-default login

# Run the script
node hello_gemini.js
```

## Deploying on Cloud Run

When you deploy to Cloud Run, authentication is automatic! Just use the same code:

```python
import vertexai
from vertexai.generative_models import GenerativeModel
import os

# Initialize - project is auto-detected on Cloud Run
vertexai.init(
    project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    location="us-central1"
)

model = GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Hello from Cloud Run!")
```

No API keys, no credentials - it just works!

## Streaming Responses

For real-time output as the model generates:

```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="YOUR_PROJECT_ID", location="us-central1")
model = GenerativeModel("gemini-1.5-flash")

# Stream the response
response = model.generate_content(
    "Write a short story about a robot",
    stream=True
)

for chunk in response:
    print(chunk.text, end='', flush=True)
```

## Multimodal - Analyzing Images

Gemini can understand images, PDFs, audio, and video!

```python
import vertexai
from vertexai.generative_models import GenerativeModel, Part

vertexai.init(project="YOUR_PROJECT_ID", location="us-central1")
model = GenerativeModel("gemini-1.5-flash")

# Load image from Cloud Storage
image_part = Part.from_uri(
    "gs://your-bucket/photo.jpg",
    mime_type="image/jpeg"
)

# Or from local file
with open("photo.jpg", "rb") as f:
    image_data = f.read()
    image_part = Part.from_data(image_data, mime_type="image/jpeg")

# Analyze it
response = model.generate_content([
    "What's in this image? Be specific.",
    image_part
])
print(response.text)
```

## Function Calling (Tool Use)

Let Gemini call functions in your code:

```python
import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    FunctionDeclaration
)

vertexai.init(project="YOUR_PROJECT_ID", location="us-central1")

# Define a function
def get_weather(location: str) -> str:
    """Get the current weather for a location"""
    return f"Sunny and 72°F in {location}"

# Define the function schema
get_weather_func = FunctionDeclaration(
    name="get_weather",
    description="Get the current weather for a location",
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name"
            }
        },
        "required": ["location"]
    }
)

# Create tool with function
weather_tool = Tool(function_declarations=[get_weather_func])

# Create model with tools
model = GenerativeModel("gemini-1.5-flash", tools=[weather_tool])

# Start a chat
chat = model.start_chat()
response = chat.send_message("What's the weather in San Francisco?")

# Check if model wants to call a function
function_call = response.candidates[0].content.parts[0].function_call

if function_call.name == "get_weather":
    # Call the function
    result = get_weather(location=function_call.args["location"])

    # Send result back
    response = chat.send_message(
        Part.from_function_response(
            name="get_weather",
            response={"weather": result}
        )
    )
    print(response.text)
```

## Chat Conversations

Maintain context across multiple messages:

```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="YOUR_PROJECT_ID", location="us-central1")
model = GenerativeModel("gemini-1.5-flash")

# Start a chat
chat = model.start_chat()

# Send messages
response = chat.send_message("Hi, I'm building a web app")
print(response.text)

response = chat.send_message("What tech stack should I use?")
print(response.text)

response = chat.send_message("How do I deploy it on GCP?")
print(response.text)

# See full history
print(chat.history)
```

## Model Selection Guide

| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| `gemini-1.5-flash` | Quick responses, chatbots | ⚡️ Fastest | 💰 Cheapest |
| `gemini-1.5-pro` | Complex reasoning, analysis | 🐢 Slower | 💰💰 More expensive |
| `gemini-1.0-pro` | Legacy applications | ⚡️ Fast | 💰 Cheap |

**For hackathons:** Start with `gemini-1.5-flash` - it's fast and cheap!

## Configuration Options

Control model behavior with generation config:

```python
from vertexai.generative_models import GenerativeModel, GenerationConfig

model = GenerativeModel("gemini-1.5-flash")

config = GenerationConfig(
    temperature=0.7,          # Higher = more creative (0-2)
    top_p=0.95,               # Nucleus sampling
    top_k=40,                 # Top-k sampling
    max_output_tokens=1024,   # Response length limit
)

response = model.generate_content(
    "Write a creative story",
    generation_config=config
)
```

## Common Patterns

### 1. Environment Setup
```python
# config.py
import vertexai
from vertexai.generative_models import GenerativeModel
import os

def setup_gemini():
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT not set")

    vertexai.init(project=project, location="us-central1")
    return GenerativeModel("gemini-1.5-flash")

# Use it
from config import setup_gemini
model = setup_gemini()
```

### 2. Error Handling
```python
from google.api_core import exceptions

try:
    response = model.generate_content("Hello")
    print(response.text)
except exceptions.ResourceExhausted:
    print("Rate limit exceeded. Wait a moment.")
except exceptions.PermissionDenied:
    print("Authentication issue. Run: gcloud auth application-default login")
except Exception as e:
    print(f"Error: {e}")
```

### 3. Structured Output
```python
prompt = """
Extract information from this text and return as JSON:
{
  "name": "...",
  "email": "...",
  "phone": "..."
}

Text: "Contact John Doe at john@example.com or 555-1234"
"""

response = model.generate_content(prompt)
import json
data = json.loads(response.text)
print(data)
```

## Troubleshooting

**Error: "Could not automatically determine credentials"**
```bash
# Make sure you're authenticated
gcloud auth application-default login
```

**Error: "Permission denied" or "403"**
```bash
# Make sure Vertex AI API is enabled
gcloud services enable aiplatform.googleapis.com

# Check your IAM roles
gcloud projects get-iam-policy PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:$(gcloud config get-value account)"
```

**Error: "Project not set"**
- Make sure you initialize with a valid project ID
- Or set environment variable: `export GOOGLE_CLOUD_PROJECT=your-project-id`

**Import errors**
```bash
# Reinstall the SDK
pip install --upgrade google-cloud-aiplatform
```

## Alternative: Using Gemini API with API Key

If you prefer using an API key instead of GCP authentication:

```bash
pip install google-generativeai
```

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content("Hello!")
print(response.text)
```

Get an API key at [aistudio.google.com](https://aistudio.google.com/)

**Why use Vertex AI instead?**
- No API keys to manage
- Works automatically on Cloud Run
- Better integration with GCP services
- More enterprise features

## Next Steps

✅ Set up Vertex AI with GCP authentication
✅ Made first API call
✅ Explored streaming and multimodal
✅ Ready to deploy

**Next:** [Cloud Run Deployment](../3_1_Cloud_Run_Deployment/README.md) or [Cloud Storage](../3_2_Cloud_Storage/README.md)
