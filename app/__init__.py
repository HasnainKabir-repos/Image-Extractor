from flask import Flask

from app.config import Config
from app.exceptions import OCRProcessingError
from app.logging_config import configure_logging
from app.routes.ocr import ocr_bp
from app.routes.health import health_bp
from app.extensions import limiter

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    limiter.init_app(app)

    configure_logging()

    app.register_blueprint(ocr_bp)
    app.register_blueprint(health_bp)
    register_error_handlers(app)
    return app

def register_error_handlers(app):

    @app.errorhandler(OCRProcessingError)
    def handle_ocr_error(error):
        return {
            "success": False,
            "error": "OCR processing failed"
        }, 500

    @app.errorhandler(413)
    def handle_file_too_large(error):
        return {
            "success": False,
            "error": "File is too large. Maximum file size is 16MB."
        }, 413

    @app.errorhandler(429)
    def handle_rate_limit_exceeded(error):
        return {
            "success": False,
            "error": "Rate limit exceeded. Please try again later."
        }, 429