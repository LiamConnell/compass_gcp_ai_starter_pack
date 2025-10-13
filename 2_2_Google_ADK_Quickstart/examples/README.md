# Google ADK Examples

Practical examples of building agents with the Agent Development Kit.

## Setup

```bash
# Install ADK
pip install google-adk

# For Cloud Storage example
pip install google-cloud-storage

# Authenticate (choose one)
# Option 1: Use Vertex AI (recommended for GCP)
gcloud auth application-default login
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"

# Option 2: Use API key (for non-GCP use)
echo 'GOOGLE_API_KEY="your-key"' > .env
```

## Examples

### 1. Simple Agent
**Directory:** `1_simple_agent/`

Basic agent with a single tool that tells the time in different cities.

```bash
cd 1_simple_agent
adk run .
```

Try asking: "What time is it in Tokyo?"

### 2. Multi-Tool Agent
**Directory:** `2_multi_tool_agent/`

Shopping assistant with product search, inventory check, and order creation.

```bash
cd 2_multi_tool_agent
adk run .
```

Try asking: "Search for laptops" or "Check inventory for product 1"

### 3. Customer Support Agent
**Directory:** `3_customer_support_agent/`

Full customer support system with knowledge base, order lookup, and ticketing.

```bash
cd 3_customer_support_agent
adk run .
```

Try asking: "What's your return policy?" or "Look up order ORD-12345"

### 4. Multi-Agent System
**Directory:** `4_multi_agent_system/`

Demonstrates agents working together - researcher, writer, and reviewer coordinated by a main agent.

```bash
cd 4_multi_agent_system
adk run .
```

Try asking: "Research and write an article about cloud computing"

### 5. Cloud Storage Agent
**Directory:** `5_cloud_storage_agent/`

Agent that manages Cloud Storage buckets and files. Requires GCP authentication.

```bash
cd 5_cloud_storage_agent

# Set environment variables
export GOOGLE_CLOUD_PROJECT="your-project-id"

# Run
adk run .
```

Try asking: "List my buckets" or "Show files in my-bucket"

## Running Examples

### Command-Line Interface

```bash
# Run any example
adk run <directory>

# Example
adk run 1_simple_agent
```

### Web Interface

```bash
# Start web UI
adk web --port 8000 <directory>

# Example
adk web --port 8000 2_multi_tool_agent
```

Then visit http://localhost:8000

## Deploying Examples

Deploy any agent to Cloud Run:

```bash
cd <example-directory>

# Create config
cat > agent_config.yaml << EOF
agent:
  name: my_agent
  model: gemini-2.0-flash-exp
  model_provider: vertex

deploy:
  platform: cloud_run
  region: us-central1
  project_id: your-project-id
EOF

# Deploy
adk deploy . --config agent_config.yaml
```

## Common Patterns

### Basic Agent Structure

```python
from google.adk.agents.llm_agent import Agent

def my_tool(param: str) -> dict:
    """Tool description for the AI."""
    return {"result": "value"}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='my_agent',
    description="What the agent does",
    instruction="Instructions for how to behave",
    tools=[my_tool],
)
```

### Using Vertex AI

Set environment variables before running:

```bash
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
```

Then create your agent normally - ADK will use Vertex AI automatically:

```python
root_agent = Agent(
    model='gemini-2.5-flash',
    name='my_agent',
    # ... rest of config
)
```

### Agent as a Tool

```python
# Create specialized agents
researcher = Agent(...)
writer = Agent(...)

# Use them as tools in another agent
coordinator = Agent(
    tools=[researcher, writer],  # Agents as tools!
    # ...
)
```

## Testing

Create tests for your agents:

```python
# test_agent.py
from google.adk.testing import AgentTestCase
from agent import root_agent

class TestMyAgent(AgentTestCase):
    def test_basic_interaction(self):
        response = self.run_agent(
            root_agent,
            "Hello, how are you?"
        )
        self.assertIsNotNone(response)
```

Run tests:

```bash
pytest test_agent.py
```

## Best Practices

1. **Clear Tool Descriptions** - Tools need good docstrings for the AI to understand them
2. **Detailed Instructions** - Give agents clear behavioral guidelines
3. **Error Handling** - Return error dictionaries from tools, don't raise exceptions
4. **Mock Data** - Use mock implementations for quick prototyping
5. **Start Simple** - Begin with one tool, add complexity gradually

## Troubleshooting

**Agent not using tools**
- Check that tool functions have docstrings
- Verify tool parameters are clearly typed
- Review agent instructions

**Authentication errors**
- Run `gcloud auth application-default login`
- Check GOOGLE_CLOUD_PROJECT is set
- Verify APIs are enabled

**Import errors**
```bash
# Reinstall ADK
pip install --upgrade google-adk
```

## Next Steps

- Explore [ADK Documentation](https://google.github.io/adk-docs/)
- Check [Code Samples](https://github.com/google/adk-samples)
- Read the [main ADK guide](../README.md)
- Deploy your agent to production
