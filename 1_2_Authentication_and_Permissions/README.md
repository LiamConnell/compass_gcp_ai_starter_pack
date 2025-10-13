# Authentication & Permissions

## The Two Types of Authentication

### 1. User Authentication (You)
For development work on your local machine.

```bash
# Login with your Google account
gcloud auth login

# Set up Application Default Credentials for local development
gcloud auth application-default login
```

**When to use:**
- Running code locally on your laptop
- Using gcloud CLI commands
- Testing applications in development

### 2. Service Account Authentication (Apps)
For applications running on GCP or in production.

```bash
# Create a service account
gcloud iam service-accounts create my-app-sa \
  --display-name="My App Service Account"

# Create and download a key (use sparingly!)
gcloud iam service-accounts keys create key.json \
  --iam-account=my-app-sa@PROJECT_ID.iam.gserviceaccount.com

# Use the key
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
```

**When to use:**
- Applications running in production
- CI/CD pipelines
- When you need long-lived credentials

## Quick Setup for Hackathon

For most hackathon work, this is all you need:

```bash
# 1. Login
gcloud auth login

# 2. Set up local development credentials
gcloud auth application-default login

# 3. Verify
gcloud auth list
```

Now your code can use Google Cloud client libraries without any extra configuration!

## Common IAM Roles You'll Need

Grant yourself these roles for full hackathon access:

```bash
# Get your email
EMAIL=$(gcloud config get-value account)
PROJECT_ID=$(gcloud config get-value project)

# Grant roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$EMAIL" \
  --role="roles/editor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$EMAIL" \
  --role="roles/aiplatform.user"
```

### Essential Roles Cheat Sheet

| Role | What it Does | When You Need It |
|------|--------------|------------------|
| `roles/editor` | Read/write access to most resources | Almost always (hackathon default) |
| `roles/owner` | Full control including IAM | When managing permissions |
| `roles/aiplatform.user` | Use Vertex AI services | AI/ML workloads |
| `roles/storage.admin` | Manage Cloud Storage buckets | File storage |
| `roles/cloudfunctions.developer` | Deploy Cloud Functions | Serverless functions |
| `roles/run.admin` | Deploy Cloud Run services | Container deployment |
| `roles/secretmanager.admin` | Manage secrets | Storing API keys |

## Service Accounts for Deployed Apps

When you deploy to Cloud Run or Cloud Functions, GCP automatically creates a service account. You usually don't need to do anything!

**To grant your Cloud Run service access to other GCP services:**

```bash
# Get the default compute service account
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
SA_EMAIL="$PROJECT_NUMBER-compute@developer.gserviceaccount.com"

# Grant it access (example: Cloud Storage)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/storage.objectAdmin"
```

## Authentication in Code

Your code automatically uses credentials when configured correctly:

### Python Example
```python
from google.cloud import storage

# No credentials needed - automatically uses:
# 1. GOOGLE_APPLICATION_CREDENTIALS env var, or
# 2. gcloud auth application-default credentials, or
# 3. Compute Engine/Cloud Run service account

client = storage.Client()
buckets = list(client.list_buckets())
print(buckets)
```

### Node.js Example
```javascript
const {Storage} = require('@google-cloud/storage');

// Automatically authenticated
const storage = new Storage();

async function listBuckets() {
  const [buckets] = await storage.getBuckets();
  console.log('Buckets:', buckets.map(b => b.name));
}
```

## Troubleshooting

**Error: "Could not automatically determine credentials"**
```bash
# Solution: Set up application default credentials
gcloud auth application-default login
```

**Error: "Permission denied" or "403 Forbidden"**
```bash
# Check your roles
gcloud projects get-iam-policy $(gcloud config get-value project) \
  --flatten="bindings[].members" \
  --filter="bindings.members:$(gcloud config get-value account)"

# Grant yourself Editor role
gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/editor"
```

**Error: "The user does not have permission to access service account"**
```bash
# Grant yourself the Service Account User role
gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/iam.serviceAccountUser"
```

## Best Practices for Hackathons

**DO:**
- ✅ Use `gcloud auth application-default login` for local development
- ✅ Use the default service account for deployed apps
- ✅ Store secrets in Secret Manager, not in code
- ✅ Grant yourself `roles/editor` for quick iteration

**DON'T:**
- ❌ Commit service account keys to git
- ❌ Create unnecessary service accounts
- ❌ Use overly restrictive permissions (you'll waste time debugging)
- ❌ Share credentials in Slack/Discord

## Quick Reference Commands

```bash
# Who am I?
gcloud auth list
gcloud config get-value account

# What project am I using?
gcloud config get-value project

# What roles do I have?
gcloud projects get-iam-policy $(gcloud config get-value project) \
  --flatten="bindings[].members" \
  --filter="bindings.members:$(gcloud config get-value account)"

# Create a service account
gcloud iam service-accounts create SA_NAME

# List service accounts
gcloud iam service-accounts list

# Grant a role to a service account
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SA_EMAIL" \
  --role="ROLE_NAME"
```

## Next Steps

**Next:** [Gemini API Quickstart](../2_1_Gemini_API_Quickstart/README.md)
