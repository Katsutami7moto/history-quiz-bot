import logging

from environs import Env
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    quiz_buttons = [['Новый вопрос', 'Сдаться'], 
                    ['Мой счёт']]
    reply_markup = ReplyKeyboardMarkup(quiz_buttons)
    update.message.reply_text(
        'Привет! Я бот для викторин',
        reply_markup=reply_markup
    )


def echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)


def main():
    env = Env()
    env.read_env()
    bot_token = env('TELEGRAM_BOT_TOKEN')

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.INFO)

    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo)
    )

    logger.info('Bot is running.')

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
