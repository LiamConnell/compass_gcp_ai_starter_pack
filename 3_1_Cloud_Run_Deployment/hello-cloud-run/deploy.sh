#!/bin/bash

# Deploy to Cloud Run
# Make sure you've set your project: gcloud config set project YOUR_PROJECT_ID

SERVICE_NAME="hello-cloud-run"
REGION="us-central1"

echo "Deploying $SERVICE_NAME to Cloud Run in $REGION..."

gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --platform managed

echo ""
echo "Deployment complete!"
echo "Get your service URL with:"
echo "  gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)'"
