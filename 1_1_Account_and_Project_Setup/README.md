# Account & Project Setup

## Creating Your First GCP Project

### What is a GCP Project?

A GCP Project is the basic container for all your GCP resources. It's lightweight and easy to create - you can have many projects for different purposes.

**Coming from AWS?** See [GCP-AWS Concept Comparison Map](../GCP_AWS_Concept_Comparison_Map.md) for detailed translations.

### Create a New Project

#### Option 1: Via Console
1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Click the project dropdown (top navigation bar)
3. Click "New Project"
4. Enter a project name (e.g., `my-hackathon-project`)
5. Click "Create"

#### Option 2: Via CLI 
```bash
# Create a new project
gcloud projects create my-hackathon-project --name="My Hackathon Project"

# Set it as your default project
gcloud config set project my-hackathon-project
```

### Set Default Project & Region

```bash
# Set your project ID
export PROJECT_ID="my-hackathon-project"
gcloud config set project $PROJECT_ID

# Set your default region (choose one close to you)
gcloud config set compute/region us-central1

# Verify your settings
gcloud config list
```

### Enable Required APIs

Instead of enabling APIs one-by-one, enable all the common AI/ML APIs at once:

```bash
# Enable all AI and deployment APIs you'll need
gcloud services enable \
  aiplatform.googleapis.com \
  cloudresourcemanager.googleapis.com \
  compute.googleapis.com \
  storage.googleapis.com \
  cloudfunctions.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  firestore.googleapis.com \
  vision.googleapis.com \
  language.googleapis.com \
  speech.googleapis.com \
  texttospeech.googleapis.com \
  translate.googleapis.com \
  documentai.googleapis.com
```

This takes 1-2 minutes. You'll see each API being enabled.

You can always use the Cloud Console to enable services by searching for the service and clicking enable. 

<!-- ### Understanding Billing

**Important:** You need a billing account linked to your project to use GCP services.

**For Hackathons:**
- You should have received credits or a coupon code
- Apply it at [console.cloud.google.com/billing](https://console.cloud.google.com/billing)

**Check your billing status:**
```bash
gcloud billing projects describe $PROJECT_ID
```

### Project Organization Best Practices for Hackathons

**Keep it simple:**
- ✅ One project per hackathon team
- ✅ Enable all APIs upfront (avoid "API not enabled" errors later)
- ✅ Use the same region for all services (reduces latency & complexity)
- ❌ Don't create folders or complex hierarchies
- ❌ Don't create multiple projects unless you need isolation

### Quick Verification

Run this to confirm everything is set up:

```bash
echo "Project ID: $(gcloud config get-value project)"
echo "Region: $(gcloud config get-value compute/region)"
echo "Account: $(gcloud config get-value account)"
gcloud services list --enabled --filter="name:aiplatform OR name:run OR name:storage"
```

You should see:
- Your project ID
- Your chosen region
- Your email account
- A list of enabled APIs -->

### Troubleshooting

**Error: "The caller does not have permission"**
- Solution: Make sure you're an Owner or Editor on the project
- Check: `gcloud projects get-iam-policy $PROJECT_ID`

**Error: "Billing must be enabled"**
- Solution: Link a billing account at [console.cloud.google.com/billing](https://console.cloud.google.com/billing)

**Can't find my project**
- List all projects: `gcloud projects list`
- Make sure you created it in the right organization

## Set Up Gemini CLI (Optional but Recommended)

The Gemini CLI gives you an AI assistant in your terminal that can help with GCP tasks, debugging, and infrastructure questions.

### Install Gemini CLI

```bash
# Install via pip
pip install google-gemini-cli

# Or install from source
git clone https://github.com/google-gemini/gemini-cli.git
cd gemini-cli
pip install -e .
```

### Configure for Vertex AI

```bash
# Set environment variables to use Vertex AI
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
export GOOGLE_CLOUD_LOCATION="us-central1"

# Add to your shell profile (~/.bashrc, ~/.zshrc) to persist
echo 'export GOOGLE_GENAI_USE_VERTEXAI=TRUE' >> ~/.bashrc
echo 'export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)' >> ~/.bashrc
echo 'export GOOGLE_CLOUD_LOCATION="us-central1"' >> ~/.bashrc
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
