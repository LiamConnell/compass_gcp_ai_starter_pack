"""
Image generation with Gemini
Generate images from text prompts using gemini-2.5-flash-image
"""

import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Initialize client
client = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
)


def generate_image(prompt: str, output_path: str = "generated_image.png"):
    """
    Generate an image from a text prompt

    Args:
        prompt: Text description of the image to generate
        output_path: Path to save the generated image
    """
    print(f"Generating image from prompt: {prompt}\n")

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[prompt],
    )

    # Process response parts
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(f"Model says: {part.text}")
        elif part.inline_data is not None:
            # Save the generated image
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(output_path)
            print(f"Image saved to: {output_path}")
            return output_path

    return None


if __name__ == "__main__":
    print("=== Image Generation with Gemini ===\n")

    # Example 1: Generate a simple image
    prompt1 = "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
    generate_image(prompt1, "nano_banana_restaurant.png")

    print("\n" + "="*50 + "\n")

    # Example 2: More detailed prompt
    prompt2 = "A serene mountain landscape at sunset with purple and orange sky, reflecting on a calm lake"
    generate_image(prompt2, "mountain_sunset.png")

    print("\n" + "="*50)
    print("\nImage generation complete!")
    print("Check the generated PNG files in the current directory.")
