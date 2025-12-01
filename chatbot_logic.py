import re
import random 
import time

OPENAI_API_KEY = "YOUR_SECRET_OPENAI_KEY" 

from models import db, Flower, Occasion 

def generate_ai_greeting(flower_name, occasion_name):
    """Mô phỏng việc gọi API AI bên ngoài."""
    
    if OPENAI_API_KEY == "YOUR_SECRET_OPENAI_KEY":
        time.sleep(1) 
        ai_greetings = [
            f"Bằng tất cả tình yêu và sự ngưỡng mộ, tôi xin gửi đến bạn lời chúc được tạo ra từ AI: **Tình yêu rực rỡ như sắc {flower_name} trong ngày {occasion_name}**.",
            f"AI đã tạo ra một lời chúc đặc biệt: **Chúc cho niềm hy vọng và sự tươi sáng mà {flower_name} mang lại sẽ soi đường cho bạn trong mọi chặng đường, đặc biệt là dịp {occasion_name} này.**",
        ]
        return random.choice(ai_greetings)
    else:
    
        return "Xin lỗi, chức năng AI đang bảo trì. Vui lòng thử lại sau."

def clean_input(text):
    return text.lower().strip()

def extract_intent(clean_text):
    """Nhận diện Ý định và trích xuất Thực thể bằng cách truy vấn DB."""
    
    if any(keyword in clean_text for keyword in ["chào", "hi", "xin chào", "alo"]):
        return "INTENT_GREETING", None
    
    if any(keyword in clean_text for keyword in ["mua hàng", "đặt hàng", "mua ngay", "giá"]):
        return "INTENT_ORDERING", None
        
 
    if any(keyword in clean_text for keyword in ["lời chúc ai", "lời chúc tự động", "chúc mới", "ai viết"]):
        
        flowers = Flower.query.all()
        for flower_obj in flowers:
            keywords = flower_obj.keywords.split(',') if flower_obj.keywords else []
            if flower_obj.name in clean_text or any(kw.strip() in clean_text for kw in keywords):
                return "INTENT_REQUEST_AI_GREETING", {"type": "flower", "name": flower_obj.name}
        
        occasions = Occasion.query.all()
        for occasion_obj in occasions:
            keywords = occasion_obj.keywords.split(',') if occasion_obj.keywords else []
            if any(keyword in clean_text for keyword in keywords):
                return "INTENT_REQUEST_AI_GREETING", {"type": "occasion", "name": occasion_obj.name}
                
        return "INTENT_REQUEST_AI_GREETING", None
        

    occasions = Occasion.query.all()
    for occasion_obj in occasions:
        keywords = occasion_obj.keywords.split(',') if occasion_obj.keywords else []
        if any(keyword in clean_text for keyword in keywords):
            return "INTENT_FLOWER_BY_OCCASION", occasion_obj.name
    
 
    flowers = Flower.query.all()
    for flower_obj in flowers:
        keywords = flower_obj.keywords.split(',') if flower_obj.keywords else []
        if flower_obj.name in clean_text or any(kw.strip() in clean_text for kw in keywords):
            return "INTENT_FLOWER_MEANING", flower_obj.name
            
    return "INTENT_UNKNOWN", None

def generate_response(intent, entity):
    """Tạo phản hồi dựa trên dữ liệu từ DB và gọi AI (nếu cần)"""
    
    ai_greeting_prompt = "\n\n✨ **Bạn có muốn tôi tạo một Lời Chúc Độc Đáo bằng AI không?**"

    if intent == "INTENT_FLOWER_BY_OCCASION":
        occasion_obj = Occasion.query.filter_by(name=entity).first()
        if occasion_obj:
            suggestions = occasion_obj.suggestion_list.replace(',', ', ')
            return (f"Dựa trên dịp **{occasion_obj.name.capitalize()}**, chúng tôi gợi ý các loại hoa sau: **{suggestions}**.\n\n"
                    f"💌 **Lời chúc gợi ý (Dữ liệu Động):** \"{occasion_obj.greeting}\"\n\n"
                    f"Bạn muốn tôi tìm hiểu chi tiết hơn về một loại hoa nào không?{ai_greeting_prompt}")

    elif intent == "INTENT_FLOWER_MEANING":
        flower_obj = Flower.query.filter_by(name=entity).first()
        if flower_obj:
            return (f"**{flower_obj.name.capitalize()}** mang ý nghĩa: **{flower_obj.meaning}**.\n"
                    f"💐 **Lời chúc gợi ý (Dữ liệu Động):** \"{flower_obj.greeting}\"{ai_greeting_prompt}")
                    
    elif intent == "INTENT_REQUEST_AI_GREETING":
        if entity:
            flower_name = "loài hoa đẹp nhất" 
            occasion_name = "một dịp đặc biệt"
            
            if entity["type"] == "flower":
                flower_name = entity["name"].capitalize()
            elif entity["type"] == "occasion":
                occasion_name = entity["name"].capitalize()
                
            ai_greeting = generate_ai_greeting(flower_name, occasion_name)
            return f"✅ **Lời chúc AI độc đáo (tạo bởi External API):**\n\n{ai_greeting}"
        else:
             return "Bạn muốn tôi tạo lời chúc AI về loài hoa hoặc dịp lễ nào ạ? Vui lòng cung cấp thêm thông tin."

   
    if intent == "INTENT_GREETING":
        return "Chào bạn! Tôi là trợ lý ảo của cửa hàng hoa 🌸. Bạn cần tôi tư vấn hoa cho dịp gì, hoặc bạn muốn tìm hiểu ý nghĩa loài hoa nào?"
    elif intent == "INTENT_ORDERING":
        return "Tuyệt vời! Bạn có thể xem danh mục sản phẩm của chúng tôi tại [Link Sản Phẩm] hoặc cho tôi biết mã sản phẩm bạn muốn đặt."
    elif intent == "INTENT_UNKNOWN":
        return "Xin lỗi, tôi chưa hiểu rõ yêu cầu của bạn. Bạn có thể hỏi về **dịp tặng hoa** hoặc **tên loài hoa**, hoặc yêu cầu **lời chúc AI** nhé."

    return "Đã xảy ra lỗi hệ thống."

def chatbot_main(user_input):
    """Hàm chính xử lý tin nhắn."""
    clean_text = clean_input(user_input)
    intent, entity = extract_intent(clean_text)
    response = generate_response(intent, entity)
    return response