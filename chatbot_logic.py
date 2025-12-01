from flower_data import FLOWER_DATA, OCCASION_MAP
import re

def clean_input(text):
    return text.lower().strip()

def extract_intent(clean_text):
    """Nhận diện Ý định và trích xuất Thực thể"""
    
    if any(keyword in clean_text for keyword in ["chào", "hi", "xin chào", "alo"]):
        return "INTENT_GREETING", None
    
    if any(keyword in clean_text for keyword in ["mua hàng", "đặt hàng", "mua ngay", "giá"]):
        return "INTENT_ORDERING", None

    for occasion, data in OCCASION_MAP.items():
        if any(keyword in clean_text for keyword in data['keywords']):
            return "INTENT_FLOWER_BY_OCCASION", occasion

    for flower_name, data in FLOWER_DATA.items():
        if flower_name in clean_text or any(kw in clean_text for kw in data['keywords']):
            return "INTENT_FLOWER_MEANING", flower_name
            
    return "INTENT_UNKNOWN", None

def generate_response(intent, entity):
    """Tạo phản hồi"""
    if intent == "INTENT_GREETING":
        return "Chào bạn! Tôi là trợ lý ảo của cửa hàng hoa 🌸. Bạn cần tôi tư vấn hoa cho dịp gì, hoặc bạn muốn tìm hiểu ý nghĩa loài hoa nào?"

    elif intent == "INTENT_ORDERING":
        return "Tuyệt vời! Bạn có thể xem danh mục sản phẩm của chúng tôi tại [Link Sản Phẩm] hoặc cho tôi biết mã sản phẩm bạn muốn đặt."

    elif intent == "INTENT_FLOWER_BY_OCCASION":
        occasion = entity
        suggestions = ", ".join(OCCASION_MAP[occasion]["suggestions"])
        greeting = OCCASION_MAP[occasion]["greeting"]
        return (f"Dựa trên dịp **{occasion.capitalize()}**, chúng tôi gợi ý các loại hoa sau: **{suggestions}**.\n\n"
                f"💌 **Lời chúc gợi ý:** \"{greeting}\"\n\n"
                "Bạn muốn tôi tìm hiểu chi tiết hơn về một loại hoa nào không?")

    elif intent == "INTENT_FLOWER_MEANING":
        flower_name = entity
        info = FLOWER_DATA[flower_name]
        occasions = ", ".join(info["occasions"])
        return (f"**{flower_name.capitalize()}** mang ý nghĩa: **{info['meaning']}**.\n"
                f"Thường được tặng vào các dịp: **{occasions}**.\n"
                f"💐 **Lời chúc gợi ý:** \"{info['greeting']}\"")

    elif intent == "INTENT_UNKNOWN":
        return "Xin lỗi, tôi chưa hiểu rõ yêu cầu của bạn. Bạn có thể hỏi về **dịp tặng hoa** (ví dụ: sinh nhật) hoặc **tên loài hoa** (ví dụ: hoa hồng) nhé."
    
    return "Đã xảy ra lỗi hệ thống."

def chatbot_main(user_input):
    """Hàm chính xử lý tin nhắn và tạo phản hồi cuối cùng."""
    clean_text = clean_input(user_input)
    intent, entity = extract_intent(clean_text)
    response = generate_response(intent, entity)
    return response