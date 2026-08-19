from google.cloud import vision
from app.exceptions import OCRProcessingError

def extract_text_from_image(image_bytes):
    """
    Extract text from image bytes.
    """

    try:
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_bytes)
        response = client.text_detection(image=image)
        
        if response.error.message:
            raise OCRProcessingError(response.error.message)
        
        if not response.text_annotations:
            return {
                "text": "",
                "confidence": 0.0
            }
        
        extracted_text = response.text_annotations[0].description
        
        return {
            "text": extracted_text,
            "confidence": 0.0  # TODO: Come back to this
        }

    except OCRProcessingError:
        raise

    except Exception as error:
        raise OCRProcessingError(
            f"OCR processing failed: {str(error)}"
        ) from error