# Hello Cloud Run

A minimal example app to deploy to Google Cloud Run.

## Files

- `main.py` - FastAPI application
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container definition
- `deploy.sh` - Deploy to Cloud Run

## Quick Start

### Deploy to Cloud Run

```bash
# Make sure your project is set
gcloud config set project YOUR_PROJECT_ID

# Deploy
./deploy.sh

# Or manually:
gcloud run deploy hello-cloud-run \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

### Test the Deployed App

```bash
# Get the URL
URL=$(gcloud run services describe hello-cloud-run \
  --region us-central1 \
  --format='value(status.url)')

# Test it
curl $URL
```

## Endpoints

- `GET /` - Returns a hello message
- `GET /health` - Health check endpoint

## Optional: Test Locally

Want to test before deploying? Run:

```bash
./test-local.sh
```

Or manually:
```bash
docker build -t hello-cloud-run .
docker run -p 8080:8080 -e PORT=8080 hello-cloud-run
```

Visit http://localhost:8080

## What's Next?

- Add environment variables
- Connect to Cloud Storage
- Add Gemini API integration
- See [Gemini API Quickstart](../../2_1_Gemini_API_Quickstart/README.md)
