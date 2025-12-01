import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'flower_service.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    EXTERNAL_AI_API_KEY = os.environ.get('AI_API_KEY', 'YOUR_SECRET_OPENAI_KEY')