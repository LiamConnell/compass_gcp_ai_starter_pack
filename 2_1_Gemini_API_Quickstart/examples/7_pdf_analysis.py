"""
Analyze PDF documents with Gemini
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


def analyze_pdf_from_cloud_storage(pdf_uri: str, question: str) -> str:
    """
    Analyze a PDF stored in Cloud Storage

    Args:
        pdf_uri: GCS URI like gs://bucket/document.pdf
        question: What to ask about the PDF
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[
            question,
            types.Part.from_uri(file_uri=pdf_uri, mime_type="application/pdf")
        ]
    )

    return response.text


def analyze_local_pdf(pdf_path: str, question: str) -> str:
    """
    Analyze a local PDF file

    Args:
        pdf_path: Path to local PDF file
        question: What to ask about the PDF
    """

    with open(pdf_path, "rb") as f:
        pdf_data = f.read()

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[
            question,
            types.Part.from_bytes(data=pdf_data, mime_type="application/pdf")
        ]
    )

    return response.text


def extract_structured_data(pdf_uri: str) -> str:
    """Extract structured information from a PDF"""

    prompt = """
    Analyze this document and extract:
    1. Document type (invoice, contract, report, etc.)
    2. Key entities (names, companies, amounts)
    3. Important dates
    4. Summary of main content

    Return as JSON.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[
            prompt,
            types.Part.from_uri(file_uri=pdf_uri, mime_type="application/pdf")
        ]
    )

    return response.text


if __name__ == "__main__":
    # Example usage
    print("PDF Analysis Examples")
    print("=" * 50)

    # Example 1: Question about PDF
    # pdf_uri = "gs://your-bucket/contract.pdf"
    # result = analyze_pdf_from_cloud_storage(
    #     pdf_uri,
    #     "What are the key terms of this contract?"
    # )
    # print(result)

    # Example 2: Summarize PDF
    # result = analyze_pdf_from_cloud_storage(
    #     pdf_uri,
    #     "Provide a 3-sentence summary of this document."
    # )
    # print(result)

    # Example 3: Extract structured data
    # result = extract_structured_data(pdf_uri)
    # print(result)

    print("\nUncomment the examples above to test with your PDFs.")
