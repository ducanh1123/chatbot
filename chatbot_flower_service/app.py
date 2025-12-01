from flask import Flask
from config import Config
from core.models import db
from db_manager import init_db
from api.chatbot_routes import chatbot_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    app.register_blueprint(chatbot_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        init_db(app) 
    
    print("Service Chatbot Hoa đã khởi động...")
    app.run(debug=True)