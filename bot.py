import telebot
import urllib.parse

# Ваш токен и номер WhatsApp
bot = telebot.TeleBot('7833284290:AAE_d1qqk7o3CTC7sAY2gMJ2b5Z7g-Q9It4')  # Замените на ваш токен
whatsapp_number = '77014815213'  # Ваш номер для WhatsApp (без знака +)

# Обновленный список услуг и цен
services = {
    "Адаптация под вакансию": 15000,
    "Создание нового резюме": 20000,
    "Перевод резюме на английский": 20000,
    "Оформление LinkedIn профиля": 10000,
    "Комплексный пакет (резюме + LinkedIn)": 27000
}

# Вопросы для теста
questions = [
    "Вы хотите адаптировать резюме под конкретную вакансию?",
    "Нужно ли вам создать новое резюме?",
    "Необходимо ли перевести резюме на английский язык?",
    "Вы хотите оформить LinkedIn профиль?",
    "Вы хотите приобрести комплексный пакет (резюме + LinkedIn)?"
]

# Сюда будем записывать ответы пользователя
answers = []

# Функция для начала опроса
def start_survey(message):
    bot.send_message(message.chat.id, questions[0], reply_markup=create_yes_no_keyboard())
    answers.clear()  # Очищаем предыдущие ответы

# Создание клавиатуры с кнопками "Да" и "Нет"
def create_yes_no_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Да"), telebot.types.KeyboardButton("Нет"))
    return markup

# Функция для обработки ответа пользователя
def handle_answer(message, question_index):
    if message.text == "Да":
        answers.append(True)
    elif message.text == "Нет":
        answers.append(False)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, ответьте 'Да' или 'Нет'.")
        return

    if question_index < len(questions) - 1:
        # Переходим к следующему вопросу
        bot.send_message(message.chat.id, questions[question_index + 1], reply_markup=create_yes_no_keyboard())
    else:
        # Завершаем опрос, показываем итог
        show_final_summary(message)

# Функция для вывода итогового сообщения
def show_final_summary(message):
    selected_services = []
    total_price = 0

    # Применяем логику, если ответ "Да" на вопрос, добавляем услугу в список
    if answers[0]:  # Адаптация под вакансию
        selected_services.append("Адаптация под вакансию")
        total_price += services["Адаптация под вакансию"]
    if answers[1]:  # Создание нового резюме
        selected_services.append("Создание нового резюме")
        total_price += services["Создание нового резюме"]
    if answers[2]:  # Перевод резюме на английский
        selected_services.append("Перевод резюме на английский")
        total_price += services["Перевод резюме на английский"]
    if answers[3]:  # Оформление LinkedIn
        selected_services.append("Оформление LinkedIn профиля")
        total_price += services["Оформление LinkedIn профиля"]
    if answers[4]:  # Комплексный пакет
        selected_services.append("Комплексный пакет (резюме + LinkedIn)")
        total_price += services["Комплексный пакет (резюме + LinkedIn)"]

    # Формируем итоговое сообщение
    final_message = "🛍️ Вы выбрали следующие услуги:\n"
    for service in selected_services:
        final_message += f"✅ {service} — {services[service]} тг\n"
    final_message += f"\n💵 Итоговая сумма: {total_price} тг"

    # Формируем текст для WhatsApp
    whatsapp_text = "Здравствуйте!\nЯ хочу заказать:\n"
    for service in selected_services:
        whatsapp_text += f"✅ {service}\n"
    whatsapp_text += f"💵 Итоговая сумма: {total_price} тг."

    # Кодируем текст для ссылки
    encoded_whatsapp_text = urllib.parse.quote(whatsapp_text)
    whatsapp_link = f"https://wa.me/{whatsapp_number}?text={encoded_whatsapp_text}"

    # Отправляем итоговое сообщение пользователю
    bot.send_message(message.chat.id, final_message)
    bot.send_message(message.chat.id, "📩 Для оформления заказа нажмите сюда 👉 " + whatsapp_link)

    # Отправляем совет от профессионала
    tip_message = (
        "\n🎯 *Совет от профессионала по составлению резюме:*\n"
        "• Упоминайте только опыт и навыки, релевантные вакансии.\n"
        "• Используйте активные глаголы: достиг, разработал, улучшил.\n"
        "• Структурируйте информацию чётко: Опыт ➔ Образование ➔ Навыки.\n"
        "• Избегайте длинных описаний, делайте акцент на результатах.\n"
        "• Адаптируйте резюме под каждую вакансию.\n"
    )
    bot.send_message(message.chat.id, tip_message, parse_mode='Markdown')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    start_survey(message)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text in ["Да", "Нет"]:
        question_index = len(answers)  # Текущий индекс вопроса
        handle_answer(message, question_index)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, ответьте 'Да' или 'Нет'.")

# Запуск бота
bot.infinity_polling()
