# Google Agent Development Kit (ADK) Quickstart

Build powerful AI agents with Google's Agent Development Kit - a framework for creating multi-agent systems with tools, memory, and deployment capabilities.

## What is ADK?

The Agent Development Kit (ADK) is Google's framework for building production-ready AI agents. It provides:

- ✅ **LLM Agents** - Build agents powered by Gemini and other models
- ✅ **Tool Integration** - Connect agents to APIs, databases, and services
- ✅ **Multi-Agent Systems** - Create teams of specialized agents
- ✅ **Built-in Deployment** - Deploy to Cloud Run, GKE, or Agent Engine
- ✅ **Session & Memory** - Maintain conversation context and state
- ✅ **Observability** - Monitor and trace agent behavior
- ✅ **MCP Support** - Use Model Context Protocol tools

**Perfect for:** Building chatbots, workflow automation, data analysis agents, and complex multi-agent systems.

## Installation

### Prerequisites

- Python 3.9 or later
- pip for installing packages

### Install ADK

```bash
pip install google-adk
```

**Recommended:** Use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate.bat  # Windows

pip install google-adk
```

## Create Your First Agent

### 1. Create a New Agent Project

```bash
adk create my_agent
```

This creates a project structure:

```
my_agent/
  agent.py      # Main agent code
  .env          # Environment variables (API keys)
  __init__.py
```

### 2. Set Up Authentication

Use Vertex AI for GCP integration (recommended):

```bash
# Authenticate with GCP
gcloud auth application-default login

# Set environment variables (REQUIRED)
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"

# Or use your current gcloud project
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
export GOOGLE_CLOUD_LOCATION="us-central1"
```

**Alternative:** For non-GCP use, get a Gemini API key at [aistudio.google.com/apikey](https://aistudio.google.com/app/apikey) and add to `.env`.

### 3. Update Your Agent

Edit `my_agent/agent.py` to add a tool:

```python
from google.adk.agents.llm_agent import Agent

# Define a tool for the agent
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {
        "status": "success",
        "city": city,
        "time": "10:30 AM"  # Mock implementation
    }

# Create the agent
root_agent = Agent(
    model='gemini-2.5-flash',
    name='time_assistant',
    description="Tells the current time in specified cities.",
    instruction="You are a helpful assistant that tells the current time. Use the 'get_current_time' tool.",
    tools=[get_current_time],
)
```

### 4. Run Your Agent

**Option 1: Command-line interface**

```bash
adk run my_agent
```

You'll get an interactive chat interface in your terminal.

**Option 2: Web interface**

```bash
adk web --port 8000 my_agent
```

Visit http://localhost:8000 to chat with your agent in a web UI.


## Building More Complex Agents

### Multiple Tools
Add multiple tools to give your agent diverse capabilities. Just pass a list of functions to the `tools` parameter.

**Learn more:** [ADK Tools Documentation](https://google.github.io/adk-docs/tools/)

### Memory & Sessions
ADK handles conversation memory automatically through sessions - your agent will remember context across multiple turns without additional configuration.

**Learn more:** [Sessions & Memory](https://google.github.io/adk-docs/sessions/)

### Multi-Agent Systems
Create specialized agents for different tasks and coordinate them by passing agents as tools to other agents. This enables complex workflows with division of labor.

**Learn more:** [Multi-Agent Systems](https://google.github.io/adk-docs/multi-agent/)

## Deploying to Cloud Run

ADK makes it easy to deploy agents to Cloud Run.

### 1. Create Deployment Configuration

Create `agent_config.yaml`:

```yaml
agent:
  name: my_agent
  model: gemini-2.5-flash
  model_provider: vertex

deploy:
  platform: cloud_run
  region: us-central1
  project_id: your-project-id
```

### 2. Deploy

```bash
adk deploy my_agent --config agent_config.yaml
```

This will:
- Containerize your agent
- Deploy to Cloud Run
- Set up authentication
- Give you a public URL

### 3. Access Your Agent

ADK creates a REST API for your agent:

```bash
# Get deployment URL
URL=$(gcloud run services describe my-agent --region us-central1 --format='value(status.url)')

# Send a message
curl -X POST $URL/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What time is it in Tokyo?"}'
```

## Built-in Tools

ADK provides ready-to-use tools for common tasks:

- **Google Cloud Tools** - CloudStorageTool, BigQueryTool, VertexSearchTool for GCP integration
- **Web Search** - GoogleSearchTool for grounding with real-time information
- **MCP (Model Context Protocol)** - Connect to any MCP server for filesystem access, APIs, databases, and more

**Learn more:**
- [Built-in Tools Reference](https://google.github.io/adk-docs/tools/built-in/)
- [MCP Documentation](https://google.github.io/adk-docs/mcp/)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)

## Example: Customer Support Agent

```python
from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_cloud import BigQueryTool

