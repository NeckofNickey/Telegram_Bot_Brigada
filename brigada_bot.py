from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from setting import TG_TOKEN


# Подключаемся к Телеграм
def main():
    # Переменная my_bot обеспечивает взаимодействие с ботом. В аругментах: токен от BotFather
    my_bot = Updater(TG_TOKEN, use_context=True)

    # dispatcher принимает от Телеграм входящее сообщение
    # add_handler передает его в обработчик CommandHandler
    # CommandHandler реагирует на определенные события и вызовет функции sms при нажатии на \start
    my_bot.dispatcher.add_handler(CommandHandler('start', sms))

    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))  # обрабатывает текстовые сообщения

    my_bot.start_polling()  # проверяет наличие сообщений из Телеграм
    my_bot.idle()  # бот будет работать пока его не остановят


def sms(bot, update):
    """
    Функция sms будет вызвана пользователем при отправке команды start
    :param bot: экземпляр бота с помощью которого мы им управляем
    :param update: сообщение, которое пришло от Телеграм
    """
    print('Кто-то отправил команду /start. Что мне делать?')  # Сообщение при нажатии \start
    bot.message.reply_text(f'Здравствуйте {bot.message.chat.first_name}, я бот! '
                           f'\nЯ пока не умею разговаривать, но я быстро учусь!')  # ответ
    print(bot.message)


def parrot(bot, update):
    """
    Функция отвечает тем же сообщением, которое ему прислали
    :param bot: экземпляр бота с помощью которого мы им управляем
    :param update: сообщение, которое пришло от Телеграм
    """
    print(bot.message.text)  # печатаем на экран сообщение пользователя
    bot.message.reply_text(bot.message.text)  # отправляем сообщение обратно пользователю


main()
