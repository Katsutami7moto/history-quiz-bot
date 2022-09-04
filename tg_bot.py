import logging

from environs import Env
from redis import Redis
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext
)

from quiz import get_random_question

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    quiz_buttons = [
        ['Новый вопрос', 'Сдаться'], 
        ['Мой счёт']
    ]
    reply_markup = ReplyKeyboardMarkup(quiz_buttons)
    update.message.reply_text(
        'Привет! Я бот для викторин',
        reply_markup=reply_markup
    )


def send_new_question(update: Update, context: CallbackContext):
    question = get_random_question(
        context.bot_data.get('questions_dir')
    )
    context.bot_data.update(
        {
            'current_question': question[0],
            'current_answer': question[1],
        }
    )
    db_connection: Redis = context.bot_data.get('db_connection')
    db_connection.set(update.effective_user.id, question[0])
    update.message.reply_text(db_connection.get(update.effective_user.id))


def handle_answer(update: Update, context: CallbackContext, answer: str):
    current_answer: str = context.bot_data.get('current_answer')
    if answer == current_answer.split('.')[0].split('(')[0]:
        msg = 'Правильно! Для следующего вопроса нажми «Новый вопрос»'
        context.bot_data.update(
        {
            'current_question': '',
            'current_answer': '',
        }
    )
    else:
        msg = 'Неправильно… Попробуешь ещё раз?'
    update.message.reply_text(msg)


def handle_giving_up(update: Update, context: CallbackContext):
    pass


def show_user_score(update: Update, context: CallbackContext):
    pass


def handle_menu_actions(update: Update, context: CallbackContext):
    menu_actions = {
        'Новый вопрос': send_new_question,
        'Сдаться': handle_giving_up,
        'Мой счёт': show_user_score,
    }
    action_text = update.message.text

    if action_text in menu_actions:
        action = menu_actions[action_text]
        action(update, context)
    elif context.bot_data.get('current_question'):
        handle_answer(update, context, action_text)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Пожалуйста, выберите действие из меню'
        )


def main():
    env = Env()
    env.read_env()
    bot_token = env('TELEGRAM_BOT_TOKEN')
    questions_dir = env('QUESTIONS_DIR')
    db_address = env('DB_ADDRESS')
    db_port = env.int('DB_PORT')
    db_username = env('DB_USERNAME')
    db_password = env('DB_PASSWORD')

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.INFO)

    db_connection = Redis(
        host=db_address,
        port=db_port,
        username=db_username,
        password=db_password,
        decode_responses=True
    )

    if db_connection.ping():
        logger.info('Redis DB is connected.')
    else:
        logger.warn('Redis DB is not connected')

    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data.update(
        {
            'questions_dir': questions_dir,
            'db_connection': db_connection,
            'current_question': '',
            'current_answer': '',
        }
    )
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        MessageHandler(Filters.text, handle_menu_actions)
    )

    logger.info('Bot is running.')

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
