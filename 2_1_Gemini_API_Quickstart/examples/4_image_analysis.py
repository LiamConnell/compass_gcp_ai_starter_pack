"""
Image analysis with Gemini multimodal capabilities
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

# Example 1: Analyze image from Cloud Storage
def analyze_from_cloud_storage(image_uri: str):
    """Analyze an image stored in Cloud Storage"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[
            "Describe this image in detail. What objects do you see?",
            types.Part.from_uri(file_uri=image_uri, mime_type="image/jpeg")
        ]
    )

    return response.text


# Example 2: Analyze local image file
def analyze_local_image(image_path: str):
    """Analyze a local image file"""

    with open(image_path, "rb") as f:
        image_data = f.read()

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[
            "What's in this image? Be specific about colors, objects, and setting.",
            types.Part.from_bytes(data=image_data, mime_type="image/jpeg")
        ]
    )

    return response.text


# Example 3: Compare two images
def compare_images(image1_path: str, image2_path: str):
    """Compare two images"""

    with open(image1_path, "rb") as f1, open(image2_path, "rb") as f2:
        image1_data = f1.read()
        image2_data = f2.read()

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[
            "Compare these two images. What are the similarities and differences?",
            types.Part.from_bytes(data=image1_data, mime_type="image/jpeg"),
            types.Part.from_bytes(data=image2_data, mime_type="image/jpeg")
        ]
    )

    return response.text


if __name__ == "__main__":
    # Example usage with Cloud Storage
    # image_uri = "gs://your-bucket/image.jpg"
    # result = analyze_from_cloud_storage(image_uri)
    # print(result)

    # Example usage with local file
    # result = analyze_local_image("photo.jpg")
    # print(result)

    print("Image analysis examples ready!")
    print("Uncomment the examples above to test with your images.")
