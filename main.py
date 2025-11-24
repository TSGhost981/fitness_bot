import telebot
from telebot import types

token = '7612529764:AAHz1cFYDdrw5-VQ0xcpgX-R4Dg0IbvG4P8'
bot = telebot.TeleBot(token)

exercises = {
    'Кардио': 1000,
    'Силовая тренировка': 2000,
    'Йога': 1500,
    'Растяжка': 1200
}

user_data = {}

ADMIN_USER_ID = 5119451328

# Функция для обработки команды /start
def start_handler(message):
    welcome_message = "Добро пожаловать!"
    bot.send_message(message.chat.id, welcome_message)
    show_exercises_menu(message)

# Функция для отображения меню с тренировками
def show_exercises_menu(message):
    markup = types.InlineKeyboardMarkup()
    for exercise, price in exercises.items():
        button_text = exercise + " - " + str(price) + "руб."
        markup.add(types.InlineKeyboardButton(button_text, callback_data=exercise))
    bot.send_message(message.chat.id, "Пожалуйста, выберите тренировку:", reply_markup=markup)

# Обработчик выбора вида тренировки
def exercise_selected(call):
    exercise = call.data
    user_data[call.message.chat.id] = {'exercise': exercise}
    bot.send_message(call.message.chat.id, "Вы выбрали" + " - " + exercise + "\nДля записи на тренировку введите ваш номер телефона:")
    bot.register_next_step_handler(call.message, get_phone_number)

# Функция для запроса номера телефона
def get_phone_number(message):
    phone_number = message.text
    user_data[message.chat.id]['phone_number'] = phone_number
    bot.send_message(message.chat.id, "Введите желаемую дату и время занятия:")
    bot.register_next_step_handler(message, get_date_time)

# Функция для запроса даты и времени
def get_date_time(message):
    date_time = message.text
    user_data[message.chat.id]['date_time'] = date_time
    # Отправка уведомлений пользователю и тренеру
    exercise = user_data[message.chat.id]['exercise']
    phone_number = user_data[message.chat.id]['phone_number']
    bot.send_message(message.chat.id, "Спасибо! Вы хотите записаться на " + exercise + " на " + date_time + "\nЯ свяжусь с вами по номеру " + phone_number + " для уточнения возможности записи.")
    bot.send_message(ADMIN_USER_ID, "Новая запись:\nТренировка: " + exercise + "\nДата и время: " + date_time + "\nТелефон: " + phone_number)
    send_image(message.chat.id)

# Функция для отправки памятки пользователю
def send_image(chat_id):
    image_path = 'Как_подготовиться_к_тренировке.jpg'
    with open(image_path, 'rb') as image:
        bot.send_photo(chat_id, image, caption='Ознакомьтесь, пожалуйста, с памяткой о подготовке к тренировке')

# Регистрация обработчиков
bot.register_message_handler(start_handler, commands=['start'])
bot.register_callback_query_handler(exercise_selected, func=lambda call: call.data in exercises.keys())
bot.register_message_handler(get_phone_number, content_types=['contact'])

# Запуск бота
bot.infinity_polling(none_stop=True)