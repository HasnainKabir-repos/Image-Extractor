from io import BytesIO
from PIL import Image, UnidentifiedImageError
from app.config import Config

def is_allowed_extension(filename, allowed_extensions=Config.ALLOWED_EXTENSIONS):
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in allowed_extensions

def is_valid_image(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes))
        image.verify()
        return True

    except (UnidentifiedImageError, OSError):
        return False