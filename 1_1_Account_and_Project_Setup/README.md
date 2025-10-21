# Account & Project Setup

## Set Up Gemini CLI 

The Gemini CLI gives you an AI assistant in your terminal that can help with GCP tasks, debugging, and infrastructure questions.

```
brew install gemini-cli
```

### Configure for Vertex AI (Optional)

```bash
# Set environment variables to use Vertex AI
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT="hackathon-2025-475415"
export GOOGLE_CLOUD_LOCATION="us-central1"

# Add to your shell profile (~/.bashrc, ~/.zshrc) to persist
echo 'export GOOGLE_GENAI_USE_VERTEXAI=TRUE' >> ~/.bashrc
echo 'export GOOGLE_CLOUD_PROJECT="hackathon-2025-475415"' >> ~/.bashrc
echo 'export GOOGLE_CLOUD_LOCATION="us-central1"' >> ~/.bashrc
```

Login with gcloud
```bash
gcloud auth application-default login
```

### Launch the CLI

```bash
# Start an interactive session
gemini

# Or run a single command
gemini "How do I deploy to Cloud Run?"
```

### Configure with Project Context

For better assistance, copy the [GEMINI.md](GEMINI.md) file that we have provided here, and fill in the variables at the top with your project information. A GEMINI.md file holds default context for the project. 

See [GEMINI.md](./GEMINI.md) for a pre-configured context file that helps Gemini act as your GCP infrastructure assistant.

### Next Steps

**Next:** [Authentication & Permissions](../1_2_Authentication_and_Permissions/README.md)
