"""
Multi-agent system with specialized agents
Run with: adk run 4_multi_agent_system
"""

from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool

# Tool for researcher agent
def web_search(query: str) -> dict:
    """Search the web for information."""
    # Mock search results
    return {
        "query": query,
        "results": [
            {"title": f"Article about {query}", "snippet": f"Detailed information on {query}..."},
            {"title": f"{query} explained", "snippet": f"A comprehensive guide to {query}..."},
        ]
    }

def read_article(url: str) -> dict:
    """Read and summarize an article."""
    return {
        "url": url,
        "content": f"This article discusses various aspects of the topic...",
        "key_points": ["Point 1", "Point 2", "Point 3"]
    }

# Researcher agent
researcher = Agent(
    model='gemini-2.5-flash',
    name='researcher',
    description="Researches topics and gathers information",
    instruction="""You are a research specialist. Your job is to:
    1. Search for information on topics
    2. Read and analyze articles
    3. Compile key findings

    Be thorough and factual.""",
    tools=[web_search, read_article],
)

# Writer agent
writer = Agent(
    model='gemini-2.5-flash',
    name='writer',
    description="Creates well-written content based on research",
    instruction="""You are a professional writer. Your job is to:
    1. Take research findings
    2. Create clear, engaging content
    3. Structure information logically

    Write in a clear, professional style.""",
    tools=[],  # No tools, just writing
)

# Reviewer agent
reviewer = Agent(
    model='gemini-2.5-flash',
    name='reviewer',
    description="Reviews content for quality and accuracy",
    instruction="""You are a content reviewer. Your job is to:
    1. Check factual accuracy
    2. Ensure clarity and readability
    3. Suggest improvements

    Be constructive and helpful in your feedback.""",
    tools=[],
)

# Coordinator agent (root agent)
root_agent = Agent(
    model='gemini-2.5-flash',
    name='coordinator',
    description="Coordinates a team of agents to create high-quality content",
    instruction="""You are a project coordinator managing a content creation team.

    Your team consists of:
    - researcher: Gathers information on topics
    - writer: Creates content from research
    - reviewer: Reviews and improves content

    When asked to create content:
    1. Ask the researcher to gather information
    2. Pass the research to the writer to create content
    3. Have the reviewer check the content
    4. Make any final adjustments
    5. Deliver the final product

    Coordinate effectively and ensure high quality output.""",
    tools=[
        AgentTool(researcher),
        AgentTool(writer),
        AgentTool(reviewer)
    ],  # Wrap agents with AgentTool
)
