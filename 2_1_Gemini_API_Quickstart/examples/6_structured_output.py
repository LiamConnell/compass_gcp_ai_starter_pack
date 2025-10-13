"""
Structured output with Gemini - get JSON responses with guaranteed schema
"""

from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List
import os

# Initialize client
client = genai.Client(
    vertexai=True,
    project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    location="us-central1"
)


# Example 1: Extract contact information
class ContactInfo(BaseModel):
    """Contact information extracted from text"""
    name: str
    email: str
    phone: str
    company: str | None = None


def extract_contact_info(text: str) -> ContactInfo:
    """Extract structured contact information from text"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=f"Extract contact information from this text: {text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ContactInfo
        )
    )

    # Parse the JSON response into Pydantic model
    return ContactInfo.model_validate_json(response.text)


# Example 2: Product review analysis
class ProductReview(BaseModel):
    """Structured product review analysis"""
    sentiment: str  # positive, negative, neutral
    rating: int  # 1-5
    key_points: List[str]
    recommended: bool
    summary: str


def analyze_review(review_text: str) -> ProductReview:
    """Analyze a product review and return structured data"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=f"""Analyze this product review and provide structured feedback:

Review: {review_text}

Provide sentiment (positive/negative/neutral), rating (1-5),
key points mentioned, whether recommended, and a brief summary.""",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ProductReview
        )
    )

    return ProductReview.model_validate_json(response.text)


# Example 3: Recipe extraction
class Ingredient(BaseModel):
    name: str
    amount: str
    unit: str | None = None


class Recipe(BaseModel):
    """Structured recipe information"""
    title: str
    servings: int
    prep_time: str
    cook_time: str
    ingredients: List[Ingredient]
    instructions: List[str]
    cuisine: str | None = None


def extract_recipe(text: str) -> Recipe:
    """Extract structured recipe from text"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=f"Extract recipe information from this text: {text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Recipe
        )
    )

    return Recipe.model_validate_json(response.text)


# Example 4: Meeting minutes
class ActionItem(BaseModel):
    task: str
    assignee: str
    deadline: str | None = None


class MeetingMinutes(BaseModel):
    """Structured meeting minutes"""
    date: str
    attendees: List[str]
    topics_discussed: List[str]
    decisions_made: List[str]
    action_items: List[ActionItem]
    next_meeting: str | None = None


def generate_meeting_minutes(transcript: str) -> MeetingMinutes:
    """Generate structured meeting minutes from transcript"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=f"""Analyze this meeting transcript and create structured minutes:

{transcript}

Extract the date, attendees, topics discussed, decisions made,
action items with assignees, and next meeting date if mentioned.""",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MeetingMinutes
        )
    )

    return MeetingMinutes.model_validate_json(response.text)


# Example 5: Invoice data extraction
class LineItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total: float


class Invoice(BaseModel):
    """Structured invoice data"""
    invoice_number: str
    date: str
    vendor_name: str
    customer_name: str
    line_items: List[LineItem]
    subtotal: float
    tax: float
    total: float
    payment_terms: str | None = None


def extract_invoice_data(invoice_text: str) -> Invoice:
    """Extract structured data from invoice text"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=f"Extract invoice information from this text: {invoice_text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Invoice
        )
    )

    return Invoice.model_validate_json(response.text)


if __name__ == "__main__":
    print("=== Structured Output Examples ===\n")

    # Example 1: Contact extraction
    print("1. Contact Information Extraction")
    contact_text = """
    John Doe from Acme Corp can be reached at john.doe@acme.com
    or by phone at 555-1234.
    """
    contact = extract_contact_info(contact_text)
    print(f"Name: {contact.name}")
    print(f"Email: {contact.email}")
    print(f"Phone: {contact.phone}")
    print(f"Company: {contact.company}\n")

    # Example 2: Review analysis
    print("2. Product Review Analysis")
    review = """
    This laptop is amazing! The battery life is incredible - lasts all day.
    The screen is bright and crisp. Build quality feels premium.
    A bit pricey but totally worth it. Highly recommended for developers.
    """
    analysis = analyze_review(review)
    print(f"Sentiment: {analysis.sentiment}")
    print(f"Rating: {analysis.rating}/5")
    print(f"Recommended: {analysis.recommended}")
    print(f"Summary: {analysis.summary}\n")

    # Example 3: Recipe extraction
    print("3. Recipe Extraction")
    recipe_text = """
    Chocolate Chip Cookies

    Makes 24 cookies
    Prep: 15 minutes, Bake: 12 minutes

    Ingredients:
    - 2 cups flour
    - 1 tsp baking soda
    - 1 cup butter (softened)
    - 3/4 cup sugar
    - 2 eggs
    - 2 cups chocolate chips

    Instructions:
    1. Preheat oven to 375°F
    2. Mix dry ingredients
    3. Cream butter and sugar
    4. Add eggs, then dry ingredients
    5. Fold in chocolate chips
    6. Bake for 10-12 minutes
    """
    recipe = extract_recipe(recipe_text)
    print(f"Title: {recipe.title}")
    print(f"Servings: {recipe.servings}")
    print(f"Ingredients: {len(recipe.ingredients)} items")
    print(f"Steps: {len(recipe.instructions)}\n")

    print("\nAll examples completed!")
    print("\nBenefits of structured output:")
    print("- Guaranteed JSON schema")
    print("- Type safety with Pydantic models")
    print("- Easy integration with databases and APIs")
    print("- No parsing errors or malformed JSON")
