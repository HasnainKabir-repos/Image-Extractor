# OCR Image Extractor API

A REST API for extracting text from images using **Flask** and **Google Cloud Vision API**.

The API accepts JPG, JPEG, and PNG images, validates the uploaded file, extracts image metadata, performs OCR, and returns the result as JSON.

## 🚀 Live Deployment

Set the Cloud Run URL:

```powershell
$SERVICE_URL = "https://image-extractor-863275486443.asia-south1.run.app"
```

### Linux (Bash)

```bash
export SERVICE_URL="https://image-extractor-863275486443.asia-south1.run.app"
```

## Health Check

```powershell
Invoke-RestMethod `
    -Uri "$SERVICE_URL/health" `
    -Method Get
```

### Linux (Bash)

```bash
curl "$SERVICE_URL/health"
```

## OCR Request

```powershell
Invoke-RestMethod `
    -Uri "$SERVICE_URL/extract-text" `
    -Method Post `
    -Form @{
        image = Get-Item ".\images\test_image_1.jpg"
    }
```

### Linux (Bash)

```bash
curl -X POST \
  -F "image=@images/test_image_1.jpg" \
  "$SERVICE_URL/extract-text"
```

---
## Features

- OCR text extraction using Google Cloud Vision API
- JPG, JPEG, and PNG support
- Image validation using Pillow
- Image metadata extraction
- Maximum upload size protection
- Rate limiting
- Health check endpoint
- Dockerized with Gunicorn
- Automated tests using pytest
- Ready for deployment on Google Cloud Run

---

# Architecture

```text
Client
  │
  │ POST /extract-text
  ▼
Flask API
  │
  ├── Rate limiting
  ├── File validation
  ├── Image validation
  ├── Metadata extraction
  │
  ▼
OCR Service
  │
  ▼
Google Cloud Vision API
  │
  ▼
JSON Response
```

---

# Project Structure

```text
Image_extractor/
│
├── app/
│   ├── routes/
│   │   ├── health.py
│   │   └── ocr.py
│   │
│   ├── services/
│   │   ├── image_service.py
│   │   └── ocr_service.py
│   │
│   ├── utils/
│   │   └── validators.py
│   │
│   ├── __init__.py
│   ├── config.py
│   ├── exceptions.py
│   ├── extensions.py
│   └── logging_config.py
│
├── images/
│   └── test_image_1.jpg
│
├── tests/
│   ├── conftest.py
│   └── test_ocr.py
│
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── run.py
└── README.md
```

---

# Prerequisites

Before running the project, install:

- Python 3.12+
- Docker Desktop
- Google Cloud CLI (`gcloud`)
- A Google Cloud project with billing enabled

---

# Local Setup

## 1. Clone the repository

```powershell
git clone https://github.com/YOUR_USERNAME/image-extractor.git

cd image-extractor
```

Linux (Bash):

```bash
git clone https://github.com/YOUR_USERNAME/image-extractor.git

cd image-extractor
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux (Bash):

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

Linux (Bash):

```bash
pip install -r requirements.txt
```

---

# Google Cloud Setup

## 1. Authenticate with Google Cloud

```powershell
gcloud init
```

Linux (Bash):

```bash
gcloud init
```

Select the Google Cloud project that will be used for the application.

Verify the active project:

```powershell
gcloud config get-value project
```

Linux (Bash):

```bash
gcloud config get-value project
```

---

## 2. Enable the required APIs

```powershell
gcloud services enable `
    vision.googleapis.com `
    run.googleapis.com `
    cloudbuild.googleapis.com `
    artifactregistry.googleapis.com
```

Linux (Bash):

```bash
gcloud services enable \
  vision.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com
```

---

## 3. Configure Application Default Credentials

For local development:

```powershell
gcloud auth application-default login
```

Linux (Bash):

```bash
gcloud auth application-default login
```

Verify that credentials work:

```powershell
gcloud auth application-default print-access-token
```

Linux (Bash):

```bash
gcloud auth application-default print-access-token
```

The Google Cloud Vision Python SDK will automatically discover these credentials during local development.

> Never commit credentials or service account JSON files to the repository.

---

# Running Locally

Start the Flask application:

```powershell
python run.py
```

Linux (Bash):

