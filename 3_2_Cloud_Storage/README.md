# Cloud Storage

Object storage for files, images, videos, and any unstructured data. Think of it as GCP's version of S3.

## Quick Start

### Create a Bucket

```bash
# Create a bucket (globally unique name required)
gsutil mb gs://my-hackathon-bucket-12345

# Or with specific location
gsutil mb -l us-central1 gs://my-hackathon-bucket-12345

# Or via gcloud
gcloud storage buckets create gs://my-hackathon-bucket-12345 --location=us-central1
```

Bucket names must be globally unique. Add random numbers or your project ID.

### Upload Files

```bash
# Upload a single file
gsutil cp file.txt gs://my-bucket/

# Upload with path
gsutil cp file.txt gs://my-bucket/folder/file.txt

# Upload directory
gsutil cp -r ./my-folder gs://my-bucket/

# Sync directory (like rsync)
gsutil rsync -r ./my-folder gs://my-bucket/my-folder
```

### Download Files

```bash
# Download a file
gsutil cp gs://my-bucket/file.txt .

# Download directory
gsutil cp -r gs://my-bucket/folder ./

# Sync from bucket
gsutil rsync -r gs://my-bucket/folder ./local-folder
```

### List Files

```bash
# List buckets
gsutil ls

# List files in bucket
gsutil ls gs://my-bucket

# List with details
gsutil ls -l gs://my-bucket

# List recursively
gsutil ls -r gs://my-bucket/**
```

## Using Cloud Storage in Python

### Install Library

```bash
pip install google-cloud-storage
```

### Upload & Download

```python
from google.cloud import storage

# Initialize client (automatically authenticated)
client = storage.Client()

# Get bucket
bucket = client.bucket('my-bucket')

# Upload a file
blob = bucket.blob('folder/file.txt')
blob.upload_from_filename('local-file.txt')

# Upload from string
blob = bucket.blob('data.json')
blob.upload_from_string('{"key": "value"}', content_type='application/json')

# Download a file
blob = bucket.blob('folder/file.txt')
blob.download_to_filename('downloaded-file.txt')

# Download as string
content = blob.download_as_string()
print(content.decode('utf-8'))

# Download as bytes
data = blob.download_as_bytes()
```

### List Files

```python
# List all files
blobs = bucket.list_blobs()
for blob in blobs:
    print(blob.name)

# List with prefix (like a folder)
blobs = bucket.list_blobs(prefix='images/')
for blob in blobs:
    print(blob.name)
```

### Delete Files

```python
# Delete a file
blob = bucket.blob('file.txt')
blob.delete()

# Delete multiple files
blobs = bucket.list_blobs(prefix='temp/')
for blob in blobs:
    blob.delete()
```

### Check if File Exists

```python
blob = bucket.blob('file.txt')
if blob.exists():
    print("File exists")
else:
    print("File not found")
```

## Using Cloud Storage in Node.js

### Install Library

```bash
npm install @google-cloud/storage
```

### Upload & Download

```javascript
const {Storage} = require('@google-cloud/storage');

// Initialize client
const storage = new Storage();
const bucket = storage.bucket('my-bucket');

// Upload a file
async function uploadFile() {
  await bucket.upload('local-file.txt', {
    destination: 'folder/file.txt',
  });
  console.log('Uploaded');
}

// Upload from buffer
async function uploadBuffer() {
  const file = bucket.file('data.json');
  await file.save(JSON.stringify({key: 'value'}), {
    contentType: 'application/json',
  });
}

// Download a file
async function downloadFile() {
  await bucket.file('folder/file.txt').download({
    destination: 'downloaded-file.txt',
  });
}

// Download as buffer
async function downloadBuffer() {
  const [content] = await bucket.file('file.txt').download();
  console.log(content.toString());
}
```

## Signed URLs (Temporary Public Access)

Allow temporary access to private files:

### Python
```python
from google.cloud import storage
from datetime import timedelta

client = storage.Client()
bucket = client.bucket('my-bucket')
blob = bucket.blob('private-file.pdf')

# Generate signed URL (valid for 1 hour)
url = blob.generate_signed_url(
    version='v4',
    expiration=timedelta(hours=1),
    method='GET'
)

print(f"Access file at: {url}")
```

