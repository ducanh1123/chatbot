from core.models import db, Flower, Occasion
from flask import Flask

def init_db(app: Flask):
    """Khởi tạo database và điền dữ liệu mẫu."""
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
            print("Database Service đã được khởi tạo và điền dữ liệu mẫu.")