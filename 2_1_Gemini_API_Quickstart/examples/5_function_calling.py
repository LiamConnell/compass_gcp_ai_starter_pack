"""
Function calling (tool use) with Gemini
Let the model call Python functions to get information
"""

from google import genai
from google.genai import types
import os

# Initialize client
client = genai.Client(
    vertexai=True,
    project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    location="us-central1"
)

# Define actual Python functions
def get_weather(location: str) -> dict:
    """Get weather for a location (mock implementation)"""
    weather_data = {
        "San Francisco": {"temp": "62F", "conditions": "Foggy"},
        "New York": {"temp": "45F", "conditions": "Rainy"},
        "Tokyo": {"temp": "55F", "conditions": "Sunny"},
    }
    return weather_data.get(location, {"temp": "Unknown", "conditions": "Unknown"})


def get_stock_price(symbol: str) -> dict:
    """Get stock price (mock implementation)"""
    prices = {
        "GOOGL": {"price": 142.50, "change": "+2.3%"},
        "AAPL": {"price": 178.20, "change": "-1.1%"},
        "MSFT": {"price": 380.00, "change": "+0.8%"},
    }
    return prices.get(symbol, {"price": 0, "change": "N/A"})


# Define function declarations for Gemini
get_weather_declaration = types.FunctionDeclaration(
    name="get_weather",
    description="Get the current weather for a location",
    parameters={
        "type": "OBJECT",
        "properties": {
            "location": {
                "type": "STRING",
                "description": "The city name, e.g. San Francisco"
            }
        },
        "required": ["location"]
    }
)

get_stock_price_declaration = types.FunctionDeclaration(
    name="get_stock_price",
    description="Get the current stock price for a symbol",
    parameters={
        "type": "OBJECT",
        "properties": {
            "symbol": {
                "type": "STRING",
                "description": "The stock ticker symbol, e.g. GOOGL"
            }
        },
        "required": ["symbol"]
    }
)

# Create tool with both functions
weather_tool = types.Tool(function_declarations=[get_weather_declaration])
stock_tool = types.Tool(function_declarations=[get_stock_price_declaration])

# Map function names to actual functions
available_functions = {
    "get_weather": get_weather,
    "get_stock_price": get_stock_price,
}


def process_message(message: str) -> str:
    """Process a message, handling function calls"""
    print(f"\nUser: {message}")

    # Generate response with tools
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=message,
        config=types.GenerateContentConfig(
            tools=[weather_tool, stock_tool]
        )
    )

    # Check if model wants to call functions
    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        function_name = function_call.name

        print(f"[Calling function: {function_name}({dict(function_call.args)})]")

        # Call the actual Python function
        function_to_call = available_functions[function_name]
        result = function_to_call(**function_call.args)

        print(f"[Function result: {result}]")

        # Send result back to model
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                message,
                types.Content(
                    parts=[types.Part(function_call=function_call)],
                    role="model"
                ),
                types.Content(
                    parts=[types.Part(
                        function_response=types.FunctionResponse(
                            name=function_name,
                            response=result
                        )
                    )],
                    role="user"
                )
            ],
            config=types.GenerateContentConfig(
                tools=[weather_tool, stock_tool]
            )
        )

    return response.text


if __name__ == "__main__":
    print("=== Function Calling Demo ===")
    print("The model can call get_weather() and get_stock_price()")

    # Example queries
    queries = [
        "What's the weather in San Francisco?",
        "How is GOOGL stock doing?",
        "Compare the weather in Tokyo and New York",
    ]

    for query in queries:
        result = process_message(query)
        print(f"Gemini: {result}\n")
