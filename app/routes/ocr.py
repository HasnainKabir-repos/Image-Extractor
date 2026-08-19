import time

from flask import Blueprint, current_app, request
from app.utils.validators import (
    is_allowed_extension,
    is_valid_image
)
from app.services.ocr_service import extract_text_from_image

ocr_bp = Blueprint('ocr', __name__)

@ocr_bp.route("/extract-text", methods=["POST"])
def extract_text():

    if "image" not in request.files:

        current_app.logger.warning(
            "OCR request rejected: No image file provided."
        )

        return {
            "success": False,
            "error": "No image file provided."
        }, 400

    image = request.files["image"]

    if image.filename == "":
        return {
            "success": False,
            "error": "No selected file."
        }, 400

    allowed_extensions = current_app.config["ALLOWED_EXTENSIONS"]

    if not is_allowed_extension(
        image.filename,
        allowed_extensions
    ): 
        return {
            "success": False,
            "error": f"File extension not allowed. Allowed extensions: {', '.join(allowed_extensions)}"
        }, 400

    image_bytes = image.read()

    if not is_valid_image(image_bytes):
        return {
            "success": False,
            "error": "Invalid or corrupted file."
        }, 400

    current_app.logger.info(
        "Image validation successful: filename=%s", 
        image.filename
    )

    try:
        start_time = time.perf_counter()
        ocr_result = extract_text_from_image(image_bytes)

        processing_time_ms = round(
            (time.perf_counter() - start_time) * 1000
        )

    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred during OCR processing: {str(e)}"
        }, 500

    current_app.logger.info(
        "OCR processing completed in %s ms",
        processing_time_ms
    )

    return {
        "success": True,
        "message": "Image validation successful",
        "confidence": ocr_result["confidence"],
        "processing_time_ms": processing_time_ms,
        "text": ocr_result["text"]
    }, 200