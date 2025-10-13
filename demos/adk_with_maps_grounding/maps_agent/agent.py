from collections.abc import AsyncGenerator
from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent, BaseAgent, LoopAgent, SequentialAgent, InvocationContext
from google.adk.events.event import Event
from google.adk.models.llm_response import LlmResponse

from rich import print

from util_generate_with_maps import generate_with_maps_grounding

class MapsAgent(BaseAgent):
    
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Core logic to run this agent via text-based conversation."""
        print("Input InvocationContext Object:")
        print(ctx)
        contents = [e.content for e in ctx.session.events]
        response = generate_with_maps_grounding(contents=contents)
        event = Event(
            **LlmResponse.create(response).model_dump(), 
            author=self.name
        )
        print("Output Event Object:")
        print(event)
        yield event


root_agent = MapsAgent(
    name="maps_agent",
    description="An agent that can provide information about locations using Google Maps.",
)


