from setting import TG_TOKEN
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import *


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
    my_bot.dispatcher.add_handler(
        ConversationHandler(entry_points=[MessageHandler(Filters.regex('Заполнить анкету'), anketa_start)],
                            states={
                                    'user_name': [MessageHandler(Filters.text, anketa_get_name)],
                                    'user_age': [MessageHandler(Filters.text, anketa_get_age)],
                                    'evaluation': [MessageHandler(Filters.regex('1|2|3|4|5'), anketa_get_evaluation)],
                                    'comment': [MessageHandler(Filters.regex('Пропустить'), anketa_exit_comment),
                                                MessageHandler(Filters.text, anketa_comment)]
                                    },
                            fallbacks=[MessageHandler(
                                                      Filters.text | Filters.video | Filters.photo |
                                                      Filters.document, dontknow)])
                            )
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))

    my_bot.start_polling()  # проверяет наличие сообщений из Телеграм
    my_bot.idle()  # бот будет работать пока его не остановят


if __name__ == '__main__':
    main()
