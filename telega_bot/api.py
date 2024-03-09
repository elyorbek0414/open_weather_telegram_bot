import requests
import json

BASE_URL = 'http://localhost:8000/open_weather_bot/v1'


def create_user(user_name, name, user_id):
    url = f"{BASE_URL}/bot-users"
    response = requests.get(url=url).text
    data = json.loads(response)
    user_exist = False
    for i in data:
        if i["user_id"] == str(user_id):
            user_exist = True
            break
    if user_exist == False:
        requests.post(url=url, data={'username': user_name, "name": name, "user_id": user_id})
        return "Foydalanuvchi yaratildi"
    else:
        return "Foydalanuvchi mavjud!..."


def create_feedback(user_id, body):
    url = f"{BASE_URL}/feedbacks"
    if body and user_id:
        post = requests.post(url=url, data={
            "user_id": user_id,
            "body": body
        })
        return ("🇺🇿: - Adminga jo'natildi. fikringiz uchun rahmat!\n"
                "🇺🇸: - Sent to admin. thanks for your opinion!\n"
                "🇷🇺: - Сообщение отправлено администратору. Спасибо за Ваше мнение!")
    else:
        return "Xatolik yuz berdi. Iltimos qayta urinib ko'ring!"
