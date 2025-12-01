# app.py (API Server)
from flask import Flask, request, jsonify, render_template
from chatbot_logic import chatbot_main

app = Flask(__name__)


def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat_api():
    """
    Đây là API Endpoint.
    - Nhận request POST có chứa JSON data {"message": "tin nhắn người dùng"}.
    - Trả về response JSON {"response": "phản hồi của bot"}.
    """
    
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid request format'}), 400
        
    user_message = data.get('message', '')
    
    bot_response = chatbot_main(user_message)
    
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)