def lookup_order(order_id: str) -> dict:
    """Looks up order details."""
    return {
        "order_id": order_id,
        "status": "shipped",
        "tracking": "1Z999AA10123456784"
    }

def create_ticket(issue: str, customer_email: str) -> dict:
    """Creates a support ticket."""
    return {"ticket_id": "TKT-12345", "status": "created"}

support_agent = Agent(
    model='gemini-2.5-flash',
    name='customer_support',
    description="Customer support agent",
    instruction="""You are a friendly customer support agent. You can:
    1. Look up order information
    2. Create support tickets
    3. Answer common questions

    Always be polite and helpful.""",
    tools=[lookup_order, create_ticket],
)
```

Run it:

```bash
adk run support_agent
```

## Observability & Debugging

### View Agent Logs

```bash
# Enable detailed logging
export ADK_LOG_LEVEL=DEBUG

adk run my_agent
```

### Cloud Trace Integration

ADK automatically integrates with Cloud Trace when deployed:

```python
from google.adk.observability import enable_tracing

enable_tracing(project_id="your-project-id")
```

View traces in Cloud Console: [console.cloud.google.com/traces](https://console.cloud.google.com/traces)

## Testing Your Agent

```python
# test_agent.py
from google.adk.testing import AgentTestCase
from agent import root_agent

class TestMyAgent(AgentTestCase):
    def test_time_query(self):
        response = self.run_agent(
            root_agent,
            "What time is it in Tokyo?"
        )
        self.assertIn("Tokyo", response)

    def test_tool_usage(self):
        response = self.run_agent(
            root_agent,
            "Tell me the time in New York"
        )
        # Verify the get_current_time tool was called
        self.assert_tool_called("get_current_time")
```

Run tests:

```bash
pytest test_agent.py
```

## Key Concepts

### Agents
The core building block - an AI entity that can use tools and make decisions.

### Tools
Functions that agents can call (APIs, databases, other agents).

### Sessions
Conversation context - ADK manages this automatically.

### Memory
Long-term storage of information across sessions.

### Runtime
The environment where agents execute (local, Cloud Run, GKE).

## ADK vs Building from Scratch

| Feature | ADK | From Scratch |
|---------|-----|--------------|
| Agent creation | ✅ One function call | ❌ Lots of boilerplate |
| Tool integration | ✅ Automatic | ❌ Manual function calling |
| Deployment | ✅ `adk deploy` | ❌ Docker + YAML config |
| Memory/Sessions | ✅ Built-in | ❌ Build your own |
| Observability | ✅ Automatic | ❌ Manual instrumentation |
| Multi-agent | ✅ Agents as tools | ❌ Complex coordination |

## Common Patterns

### 1. Chat Agent with Session Memory

```python
agent = Agent(
    model='gemini-2.5-flash',
    name='chat_bot',
    instruction="You are a helpful chatbot. Remember user preferences.",
)
```

### 2. Task Automation Agent

```python
agent = Agent(
    model='gemini-2.5-flash',
    tools=[send_email, create_calendar_event, update_spreadsheet],
    instruction="Automate tasks by using the provided tools."
)
```

### 3. Data Analysis Agent

```python
from google.adk.tools.google_cloud import BigQueryTool

analyst = Agent(
    model='gemini-2.5-flash',
    tools=[BigQueryTool()],
    instruction="Analyze data and provide insights. Query the database when needed."
)
```

## Troubleshooting

**Error: "API key not valid"**
```bash
# Make sure GOOGLE_API_KEY is set in .env
cat my_agent/.env
```

**Error: "Module not found"**
```bash
# Make sure you're in the virtual environment
which python  # Should point to .venv

# Reinstall ADK
pip install --upgrade google-adk
```

**Agent not using tools**
- Make sure tools have docstrings (required for agent to understand what they do)
- Check instruction mentions the tools
- Review model selection (some models are better at tool use)

**Deployment fails**
```bash
# Make sure you're authenticated
gcloud auth login
gcloud auth application-default login

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

## Resources

- **Official Docs:** [google.github.io/adk-docs](https://google.github.io/adk-docs/)
- **GitHub:** [github.com/google/adk-python](https://github.com/google/adk-python)
- **Code Samples:** [github.com/google/adk-samples](https://github.com/google/adk-samples)
- **Deploy Guide:** [ADK Cloud Run Deployment](https://google.github.io/adk-docs/deploy/cloud-run/)

## Next Steps

✅ Created your first ADK agent
✅ Added tools and tested locally
✅ Understand deployment options

**Next:**
- [Cloud Run Deployment](../3_1_Cloud_Run_Deployment/README.md) - Deploy your agent
- [Cloud Storage](../3_2_Cloud_Storage/README.md) - Add file storage capabilities
- [Advanced ADK Patterns](https://google.github.io/adk-docs/tutorials/) - Build complex agents
