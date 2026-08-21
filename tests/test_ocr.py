from io import BytesIO
from unittest.mock import patch
from PIL import Image

def test_health_check(client):
    response = client.get('/health')

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["message"] == "healthy"

def test_extract_text_without_file(client):
    response = client.post("/extract-text")

    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["error"] == "No image file provided."

def test_reject_unsupported_file_extension(client):
    response = client.post(
        "/extract-text",
        data={
            "image": (
                BytesIO(b"fake image"),
                "image.png"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert response.json["success"] is False

def create_test_jpeg():
    image = Image.new("RGB", (100, 100))

    image_bytes = BytesIO()
    image.save(
        image_bytes,
        format="JPEG"
    )
    image_bytes.seek(0)

    return image_bytes

@patch("app.routes.ocr.extract_text_from_image")
def test_extract_text_success(mock_extract_text, client):
    mock_extract_text.return_value = {
        "text": "Extracted text",
        "confidence": 0.95
    }

    response = client.post(
        "/extract-text",
        data={
            "image": (
                create_test_jpeg(),
                "test_image.jpg"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["text"] == "Extracted text"
    assert response.json["confidence"] == 0.95

def create_test_png():
    image = Image.new("RGB", (100, 100))

    image_bytes = BytesIO()

    image.save(
        image_bytes,
        format="PNG"
    )

    image_bytes.seek(0)

    return image_bytes

@patch("app.routes.ocr.extract_text_from_image")
def test_extract_text_with_png(
    mock_extract_text,
    client
):
    mock_extract_text.return_value = {
        "text": "PNG text",
        "confidence": 0.95,
        "detected_texts": []
    }

    response = client.post(
        "/extract-text",
        data={
            "image": (
                create_test_png(),
                "test.png"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.json["success"] is True

@patch("app.routes.ocr.extract_text_from_image")
def test_image_metadata(
    mock_extract_text,
    client
):
    mock_extract_text.return_value = {
        "text": "Test",
        "confidence": 0.95,
        "detected_texts": []
    }

    response = client.post(
        "/extract-text",
        data={
            "image": (
                create_test_jpeg(),
                "test.jpg"
            )
        },
        content_type="multipart/form-data"
    )

    metadata = response.json["image_metadata"]

    assert metadata["format"] == "JPEG"
    assert metadata["width"] == 100
    assert metadata["height"] == 100
    assert metadata["mode"] == "RGB"