### Node.js
```javascript
const [url] = await bucket.file('private-file.pdf').getSignedUrl({
  version: 'v4',
  action: 'read',
  expires: Date.now() + 60 * 60 * 1000, // 1 hour
});

console.log(`Access file at: ${url}`);
```

## Make Files Public

### Via gsutil
```bash
# Make entire bucket public
gsutil iam ch allUsers:objectViewer gs://my-bucket

# Make single file public
gsutil acl ch -u AllUsers:R gs://my-bucket/file.txt

# Remove public access
gsutil acl ch -d AllUsers gs://my-bucket/file.txt
```

### Via Python
```python
blob = bucket.blob('file.txt')
blob.make_public()

# Now accessible at:
print(blob.public_url)
# https://storage.googleapis.com/my-bucket/file.txt
```

### Via Node.js
```javascript
await bucket.file('file.txt').makePublic();

const publicUrl = `https://storage.googleapis.com/${bucket.name}/file.txt`;
console.log(publicUrl);
```

## Metadata & Content Types

### Set Metadata on Upload

```python
blob = bucket.blob('image.jpg')
blob.upload_from_filename(
    'photo.jpg',
    content_type='image/jpeg',
    metadata={
        'description': 'Profile photo',
        'uploaded_by': 'user123'
    }
)
```

### Read Metadata

```python
blob = bucket.blob('image.jpg')
blob.reload()  # Fetch latest metadata

print(f"Content type: {blob.content_type}")
print(f"Size: {blob.size} bytes")
print(f"Created: {blob.time_created}")
print(f"Custom metadata: {blob.metadata}")
```

## Common Patterns

### 1. Upload User Files

```python
from google.cloud import storage
from fastapi import UploadFile

async def upload_user_file(file: UploadFile):
    client = storage.Client()
    bucket = client.bucket('my-bucket')

    # Use safe filename
    blob = bucket.blob(f"uploads/{file.filename}")

    # Upload
    blob.upload_from_file(file.file, content_type=file.content_type)

    # Return public URL or signed URL
    url = blob.public_url
    return {"url": url}
```

### 2. Process Uploaded Images

```python
from google.cloud import storage
from PIL import Image
from io import BytesIO

def resize_image(bucket_name, blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Download image
    blob = bucket.blob(blob_name)
    image_bytes = blob.download_as_bytes()

    # Process with PIL
    image = Image.open(BytesIO(image_bytes))
    image.thumbnail((800, 800))

    # Upload resized version
    output = BytesIO()
    image.save(output, format='JPEG')
    output.seek(0)

    new_blob = bucket.blob(f"thumbnails/{blob_name}")
    new_blob.upload_from_file(output, content_type='image/jpeg')
```

### 3. Streaming Large Files

```python
# Stream download (memory efficient)
blob = bucket.blob('large-file.csv')

with blob.open('r') as f:
    for line in f:
        process_line(line)
```

### 4. Integration with Gemini Vision

```python
from google.cloud import storage
import google.generativeai as genai

# Download image
client = storage.Client()
bucket = client.bucket('my-bucket')
blob = bucket.blob('image.jpg')
image_bytes = blob.download_as_bytes()

# Analyze with Gemini
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash')

from PIL import Image
from io import BytesIO
image = Image.open(BytesIO(image_bytes))

response = model.generate_content([
    "What's in this image?",
    image
])
print(response.text)
```

## Storage Classes & Pricing

### Storage Classes

| Class | Use Case | Price (per GB/month) |
|-------|----------|---------------------|
| Standard | Frequently accessed | $0.020 |
| Nearline | < 1/month access | $0.010 |
| Coldline | < 1/quarter access | $0.004 |
| Archive | < 1/year access | $0.0012 |

**For hackathons:** Use Standard (default).

### Set Storage Class

```bash
# Create bucket with Nearline
gsutil mb -c nearline gs://my-bucket

# Change storage class
gsutil rewrite -s nearline gs://my-bucket/file.txt
```

### Lifecycle Rules (Auto-Delete Old Files)

```bash
# Create lifecycle.json
cat > lifecycle.json << EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {"age": 30}
      }
    ]
  }
}
EOF

