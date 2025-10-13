# Development Environment Setup

## What You Need to Deploy to Cloud Run

To deploy to Cloud Run, you only need:

1. **gcloud CLI** - to deploy to Cloud Run (already installed from Prerequisites)

That's it! Cloud Run can build your container for you automatically.

## Your First Container

Let's create a simple web app and deploy it to Cloud Run.

> **Ready to try it?** A complete working example is in the [`hello-cloud-run/`](./hello-cloud-run/) directory. You can `cd` into it and run `./deploy.sh` to deploy immediately, or follow along below to understand what's happening.

### 1. Create a Simple App

**Create these files in a new directory:**

`main.py`:
```python
from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Cloud Run!"}

@app.get("/health")
def health():
    return {"status": "healthy"}
```

`requirements.txt`:
```
fastapi
uvicorn[standard]
```

`Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run sets the PORT environment variable
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 2. Deploy to Cloud Run

```bash
gcloud run deploy my-app \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

Cloud Run will:
- Build your Docker container
- Push it to Google Container Registry
- Deploy it
- Give you a live URL

Done! Your app is live on the internet.

## Important: The PORT Environment Variable

Cloud Run automatically sets a `PORT` environment variable. Your app **must** listen on this port.

**Python (FastAPI/Flask):**
```python
import os
port = int(os.environ.get("PORT", 8080))
```

**Node.js (Express):**
```javascript
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
```

**Your Dockerfile CMD should use $PORT:**
```dockerfile
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Quick Reference

### Deploy to Cloud Run:
```bash
gcloud run deploy my-app --source . --region us-central1 --allow-unauthenticated
```

### View logs:
```bash
gcloud run logs tail my-app
```

## Troubleshooting

**Docker command not found**
- Restart your terminal after installing Docker
- Make sure Docker Desktop is running (macOS/Windows)

**Permission denied (Linux)**
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

**Container fails to start on Cloud Run**
- Check logs: `gcloud run logs read my-app`
- Make sure your app listens on `$PORT`
- Verify all dependencies are in requirements.txt

**Port already in use (local testing)**
```bash
# Use a different port
docker run -p 8081:8080 -e PORT=8080 my-app
# Access at http://localhost:8081
```

## Next Steps

✅ Deployed your first app to Cloud Run
✅ Understand how containers work on Cloud Run
✅ Ready to add AI capabilities

**Next:** [Gemini API Quickstart](../2_1_Gemini_API_Quickstart/README.md)
