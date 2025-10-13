"""
Image editing with Gemini
Edit existing images using text prompts with gemini-2.5-flash-image
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


def edit_image(image_path: str, prompt: str, output_path: str = "edited_image.png"):
    """
    Edit an existing image using a text prompt

    Args:
        image_path: Path to the input image
        prompt: Text description of how to edit the image
        output_path: Path to save the edited image
    """
    print(f"Editing image: {image_path}")
    print(f"Prompt: {prompt}\n")

    # Load the input image
    try:
        input_image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        print("Please provide a valid image path.")
        return None

    # Generate edited image
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[prompt, input_image],
    )

    # Process response parts
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(f"Model says: {part.text}")
        elif part.inline_data is not None:
            # Save the edited image
            edited_image = Image.open(BytesIO(part.inline_data.data))
            edited_image.save(output_path)
            print(f"Edited image saved to: {output_path}")
            return output_path

    return None


if __name__ == "__main__":
    print("=== Image Editing with Gemini ===\n")

    # Example usage (commented out - requires an actual image)
    # image_path = "/path/to/your/image.png"
    # prompt = (
    #     "Create a picture of my cat eating a nano-banana in a "
    #     "fancy restaurant under the Gemini constellation"
    # )
    # edit_image(image_path, prompt, "edited_cat_image.png")

    print("Image editing example ready!")
    print("\nTo use this example:")
    print("1. Uncomment the example code above")
    print("2. Replace '/path/to/your/image.png' with an actual image path")
    print("3. Run the script again")
    print("\nThe model will generate an edited version of your image based on the prompt.")