# Apply to bucket
gsutil lifecycle set lifecycle.json gs://my-bucket
```

## Permissions

### Grant Access to Cloud Run

```bash
# Get Cloud Run service account
PROJECT_NUMBER=$(gcloud projects describe $(gcloud config get-value project) --format="value(projectNumber)")
SA="$PROJECT_NUMBER-compute@developer.gserviceaccount.com"

# Grant storage access
gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
  --member="serviceAccount:$SA" \
  --role="roles/storage.objectAdmin"
```

### Grant Read-Only Access

```bash
gsutil iam ch serviceAccount:SA_EMAIL:objectViewer gs://my-bucket
```

## Troubleshooting

**Error: "403 Forbidden"**
```bash
# Check your permissions
gsutil iam get gs://my-bucket

# Grant yourself access
gsutil iam ch user:YOUR_EMAIL:objectAdmin gs://my-bucket
```

**Error: "Bucket name already exists"**
- Bucket names are globally unique
- Try adding random numbers or your project ID

**Slow uploads/downloads**
- Use `gsutil -m` for parallel transfers:
```bash
gsutil -m cp -r ./folder gs://my-bucket/
```

**File not found**
```bash
# List to verify
gsutil ls gs://my-bucket/

# Check full path (no folders, just prefixes)
gsutil ls gs://my-bucket/folder/subfolder/
```

## Best Practices

**DO:**
- ✅ Use descriptive bucket names with project ID
- ✅ Use prefixes (folders) to organize files
- ✅ Set appropriate content types
- ✅ Use signed URLs for temporary access
- ✅ Enable versioning for important data

**DON'T:**
- ❌ Make entire buckets public unless necessary
- ❌ Store sensitive data without encryption
- ❌ Use sequential filenames (easy to guess)
- ❌ Forget about storage costs for large files

## Quick Commands Reference

```bash
# Create bucket
gsutil mb gs://BUCKET_NAME

# Upload
gsutil cp FILE gs://BUCKET/
gsutil cp -r FOLDER gs://BUCKET/

# Download
gsutil cp gs://BUCKET/FILE .
gsutil cp -r gs://BUCKET/FOLDER .

# List
gsutil ls gs://BUCKET/

# Delete
gsutil rm gs://BUCKET/FILE
gsutil rm -r gs://BUCKET/FOLDER

# Make public
gsutil acl ch -u AllUsers:R gs://BUCKET/FILE

# Sync
gsutil rsync -r LOCAL_DIR gs://BUCKET/DIR

# Get file info
gsutil ls -L gs://BUCKET/FILE

# Delete bucket
gsutil rm -r gs://BUCKET
```

## Integration Examples

### Store Gemini Responses
```python
from google.cloud import storage
import google.generativeai as genai
import json

# Generate content
response = model.generate_content("Write a story")

# Store in Cloud Storage
client = storage.Client()
bucket = client.bucket('my-bucket')
blob = bucket.blob('ai-output/story.txt')
blob.upload_from_string(response.text)

# Store metadata
metadata = {
    'model': 'gemini-1.5-flash',
    'prompt': 'Write a story',
    'timestamp': str(datetime.now())
}
blob.metadata = metadata
blob.patch()
```

### Serve Static Website
```bash
# Upload website files
gsutil cp -r website/* gs://my-bucket/

# Make bucket public
gsutil iam ch allUsers:objectViewer gs://my-bucket

# Set index and error pages
gsutil web set -m index.html -e 404.html gs://my-bucket

# Access at:
# http://my-bucket.storage.googleapis.com
```

## Next Steps

✅ Created buckets
✅ Uploaded and downloaded files
✅ Integrated with Cloud Run and AI services

**More Topics:**
- [Firestore (NoSQL Database)](../4_2_Firestore/README.md)
- [Complete Examples](../examples/)
