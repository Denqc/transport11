import telebot
import sqlite3
from telebot import types

TOKEN = "8882777311:AAGLJU-j927Xjrbj69NuHvbW9tM-w9qr9Cw"
bot = telebot.TeleBot(TOKEN)

# Главное меню (Inline кнопки)
keyboard = types.InlineKeyboardMarkup(row_width=2)
BPMN_button = types.InlineKeyboardButton('Диаграмма BPMN', callback_data='bpmn')
dashboard_button = types.InlineKeyboardButton('Дашборд', callback_data='dashboard')
help_button = types.InlineKeyboardButton('Помощь', callback_data='help')
order_button = types.InlineKeyboardButton('Оформить заказ', callback_data='order')
keyboard.add(BPMN_button, help_button, dashboard_button, order_button)

# ==================== ОБРАБОТЧИКИ КОМАНД ====================

@bot.message_handler(commands=['creator'])
def creator(message):
    bot.reply_to(message, 'Денис 4ВТБА-1')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        'Привет! Этот бот обрабатывает заказы для транспортной компании.\n'
        'Отправьте /help, чтобы узнать доступные команды. Автор /creator'
    )

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

# ==================== ОБРАБОТЧИКИ КНОПОК (ФУНКЦИИ МЕНЮ) ====================

def BPMN_but(message):
    bpmn_markup = types.InlineKeyboardMarkup(row_width=1)
    button9 = types.InlineKeyboardButton('Описание BPMN', callback_data='bpmn_function1')
    button10 = types.InlineKeyboardButton('Ссылка на диаграмму', callback_data='bpmn_function2')
    bpmn_markup.add(button9, button10)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=bpmn_markup)

def Dashboard_but(message):
    dashboard_markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('Описание дашборда', callback_data='dashboard_function1')
    button2 = types.InlineKeyboardButton('Ссылка на GitHub', callback_data='dashboard_function2')
    dashboard_markup.add(button1, button2)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=dashboard_markup)

def Help_but(message):
    help_markup = types.InlineKeyboardMarkup(row_width=1)
    button15 = types.InlineKeyboardButton('Как пользоваться ботом', callback_data='help_function1')
    button16 = types.InlineKeyboardButton('Контакты поддержки', callback_data='help_function2')
    help_markup.add(button15, button16)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=help_markup)

def Order_but(message):
    order_handler(message)

# ==================== СЛОВАРИ ДЛЯ КАЛЛБЭКОВ ====================

CALLBACK_D = {
    "Диаграмма BPMN": BPMN_but,
    "Дашборд": Dashboard_but,
    "Помощь": Help_but,
    "Оформить заказ": Order_but
}

CALLBACK_D_BUTTON = {
    "bpmn": BPMN_but,
    "dashboard": Dashboard_but,
    "help": Help_but,
    "order": Order_but,
}

# ==================== ОБРАБОТЧИК ТЕКСТОВЫХ СООБЩЕНИЙ ====================

@bot.message_handler(func=lambda message: True)
def home_screen(message):
    if message.text in CALLBACK_D:
        CALLBACK_D[message.text](message)
    else:
        bot.reply_to(message, 'Не понимаю /help', reply_markup=keyboard)

# ==================== ОФОРМЛЕНИЕ ЗАКАЗА ====================

def order_handler(message):
    bot.send_message(message.chat.id, 'Давайте начнем оформление заказа. Введите ваше имя:')
    bot.register_next_step_handler(message, enter_sender_name)

def enter_sender_name(message):
    order = {}
    order['sender_name'] = message.text
    bot.send_message(message.chat.id, f'Отлично, {message.text}! Теперь укажите место отправки груза:')
    bot.register_next_step_handler(message, enter_pickup_location, order)

def enter_pickup_location(message, order):
    order['pickup_location'] = message.text
    bot.send_message(message.chat.id, f'Место подачи груза: {message.text}. Теперь введите пункт назначения:')
    bot.register_next_step_handler(message, enter_destination, order)

