from telegram import ReplyKeyboardMarkup, KeyboardButton


def get_keyboard():
    """
    Функция создает клавиатуру и ее разметку
    """
    contact_button = KeyboardButton('Отправить контакты', request_contact=True)
    location_button = KeyboardButton('Отправить геопозицию', request_location=True)

    my_keyboard = ReplyKeyboardMarkup([['Цитата', 'Начать'],
                                       [contact_button, location_button],
                                       ['Заполнить анкету']
                                       ], resize_keyboard=True)
    return my_keyboard
