from google import genai
from google.genai import types
import base64
import os

from google.genai import types

def generate_with_maps_grounding(contents: list[types.Content]) -> types.GenerateContentResponse:
  client = genai.Client(
      vertexai=True,
      api_key=os.environ.get("GOOGLE_CLOUD_API_KEY"),
  )

  model = "gemini-2.5-flash"
  contents = contents
  # [
  #   user_content
  #   # types.Content(
  #   #   role="user",
  #   #   parts=[
  #   #     types.Part.from_text(text=query)
  #   #   ]
  #   # ),
  # ]
  tools = [
    types.Tool(google_maps=types.GoogleMaps()),
  ]
  tool_config = types.ToolConfig(
      retrieval_config = types.RetrievalConfig(
          lat_lng = types.LatLng(
            latitude= 40.7137864,
            longitude= -73.948351,
          ),
      ),
  )

  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
    max_output_tokens = 65535,
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
    tools = tools,
    tool_config = tool_config,
    thinking_config=types.ThinkingConfig(
      thinking_budget=0,
    ),
  )

  response = client.models.generate_content(
      model = model,
      contents = contents,
      config = generate_content_config,
    )
  if not response.candidates or not response.candidates[0].content or not response.candidates[0].content.parts:
      print("No content generated.")
      print(response)
      return "No content generated."
    
  # print(response)
  return response
  # return response.candidates[0].content.parts[0].text


def generate_with_maps_grounding__as_tool(query: str) -> str:
  response = generate_with_maps_grounding([
    types.Content(
      role="user",
      parts=[
        types.Part.from_text(text=query)
      ]
    ),
  ])
  if not response.candidates or not response.candidates[0].content or not response.candidates[0].content.parts:
      print("No content generated.")
      print(response)
      return "No content generated."
    
  return response.text