def enter_destination(message, order):
    order['destination'] = message.text
    bot.send_message(message.chat.id, f'Пункт назначения: {message.text}. Заказ оформлен!')

    # Отчёт по заказу
    report = f'Отчет по заказу:\n\n' \
             f'Имя отправителя: {order["sender_name"]}\n' \
             f'Место подачи груза: {order["pickup_location"]}\n' \
             f'Пункт назначения: {order["destination"]}\n'

    bot.send_message(message.chat.id, report)

    # Сохранение в SQLite
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_name TEXT,
            pickup_location TEXT,
            destination TEXT
        )
    ''')

    cursor.execute('''
        INSERT INTO orders (sender_name, pickup_location, destination)
        VALUES (?, ?, ?)
    ''', (order['sender_name'], order['pickup_location'], order['destination']))
    conn.commit()
    conn.close()

# ==================== ОБРАБОТЧИК ИНЛАЙН-КНОПОК (CALLBACK) ====================

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data in CALLBACK_D_BUTTON:
        CALLBACK_D_BUTTON[call.data](call.message)

    # ---------- BPMN ----------
    elif call.data == 'bpmn_function1':
        bot.send_message(
            call.message.chat.id,
            'Диаграммы BPMN (Business Process Model and Notation) представляют собой стандартный '
            'графический язык, разработанный для моделирования бизнес-процессов в организации. '
            'Этот инструмент обеспечивает единый и понятный способ визуализации бизнес-процессов, '
            'что помогает более эффективно понимать, анализировать и оптимизировать деятельность компании.'
        )

        bpmn_function_markup = types.InlineKeyboardMarkup(row_width=1)
        button11 = types.InlineKeyboardButton(
            'Как телеграм бот может помочь в процессе обработки заказов для транспортной компании',
            callback_data='bpmn_function3'
        )
        button12 = types.InlineKeyboardButton('Изображение BPMN схемы', callback_data='bpmn_function4')
        bpmn_function_markup.add(button11, button12)
        bot.send_message(call.message.chat.id, 'Выберите действие:', reply_markup=bpmn_function_markup)

    elif call.data == 'bpmn_function2':
        bot.send_message(
            call.message.chat.id,
            'Ссылка на диаграмму: https://lucid.app/users/registerOrLogin/free?showLogin=false&invitationId=inv_'
            'cbccaf51-8132-410a-ac55-685a8529e396&productOpt=chart&invitationType=documentAcceptance&returnUrlOverride='
            '%2Flucidchart%2Fd0a8d047-4837-4c88-afad-50bf218fd1c8%2Fedit%3Fviewport_loc%3D-836%252C-242%252C3700%252C1817'
            '%252CtFvMj0YbrJai%26invitationId%3Dinv_cbccaf51-8132-410a-ac55-685a8529e396'
        )

    elif call.data == 'bpmn_function3':
        bot.send_message(
            call.message.chat.id,
            'Телеграм-бот может значительно упростить и ускорить процесс обработки заказов для транспортной компании.\n'
            'Вот несколько способов, как он может быть полезен:\n'
            'Получение заказов: Клиенты могут отправлять заказы через бота, '
            'указывая необходимую информацию, такую как место погрузки, место назначения, тип груза и другие детали.\n'
            'Интеграция с платежными системами: Для удобства клиентов бот может интегрироваться с '
            'платежными системами, позволяя им оплачивать услуги напрямую через телеграм.\n'
            'Обратная связь и поддержка: Клиенты могут общаться с ботом для задания вопросов, '
            'уточнения деталей заказа или предоставления обратной связи.'
        )

    elif call.data == 'bpmn_function4':
        # Замените на вашу реальную ссылку на изображение BPMN, если она есть
        image7_url = 'https://raw.githubusercontent.com/vladislawwwwww/TelegramBotRgr/development/bpmn.jpg'
        bot.send_photo(call.message.chat.id, image7_url, caption='Это схема BPMN')

    # ---------- ДАШБОРД ----------
    elif call.data == 'dashboard':
        dashboard_markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton('Описание дашборда', callback_data='dashboard_function1')
        button2 = types.InlineKeyboardButton('Ссылка на GitHub', callback_data='dashboard_function2')
        dashboard_markup.add(button1, button2)
        bot.send_message(call.message.chat.id, 'Выберите действие:', reply_markup=dashboard_markup)

    elif call.data == 'dashboard_function1':
        bot.send_message(
            call.message.chat.id,
            'Дашборд предназначен для визуализации и анализа данных о здоровье и медицинских показателях.\n'
            'Содержит пять ключевых графиков, предоставляющих информацию о различных аспектах пациентского здоровья.'
        )

        dashboard_function_markup = types.InlineKeyboardMarkup(row_width=2)
        button3 = types.InlineKeyboardButton('График 1', callback_data='dashboard_function3')
        button4 = types.InlineKeyboardButton('График 2', callback_data='dashboard_function4')
        button5 = types.InlineKeyboardButton('График 3', callback_data='dashboard_function5')
        button6 = types.InlineKeyboardButton('График 4', callback_data='dashboard_function6')
        button7 = types.InlineKeyboardButton('График 5', callback_data='dashboard_function7')
        button8 = types.InlineKeyboardButton('Таблица', callback_data='dashboard_function8')
        dashboard_function_markup.add(button3, button4, button5, button6, button7, button8)
        bot.send_message(call.message.chat.id, 'Выберите график:', reply_markup=dashboard_function_markup)

    elif call.data == 'dashboard_function2':
        # ИСПРАВЛЕННАЯ ССЫЛКА НА ВАШ РЕПОЗИТОРИЙ
        bot.send_message(call.message.chat.id, 'Ссылка на GitHub: https://github.com/Denqc/transport1')

    elif call.data == 'dashboard_function3':
        # Замените на ваши реальные ссылки на изображения графиков, если они есть
        image1_url = 'https://raw.githubusercontent.com/vladislawwwwww/TelegramBotRgr/development/graphik1.jpg'
        bot.send_photo(call.message.chat.id, image1_url, caption='Это точечный график')

    elif call.data == 'dashboard_function4':
        image2_url = 'https://raw.githubusercontent.com/vladislawwwwww/TelegramBotRgr/development/graphik2.jpg'
        bot.send_photo(call.message.chat.id, image2_url, caption='Это столбчатый график')

    elif call.data == 'dashboard_function5':
        image3_url = 'https://raw.githubusercontent.com/vladislawwwwww/TelegramBotRgr/development/graphik3.jpg'
        bot.send_photo(call.message.chat.id, image3_url, caption='Это круговой график')

    elif call.data == 'dashboard_function6':
        image4_url = 'https://raw.githubusercontent.com/vladislawwwwww/TelegramBotRgr/development/graphik4.jpg'
        bot.send_photo(call.message.chat.id, image4_url, caption='Это линейный график')

    elif call.data == 'dashboard_function7':
        image5_url = 'https://raw.githubusercontent.com/vladislawwwwww/TelegramBotRgr/development/graphik5.jpg'
        bot.send_photo(call.message.chat.id, image5_url, caption='Это ящичковый график')

    elif call.data == 'dashboard_function8':
        image6_url = 'https://raw.githubusercontent.com/vladislawwwwww/TelegramBotRgr/development/table1.jpg'
        bot.send_photo(call.message.chat.id, image6_url, caption='Это таблица')

    # ---------- ПОМОЩЬ ----------
    elif call.data == 'help_function1':
        bot.send_message(
            call.message.chat.id,
            'Как пользоваться ботом:\n\n'
            '1. Нажмите "Оформить заказ" — введите имя, место отправки и пункт назначения.\n'
            '2. Нажмите "Диаграмма BPMN" — получите описание, ссылку и изображение схемы.\n'
            '3. Нажмите "Дашборд" — получите описание, ссылку на GitHub и графики.\n'
            '4. Если что-то непонятно — нажмите "Помощь".'
        )

    elif call.data == 'help_function2':
        bot.send_message(
            call.message.chat.id,
            'Контакты поддержки:\n\n'
            '📧 Email: support@transport-company.ru\n'
            '📞 Телефон: 8-800-123-45-67\n'
            '✈️ Telegram: @transport_support_bot'
        )

# ==================== ЗАПУСК БОТА ====================

if __name__ == '__main__':
    print('🤖 Бот запущен...')
    bot.infinity_polling()
