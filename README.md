# GCP AI Starter Pack

A fast-track guide to building and deploying AI applications on Google Cloud Platform. Get from zero to deployed in under 30 minutes.

## What's This?

This starter pack helps you quickly get productive with GCP's AI services, especially if you're coming from AWS or are new to cloud platforms. We focus on:

- **Fast onboarding** - Clear, concise guides without unnecessary detail
- **AI-first** - Gemini API, Vertex AI, and the Agent Development Kit
- **Practical deployment** - Real code examples and working applications
- **AWS translation** - Concept mappings for AWS developers

## Quick Start

**Prerequisites:** Google Cloud account with billing enabled. [Get started here](./0_Prerequisites/README.md).

### 1. Set Up Your Environment (5 min)

```bash
# Install gcloud CLI
# See: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud auth application-default login

# Create a project
gcloud projects create my-ai-project --name="My AI Project"
gcloud config set project my-ai-project

# Enable required APIs
gcloud services enable \
  aiplatform.googleapis.com \
  run.googleapis.com \
  storage.googleapis.com
```

### 2. Make Your First AI API Call (5 min)

```python
# Install the SDK
pip install google-genai

# Set environment variables
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT="my-ai-project"
export GOOGLE_CLOUD_LOCATION="us-central1"

# Run your first call
from google import genai

client = genai.Client(
    vertexai=True,
    project="my-ai-project",
    location="us-central1"
)

response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="Explain quantum computing in one sentence"
)
print(response.text)
```

### 3. Deploy to Cloud Run (5 min)

```bash
# Clone a starter template
git clone https://github.com/your-repo/hello-cloud-run
cd hello-cloud-run

# Deploy with one command
gcloud run deploy my-app \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

**You're live!** Cloud Run gives you a public HTTPS URL.

## Learning Path

### Phase 1: Foundations

Start here if you're new to GCP or need to understand core concepts.

1. **[Prerequisites](./0_Prerequisites/README.md)** - Account setup and billing
2. **[Account & Project Setup](./1_1_Account_and_Project_Setup/README.md)** - Create and configure your project
3. **[Authentication & Permissions](./1_2_Authentication_and_Permissions/README.md)** - IAM and service accounts

### Phase 2: AI Services

Learn to use Gemini and build AI agents.

4. **[Gemini API Quickstart](./2_1_Gemini_API_Quickstart/README.md)** - Text generation, vision, function calling
   - 8 code examples including structured output with Pydantic
   - Streaming, chat, image analysis, PDF processing
5. **[Google ADK Quickstart](./2_2_Google_ADK_Quickstart/README.md)** - Build production-ready AI agents
   - Multi-agent systems, tool integration, MCP support
   - 5 complete agent examples

### Phase 3: Deployment & Storage

Deploy your applications and manage data.

6. **[Cloud Run Deployment](./3_1_Cloud_Run_Deployment/README.md)** - Containerized serverless deployment
   - Complete hello-world example included
7. **[Cloud Storage](./3_2_Cloud_Storage/README.md)** - Object storage for files, images, and data

## Key Resources

### Documentation
- [Gemini API Examples](./2_1_Gemini_API_Quickstart/examples/) - 8 working code samples
- [ADK Agent Examples](./2_2_Google_ADK_Quickstart/examples/) - 5 complete agent implementations
- [Cloud Run Hello World](./3_1_Cloud_Run_Deployment/hello-cloud-run/) - Ready-to-deploy application

### For AWS Developers
- [GCP-AWS Concept Comparison Map](./GCP_AWS_Concept_Comparison_Map.md) - Service equivalents and translations

### Common Patterns

**Structured Output with Pydantic:**
```python
from google import genai
from google.genai import types
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    email: str

response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="Extract: John Doe, 30, john@example.com",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=Person
    )
)
person = Person.model_validate_json(response.text)
```

**Building an Agent:**
```python
from google.adk.agents.llm_agent import Agent

def get_weather(city: str) -> dict:
    """Gets current weather for a city."""
    return {"temp": "72F", "conditions": "Sunny"}

agent = Agent(
    model='gemini-2.5-flash',
    name='weather_assistant',
    instruction="Help users check the weather.",
    tools=[get_weather]
)
```

**Deploy to Cloud Run:**
```bash
# From your project directory with a Dockerfile
gcloud run deploy my-service \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

## What's Included

### Working Code Examples
- **8 Gemini API examples** - Hello world, streaming, chat, images, PDFs, function calling, structured output, FastAPI
- **5 ADK agent examples** - Simple agent, multi-tool, customer support, multi-agent system, Cloud Storage integration
- **1 deployment example** - Complete Cloud Run application with Dockerfile and deployment scripts

### Guides & References
- Prerequisites and account setup
- Authentication patterns for local and production
- Gemini API comprehensive quickstart
- Google ADK (Agent Development Kit) guide
- Cloud Run deployment tutorial
- Cloud Storage object storage guide
- AWS-to-GCP concept mapping

## Project Structure

```
compass_gcp_ai_starter_pack/
├── 0_Prerequisites/              # Account and billing setup
├── 1_1_Account_and_Project_Setup/  # Project creation
├── 1_2_Authentication_and_Permissions/  # IAM and auth
├── 2_1_Gemini_API_Quickstart/    # Gemini API guide
│   └── examples/                 # 8 working code samples
├── 2_2_Google_ADK_Quickstart/    # Agent Development Kit
│   └── examples/                 # 5 agent examples
├── 3_1_Cloud_Run_Deployment/     # Serverless deployment
│   └── hello-cloud-run/          # Complete example app
├── 3_2_Cloud_Storage/            # Object storage guide
└── GCP_AWS_Concept_Comparison_Map.md  # AWS translations
```

## Troubleshooting

### Authentication Issues
```bash
# Re-authenticate
gcloud auth login
gcloud auth application-default login

# Verify your project
gcloud config get-value project
```

### API Not Enabled
```bash
# Enable a specific API
gcloud services enable aiplatform.googleapis.com

# List enabled services
gcloud services list --enabled
```

### Permission Denied
Check your IAM roles - you need at least:
- `Vertex AI User` for AI services
- `Cloud Run Developer` for deployments
- `Storage Object Admin` for Cloud Storage

See [Authentication & Permissions](./1_2_Authentication_and_Permissions/README.md) for details.

## Need Help?

- **Check the guides** - Each section has troubleshooting tips
- **Review examples** - All code samples are tested and working
- **GCP Documentation** - [cloud.google.com/docs](https://cloud.google.com/docs)
- **Stack Overflow** - Tag questions with `google-cloud-platform`

## License

This starter pack is provided as-is for educational purposes.

## Next Steps

1. ✅ Complete [Prerequisites](./0_Prerequisites/README.md)
2. ✅ Run through [Gemini API Quickstart](./2_1_Gemini_API_Quickstart/README.md)
3. ✅ Try the [ADK examples](./2_2_Google_ADK_Quickstart/examples/)
4. ✅ Deploy your first app with [Cloud Run](./3_1_Cloud_Run_Deployment/README.md)
5. 🚀 Build something amazing!

---

**Ready to get started?** Begin with [Prerequisites](./0_Prerequisites/README.md) or jump straight to [Gemini API Quickstart](./2_1_Gemini_API_Quickstart/README.md) if you already have a GCP account.
