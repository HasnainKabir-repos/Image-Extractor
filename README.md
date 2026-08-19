# Image Extractor

A small Flask API that validates JPEG images and extracts their text with
Google Cloud Vision OCR.

## Features

- Health check endpoint for service monitoring
- JPEG, JPG, and JFIF upload validation
- Image integrity validation with Pillow
- Maximum upload size of 10 MB
- JSON responses with extracted text and processing time
- Local development and Docker/Gunicorn support

## Requirements

- Python 3.12 or later
- A Google Cloud project with the Vision API enabled
- Google Cloud application credentials available to the process

Set up Google Cloud authentication using a service-account key, or another
supported Application Default Credentials method. For a service-account key,
set `GOOGLE_APPLICATION_CREDENTIALS` to its path before starting the API.

PowerShell:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\service-account.json"
```

## Local Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the development server:

```powershell
python run.py
```

The API is available at `http://127.0.0.1:5000`.

## API

### Health check

```http
GET /health
```

Example response:

```json
{
	"success": true,
	"message": "healthy"
}
```

### Extract text

```http
POST /extract-text
Content-Type: multipart/form-data
```

Upload the image in a multipart form field named `image`.

Example with `curl`:

```bash
curl -X POST http://127.0.0.1:5000/extract-text \
	-F "image=@./images/example.jpg"
```

Successful response:

```json
{
	"success": true,
	"message": "Image validation successful",
	"confidence": 0.0,
	"processing_time_ms": 245,
	"text": "Text detected in the image"
}
```

The current OCR service does not calculate confidence yet, so `confidence`
is currently `0.0`. The `text` value contains the full text description
returned by Google Cloud Vision.

Common validation errors return HTTP 400 for missing files, empty filenames,
unsupported extensions, or invalid image data. OCR failures return HTTP 500.

## Docker

Build and run the container:

```bash
docker build -t image-extractor .
docker run --rm -p 8000:8000 \
	-e GOOGLE_APPLICATION_CREDENTIALS=/run/secrets/google-credentials.json \
	-v "$PWD/service-account.json:/run/secrets/google-credentials.json:ro" \
	image-extractor
```

The container listens on port `8000` and runs Gunicorn with the Flask app in
`run:app`.

## Testing

Run the test suite from the project root:

```bash
pytest
```

The OCR success test mocks Google Cloud Vision, so the test suite does not
require live Google Cloud credentials.

## Project Structure

```text
app/
	routes/          Flask endpoints
	services/        Google Cloud Vision integration
	utils/           Upload and image validation
	config.py        Application limits and allowed extensions
run.py             Application entry point
tests/             Pytest tests
Dockerfile         Container image definition
```
