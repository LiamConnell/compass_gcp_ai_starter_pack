"""
Simple agent with a single tool
Run with: adk run 1_simple_agent
"""

from google.adk.agents.llm_agent import Agent

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    # Mock implementation - in production, use a real time API
    times = {
        "Tokyo": "10:30 AM JST",
        "New York": "9:30 PM EST",
        "London": "2:30 AM GMT",
        "San Francisco": "6:30 PM PST",
    }
    return {
        "status": "success",
        "city": city,
        "time": times.get(city, "Unknown city")
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='time_assistant',
    description="Helpful assistant that tells the current time in cities.",
    instruction="""You are a helpful assistant that tells the current time in different cities.
    Use the 'get_current_time' tool to get the time for a specific city.
    Be friendly and conversational.""",
    tools=[get_current_time],
)
