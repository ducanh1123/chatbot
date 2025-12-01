from flask import Blueprint, request, jsonify, render_template
from core.logic import chatbot_main

chatbot_bp = Blueprint('chatbot_bp', __name__)

@chatbot_bp.route('/')
def index():
    """Route cho giao diện web."""
    return render_template('index.html')

@chatbot_bp.route('/chat', methods=['POST'])
def chat_api():
    """API Endpoint chính của Chatbot Service."""
    data = request.get_json()
    user_message = data.get('message', '')
    
    bot_response = chatbot_main(user_message)
    return jsonify({'response': bot_response})