from io import BytesIO

from PIL import Image

def extract_image_metadata(image_bytes):
    with Image.open(BytesIO(image_bytes)) as img:
        return {
            "format": img.format,
            "width": img.width,
            "height": img.height,
            "mode": img.mode
        }