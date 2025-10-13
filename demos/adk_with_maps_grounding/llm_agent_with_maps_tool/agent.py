# import datetime
# from zoneinfo import ZoneInfo
from google.adk.agents import Agent, LlmAgent

from util_generate_with_maps import generate_with_maps_grounding__as_tool


root_agent = Agent(
    name="maps_tool_agent",
    model="gemini-2.5-flash",
    description=(
        "Agent to answer questions about locations."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about locations using the tools provided."
    ),
    tools=[generate_with_maps_grounding__as_tool],
)