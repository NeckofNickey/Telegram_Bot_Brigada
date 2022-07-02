from bs4 import BeautifulSoup
import requests
import random
from utilities import get_keyboard
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler


def sms(bot, update):
    """
    Функция sms будет вызвана пользователем при отправке команды start
    :param bot: экземпляр бота с помощью которого мы им управляем
    :param update: сообщение, которое пришло от Телеграм
    """
    print('Кто-то отправил команду /start. Что мне делать?')  # Сообщение при нажатии \start
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


def get_contact(bot, update):
    print(bot.message.contact)
    bot.message.reply_text(f'{bot.message.chat.first_name}, мы получили Ваш номер телефона.')


def get_location(bot, update):
    print(bot.message.location)
    bot.message.reply_text(f'{bot.message.chat.first_name}, мы получили Ваше местоположение.')


def anketa_start(bot, update):
    bot.message.reply_text('Как Вас зовут?', reply_markup=ReplyKeyboardRemove())
    return 'user_name'  # ключ для определения следующего шага


def anketa_get_name(bot, update):
    update.user_data['name'] = bot.message.text  # временно сохраняем ответ
    bot.message.reply_text('Сколько вам лет?')  # задаем вопрос
    return 'user_age'  # ключ для определения следующего шага


def anketa_get_age(bot, update):
    update.user_data['age'] = bot.message.text  # временно сохраняем ответ
    reply_keyboard = [['1', '2', '3', '4', '5']]  # создаем клавиатуру
    # reply_keyboard: 1 аргумент выводит на экран клавивтуру, 2 заставляет исчезнуть клавиатуру при нажатии
    bot.message.reply_text(
        'Оцените бота от 1 до 5',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True))
    return 'evaluation'  # ключ для определения следующего шага


def anketa_get_evaluation(bot, update):
    update.user_data['evaluation'] = bot.message.text  # временно сохраняем ответ
    reply_keyboard = [['Пропустить']]  # создаем клавиатуру
    bot.message.reply_text('Напишите отзыв или нажмите кнопку пропустить этот шаг.',
                           reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                              resize_keyboard=True, one_time_keyboard=True))
    return 'comment'  # ключ для определения следующего шага


def anketa_comment(bot, update):
    update.user_data['comment'] = bot.message.text  # временно сохраняем ответ
    text = """Результат опроса:
    <b>Имя:</b> {name}
    <b>Возраст:</b> {age}
    <b>Оценка:</b> {evaluation}
    <b>Комментарий:</b> {comment}
    """.format(**update.user_data)
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)  # текстовое сообщение с форматирование HTML
    bot.message.reply_text('Спасибо Вам за комментарий!', reply_markup=get_keyboard())  # возвращает основ. клаву
    return ConversationHandler.END


def anketa_exit_comment(bot, update):
    update.user_data['comment'] = bot.message.text  # временно сохраняем ответ
    text = """Результат опроса:
    <b>Имя:</b> {name}
    <b>Возраст:</b> {age}
    <b>Оценка:</b> {evaluation}
    """.format(**update.user_data)
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)  # текстовое сообщение с форматирование HTML
    bot.message.reply_text('Спасибо!', reply_markup=get_keyboard())  # возвращает основ. клаву
    return ConversationHandler.END


def dontknow(bot, update):
    bot.message.reply_text('Я вас не понимаю, выберите оценку на клавиатуре!')
