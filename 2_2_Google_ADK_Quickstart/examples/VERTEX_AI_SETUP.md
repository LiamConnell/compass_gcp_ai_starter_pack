# Vertex AI Configuration

All examples have been configured to use Vertex AI instead of API keys.

## Configuration

Each example directory now contains a `.env` file with:

```bash
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

## Setup Steps

1. **Authenticate with GCP:**
   ```bash
   gcloud auth application-default login
   ```

2. **Set your project ID:**
   Edit the `.env` file in each example directory and replace `your-project-id` with your actual GCP project ID.
   
   Or set it globally:
   ```bash
   export GOOGLE_CLOUD_PROJECT="your-actual-project-id"
   ```

3. **Verify Vertex AI API is enabled:**
   ```bash
   gcloud services enable aiplatform.googleapis.com --project=your-project-id
   ```

4. **Run any example:**
   ```bash
   cd 1_simple_agent
   adk run .
   ```

## How It Works

- `GOOGLE_GENAI_USE_VERTEXAI=TRUE` tells the ADK to use Vertex AI instead of the Gemini API
- `GOOGLE_CLOUD_PROJECT` specifies which GCP project to use
- `GOOGLE_CLOUD_LOCATION` sets the region for Vertex AI (default: us-central1)

## Benefits of Vertex AI

- Better integration with GCP services
- Enterprise-grade security and compliance
- No need to manage API keys
- Uses your GCP credentials automatically
- Access to private models and customizations

## Troubleshooting

**Authentication errors:**
- Run `gcloud auth application-default login`
- Ensure your account has Vertex AI User role

**Project not found:**
- Verify GOOGLE_CLOUD_PROJECT is set correctly
- Check that Vertex AI API is enabled

**Permission denied:**
- Add Vertex AI User role: `gcloud projects add-iam-policy-binding PROJECT_ID --member=user:EMAIL --role=roles/aiplatform.user`
