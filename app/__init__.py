from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Garante que as pastas existam
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'instance'), exist_ok=True)

    # Importa rotas e registra no app diretamente
    from app import routes
    routes.init_routes(app)

    with app.app_context():
        db.create_all()

    return app