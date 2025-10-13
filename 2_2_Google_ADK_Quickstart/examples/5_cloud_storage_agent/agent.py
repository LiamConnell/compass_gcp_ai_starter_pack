"""
Agent that interacts with Cloud Storage
Requires: pip install google-cloud-storage
Run with: adk run 5_cloud_storage_agent
"""

from google.adk.agents.llm_agent import Agent
from google.cloud import storage
import os

# Initialize Cloud Storage client
storage_client = storage.Client()

def list_buckets() -> dict:
    """List all Cloud Storage buckets in the project."""
    try:
        buckets = list(storage_client.list_buckets())
        return {
            "success": True,
            "buckets": [bucket.name for bucket in buckets],
            "count": len(buckets)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def list_files(bucket_name: str, prefix: str = "") -> dict:
    """List files in a Cloud Storage bucket."""
    try:
        bucket = storage_client.bucket(bucket_name)
        blobs = list(bucket.list_blobs(prefix=prefix))

        return {
            "success": True,
            "bucket": bucket_name,
            "files": [
                {
                    "name": blob.name,
                    "size": blob.size,
                    "updated": blob.updated.isoformat() if blob.updated else None
                }
                for blob in blobs[:20]  # Limit to 20 files
            ],
            "count": len(blobs)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def upload_file(bucket_name: str, source_file: str, destination_name: str) -> dict:
    """Upload a file to Cloud Storage."""
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_name)

        blob.upload_from_filename(source_file)

        return {
            "success": True,
            "bucket": bucket_name,
            "file": destination_name,
            "public_url": blob.public_url
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def download_file(bucket_name: str, source_name: str, destination_file: str) -> dict:
    """Download a file from Cloud Storage."""
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_name)

        blob.download_to_filename(destination_file)

        return {
            "success": True,
            "bucket": bucket_name,
            "file": source_name,
            "saved_to": destination_file
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_file_info(bucket_name: str, file_name: str) -> dict:
    """Get metadata about a file in Cloud Storage."""
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.reload()  # Fetch metadata

        return {
            "success": True,
            "name": blob.name,
            "size": blob.size,
            "content_type": blob.content_type,
            "created": blob.time_created.isoformat() if blob.time_created else None,
            "updated": blob.updated.isoformat() if blob.updated else None,
            "public_url": blob.public_url
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='storage_assistant',
    description="Cloud Storage management assistant",
    instruction="""You are a Cloud Storage assistant. You can help users:

    1. List buckets and files
    2. Upload and download files
    3. Get file information

    When helping users:
    - Ask for bucket names when needed
    - Confirm file operations before executing
    - Provide clear status updates
    - Explain any errors in simple terms

    Be helpful and ensure users understand what's happening with their files.""",
    tools=[
        list_buckets,
        list_files,
        upload_file,
        download_file,
        get_file_info
    ],
)
