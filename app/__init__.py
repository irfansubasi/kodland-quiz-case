from flask import Flask
from .models import db, init_db
from .routes import bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    app.register_blueprint(bp)
    
    with app.app_context():
        db.drop_all() #for development. i'll remove this
        init_db()
    
    return app