```bash
python run.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

---

# API Documentation

## Health Check

### Endpoint

```text
GET /health
```

### PowerShell

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/health" `
    -Method Get
```

### Linux (Bash)

```bash
curl "http://127.0.0.1:5000/health"
```

### Example Response

```json
{
  "success": true,
  "status": "healthy"
}
```

---

# Extract Text

### Endpoint

```text
POST /extract-text
```

### Content Type

```text
multipart/form-data
```

### Request Field

| Field | Type | Required | Description |
|---|---|---|---|
| image | File | Yes | JPG, JPEG, or PNG image |

### Supported Formats

- `.jpg`
- `.jpeg`
- `.png`

### Maximum File Size

```text
10 MB
```

---

## PowerShell Example

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/extract-text" `
    -Method Post `
    -Form @{
        image = Get-Item ".\images\test_image_1.jpg"
    }
```

### Linux (Bash)

```bash
curl -X POST \
  -F "image=@images/test_image_1.jpg" \
  "http://127.0.0.1:5000/extract-text"
```

---

## cURL Example

```bash
curl -X POST \
  -F "image=@test_image_1.jpg" \
  http://127.0.0.1:5000/extract-text
```

---

# Successful Response

```json
{
  "success": true,
  "text": "Extracted text from the image",
  "confidence": 0.95,
  "image_metadata": {
    "format": "JPEG",
    "width": 1920,
    "height": 1080,
    "mode": "RGB"
  },
  "processing_time_ms": 1234
}
```

## Response Fields

| Field | Description |
|---|---|
| success | Indicates whether the request was successful |
| text | Extracted text |
| confidence | Overall OCR confidence score |
| image_metadata | Metadata extracted from the uploaded image |
| processing_time_ms | OCR processing time in milliseconds |

## Image Metadata

The API extracts:

- Image format
- Width
- Height
- Color mode

Example:

```json
{
  "format": "PNG",
  "width": 1200,
  "height": 800,
  "mode": "RGB"
}
```

---

# Error Responses

## No Image Provided

**Status:** `400 Bad Request`

```json
{
  "success": false,
  "error": "No image file provided"
}
```

---

## Unsupported File Format

**Status:** `400 Bad Request`

```json
{
  "success": false,
  "error": "File extension not allowed"
}
```

Only JPG, JPEG, and PNG images are supported.

---

## Invalid or Corrupted Image

**Status:** `400 Bad Request`

```json
{
  "success": false,
  "error": "Invalid or corrupted file"
}
```

The application validates the actual image content instead of trusting only the filename extension.

---

## File Too Large

**Status:** `413 Payload Too Large`

```json
{
  "success": false,
  "error": "File exceeds maximum size of 10 MB"
}
```

---

## Rate Limit Exceeded

**Status:** `429 Too Many Requests`

```json
{
  "success": false,
  "error": "Rate limit exceeded. Please try again later."
}
```

Rate limiting helps protect the public API and reduces the risk of excessive OCR API usage.

---

## OCR Processing Failure

**Status:** `500 Internal Server Error`

```json
{
  "success": false,
  "error": "OCR processing failed"
}
```

---

# Rate Limiting

The `/extract-text` endpoint is rate limited.

Example policy:

```text
10 requests per minute per client IP
```

This helps prevent:

- Excessive API usage
- Abuse of the public endpoint
- Unexpected Google Cloud Vision costs

For a production system with multiple Cloud Run instances, a shared rate-limit storage backend such as Redis should be used.

---

# Running Tests

Run the test suite:

```powershell
pytest -v
```

Linux (Bash):

```bash
pytest -v
```

The tests cover:

- Health endpoint
- Missing image file
- Unsupported file types
- JPG uploads
- PNG uploads
- Successful OCR responses
- Image metadata extraction
- Request validation

Google Cloud Vision calls are mocked during tests, so tests do not depend on network access or consume OCR API quota.

---

# Docker

## Build the Image

From the project root:

```powershell
docker build -t image-extractor .
```

Linux (Bash):

```bash
docker build -t image-extractor .
```

---

## Run Locally

For local OCR testing with Google Application Default Credentials:

```powershell
docker run --rm `
    -p 8080:8080 `
    -v "$env:APPDATA\gcloud\application_default_credentials.json:/tmp/adc.json:ro" `
    -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/adc.json `
    image-extractor
```

Linux (Bash):

