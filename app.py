from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from datetime import datetime
import secrets
import random

# Оптимизация: кэширование статики
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 86400  # Кэш на 24 часа
app.config['TEMPLATES_AUTO_RELOAD'] = False  # Отключаем авто-перезагрузку шаблонов

# Оптимизация: сжатие ответов
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'public, max-age=3600'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

app = Flask(__name__)
app.secret_key = '1606AnnaSecretKey2026'

# Уникальный код доступа
UNIQUE_CODE = "1606Anna"

# Секретный код для карты (регистр важен!)
SECRET_MAP_CODE = "LeFleur2026"  # Оставляем как есть, без upper()

# Короткие комплименты и пожелания для падающих эмодзи
short_messages = {
    "❤️": [
        "Ты - любовь всей моей жизни! 💕",
        "Твоё сердце такое доброе! 💗",
        "С тобой каждый день как праздник! 💖",
        "Ты умеешь любить по-настоящему! 💝"
    ],
    "🌸": [
        "Ты прекрасна как весенний цветок! 🌷",
        "Твоя красота расцветает с каждым днём! 🌺",
        "Ты нежная и красивая как сакура! 🎋",
        "Твоя улыбка как самый красивый цветок! 🌻"
    ],
    "⭐": [
        "Ты сияешь ярче всех звёзд! ✨",
        "Ты - звезда нашего вечера! 🌟",
        "Твой талант освещает путь другим! 💫",
        "Ты рождена быть звездой! ⭐"
    ],
    "🎈": [
        "С днём рождения! Желаю счастья! 🎉",
        "Пусть мечты сбываются! 🎊",
        "Будь всегда на позитиве! 🎵",
        "Желаю море улыбок! 🌊"
    ],
    "🎂": [
        "Сладкой жизни желаю! 🍰",
        "Пусть каждый день будет праздником! 🎪",
        "Желаю исполнения желаний! 🕯️",
        "Ты заслуживаешь самого лучшего! 💝"
    ],
    "💝": [
        "Ты особенная! ✨",
        "Твоя доброта спасает мир! 🦸‍♀️",
        "Ты вдохновляешь меня каждый день! 💪",
        "Спасибо, что ты есть! 🙏"
    ]
}

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    code = request.form.get('code', '').strip()
    
    if code == UNIQUE_CODE:
        session['authenticated'] = True
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Неверный код доступа! 🔐"})

@app.route('/verify-map', methods=['POST'])
def verify_map():
    if not session.get('authenticated'):
        return jsonify({"error": "Не авторизован"}), 401
    
    code = request.json.get('code', '').strip()  # Убираем .upper()
    
    if code == SECRET_MAP_CODE:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "❌ Неверный код! Попробуйте: Le2026"})

@app.route('/map')
def map_page():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    return render_template('map.html')

@app.route('/api/message')
def get_random_message():
    emoji_type = request.args.get('emoji', '❤️')
    messages = short_messages.get(emoji_type, short_messages['❤️'])
    message = random.choice(messages)
    return jsonify({"message": message})

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=300'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
