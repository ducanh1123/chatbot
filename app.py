from flask import Flask, request, jsonify, render_template
import os
from models import db, Flower, Occasion 
from chatbot_logic import chatbot_main

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'flower_db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app) 
    return app

def init_db(app):
    """Hàm khởi tạo và điền dữ liệu mẫu vào DB."""
    with app.app_context():
        db.create_all()

        if not Flower.query.first():
            flowers = [
                Flower(name='hoa hồng đỏ', meaning='Tình yêu mãnh liệt, lãng mạn, sự tôn kính.', 
                       greeting='Chúc tình yêu của chúng ta mãi nồng cháy!', keywords='hồng đỏ,tình yêu,lãng mạn'),
                Flower(name='hoa hướng dương', meaning='Niềm tin, hy vọng, lòng trung thành.', 
                       greeting='Chúc bạn luôn vững bước và đạt được thành công rỡ!', keywords='hướng dương,thành công,hy vọng'),
            ]
            occasions = [
                Occasion(name='sinh nhật', suggestion_list='hoa hồng,hoa hướng dương,hoa ly', 
                         greeting='Chúc mừng sinh nhật! Chúc bạn tuổi mới nhiều niềm vui, sức khỏe và thành công!', keywords='sinh nhật,sn,mừng tuổi'),
                Occasion(name='valentine', suggestion_list='hoa hồng đỏ,hoa tulip,hoa baby', 
                         greeting='Gửi đến em/anh tình yêu nồng nàn nhất. Valentine vui vẻ và mãi mãi bên nhau nhé!', keywords='valentine,14/2'),
            ]
            db.session.add_all(flowers)
            db.session.add_all(occasions)
            db.session.commit()
            print("Database đã được khởi tạo với dữ liệu mẫu.")

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_api():
    """API Endpoint nhận request và gọi logic xử lý."""
    data = request.get_json()
    user_message = data.get('message', '')
    
   
    with app.app_context(): 
        bot_response = chatbot_main(user_message)
        return jsonify({'response': bot_response})

if __name__ == '__main__':
  
    init_db(app) 
    app.run(debug=True)