```bash
docker run --rm \
  -p 8080:8080 \
  -v "$HOME/.config/gcloud/application_default_credentials.json:/tmp/adc.json:ro" \
  -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/adc.json \
  image-extractor
```

The API will be available at:

```text
http://localhost:8080
```

---

## Test Docker Health Endpoint

```powershell
Invoke-RestMethod `
    -Uri "http://localhost:8080/health" `
    -Method Get
```

### Linux (Bash)

```bash
curl "http://localhost:8080/health"
```

---

## Test OCR Inside Docker

```powershell
Invoke-RestMethod `
    -Uri "http://localhost:8080/extract-text" `
    -Method Post `
    -Form @{
        image = Get-Item ".\images\test_image_1.jpg"
    }
```

### Linux (Bash)

```bash
curl -X POST \
  -F "image=@images/test_image_1.jpg" \
  "http://localhost:8080/extract-text"
```

---

# Deploy to Google Cloud Run

## 1. Check the Active Project

```powershell
gcloud config get-value project
```

Linux (Bash):

```bash
gcloud config get-value project
```

If needed:

```powershell
gcloud config set project YOUR_PROJECT_ID
```

Linux (Bash):

```bash
gcloud config set project YOUR_PROJECT_ID
```

---

## 2. Enable Required APIs

```powershell
gcloud services enable `
    run.googleapis.com `
    cloudbuild.googleapis.com `
    artifactregistry.googleapis.com `
    vision.googleapis.com
```

Linux (Bash):

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  vision.googleapis.com
```

---

## 3. Deploy from Source

From the project root:

```powershell
gcloud run deploy image-extractor `
    --source . `
    --region asia-south1 `
    --allow-unauthenticated
```

Linux (Bash):

```bash
gcloud run deploy image-extractor \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated
```

During the first deployment, Google Cloud may ask to create an Artifact Registry repository.

Allow it to create the required repository.

The deployment flow is:

```text
Source Code
    ↓
Cloud Build
    ↓
Docker Image
    ↓
Artifact Registry
    ↓
Cloud Run
    ↓
Public URL
```

After deployment, Cloud Run will return a URL similar to:

```text
https://image-extractor-xxxxx-xx.a.run.app
```

---

# Test the Deployed API

Set the Cloud Run URL:

```powershell
$SERVICE_URL = "https://image-extractor-863275486443.asia-south1.run.app"
```

### Linux (Bash)

```bash
export SERVICE_URL="https://image-extractor-863275486443.asia-south1.run.app"
```

## Health Check

```powershell
Invoke-RestMethod `
    -Uri "$SERVICE_URL/health" `
    -Method Get
```

### Linux (Bash)

```bash
curl "$SERVICE_URL/health"
```

## OCR Request

```powershell
Invoke-RestMethod `
    -Uri "$SERVICE_URL/extract-text" `
    -Method Post `
    -Form @{
        image = Get-Item ".\images\test_image_1.jpg"
    }
```

### Linux (Bash)

```bash
curl -X POST \
  -F "image=@images/test_image_1.jpg" \
  "$SERVICE_URL/extract-text"
```

---

# Cloud Run Authentication

For local development, the application uses Application Default Credentials.

For Cloud Run:

- Do not upload credential JSON files.
- Do not copy credentials into the Docker image.
- Cloud Run should use its service account identity to access Google Cloud services.

If OCR fails after deployment with a permission error, the Cloud Run service account needs the appropriate permission to access the Vision API.

---

# Security Considerations

The API includes:

- File extension validation
- Actual image content validation
- Maximum upload size protection
- Rate limiting
- Corrupted file detection
- Credentials excluded from Docker images
- Production WSGI server using Gunicorn
- Logging for request and OCR processing events

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application language |
| Flask | REST API framework |
| Google Cloud Vision API | OCR |
| Pillow | Image validation and metadata |
| Flask-Limiter | Rate limiting |
| Pytest | Automated testing |
| Gunicorn | Production WSGI server |
| Docker | Containerization |
| Google Cloud Run | Serverless deployment |

---

# Future Improvements

- Redis-backed distributed rate limiting
- OCR confidence improvements
- Batch image processing
- Image preprocessing
- API authentication
- CI/CD with GitHub Actions
- Monitoring and alerting

---

# Author

Hasnain Kabir