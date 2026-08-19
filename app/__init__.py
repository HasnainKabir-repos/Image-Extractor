from flask import Flask

from app.config import Config
from app.routes.ocr import ocr_bp
from app.routes.health import health_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(ocr_bp)
    app.register_blueprint(health_bp)
    return app