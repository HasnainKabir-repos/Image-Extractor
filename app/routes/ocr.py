from flask import Blueprint, current_app, request
from app.utils.validators import is_allowed_extension
from app.services.ocr_service import extract_text_from_image

ocr_bp = Blueprint('ocr', __name__)

@ocr_bp.route("/extract-text", methods=["POST"])
def extract_text():
    if "image" not in request.files:
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
    ocr_result = extract_text_from_image(image_bytes)
    
    return {
        "success": True,
        "message": "Image validation successful",
        "size": len(image_bytes)
    }, 200