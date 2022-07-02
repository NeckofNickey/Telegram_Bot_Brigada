from setting import TG_TOKEN
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
from bs4 import BeautifulSoup
import requests
import random


# Подключаемся к Телеграм
def main():
    # Переменная my_bot обеспечивает взаимодействие с ботом. В аругментах: токен от BotFather
    my_bot = Updater(TG_TOKEN, use_context=True)

    # dispatcher принимает от Телеграм входящее сообщение
    # add_handler передает его в обработчик CommandHandler
    # CommandHandler реагирует на определенные события и вызовет функции sms при нажатии на \start
    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Цитата'), get_quote))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_contact))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.location, get_location))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))

    my_bot.start_polling()  # проверяет наличие сообщений из Телеграм
    my_bot.idle()  # бот будет работать пока его не остановят


def sms(bot, update):
    """
    Функция sms будет вызвана пользователем при отправке команды start
    :param bot: экземпляр бота с помощью которого мы им управляем
    :param update: сообщение, которое пришло от Телеграм
    """
    print('Кто-то отправил команду /start. Что мне делать?')  # Сообщение при нажатии \start
    # my_keyboard = ReplyKeyboardMarkup([['Цитата', 'Начать']], resize_keyboard=True)
    bot.message.reply_text(f'Здравствуйте, {bot.message.chat.first_name}! '
                           f'\nЯ бот, который выдает цитаты из лучшего сериала во вселенной "Бригада"!'
                           f'\nПросто нажми на кнопку "Цитата"!',
                           reply_markup=get_keyboard())  # ответ
    print(bot.message)


def parrot(bot, update):
    """
    Функция отвечает тем же сообщением, которое ему прислали

    """
    print(bot.message.text)  # печатаем на экран сообщение пользователя
    bot.message.reply_text(bot.message.text)  # отправляем сообщение обратно пользователю


def get_quote(bot, update):
    """
    Функция выдает пользователю цитату с сайта  при нажатии на кнопку "Цитата"

    """
    # отправляем запрос к странице
    receive = requests.get('https://citatnica.ru/citaty/tsitaty-iz-seriala-brigada-310-tsitat')
    page = BeautifulSoup(receive.text, 'html.parser')  # подключаем html парсер, получаем текст страницы
    find = page.select('.su-note')  # из страницы html получаем class="su-note"
    counter = 0
    random_number = random.randint(0, len(find))  # выбираем случайное число для выдачи случайной цитаты
    for text in find:
        page = (text.getText().strip())  # из class="su-note" получает текст и убираем пробелы по краям
        counter += 1
        if counter == random_number:
            break
    bot.message.reply_text(page)  # отправляем одну случайную цитату


def get_keyboard():
    """
    Функция создает клавиатуру и ее разметку
    """
    contact_button = KeyboardButton('Отправить контакты', request_contact=True)
    location_button = KeyboardButton('Отправить геопозицию', request_location=True)

    my_keyboard = ReplyKeyboardMarkup([['Цитата', 'Начать'],
                                       [contact_button, location_button]], resize_keyboard=True)
    return my_keyboard


def get_contact(bot, update):
    print(bot.message.contact)
    bot.message.reply_text(f'{bot.message.chat.first_name}, мы получили Ваш номер телефона.')


def get_location(bot, update):
    print(bot.message.location)
    bot.message.reply_text(f'{bot.message.chat.first_name}, мы получили Ваше местоположение.')


main()
