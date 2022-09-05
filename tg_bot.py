import logging

from environs import Env
from redis import Redis
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext,
    ConversationHandler
)

from quiz import get_random_question

logger = logging.getLogger(__name__)

CHOOSING, ANSWERING = range(2)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Привет! Я бот для викторин',
        reply_markup=context.bot_data.get('quiz_buttons')
    )

    return CHOOSING


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

    return ANSWERING


def handle_answer(update: Update, context: CallbackContext):
    current_answer: str = context.bot_data.get('current_answer')
    attempt = update.message.text
    if attempt == current_answer.split('.')[0].split('(')[0]:
        msg = 'Правильно! Для следующего вопроса нажми «Новый вопрос»'
        context.bot_data.update(
            {
                'current_question': '',
                'current_answer': '',
            }
        )
        state = CHOOSING
    else:
        msg = 'Неправильно… Попробуешь ещё раз?'
        state = ANSWERING
    update.message.reply_text(msg)
    return state


def handle_giving_up(update: Update, context: CallbackContext):
    current_answer: str = context.bot_data.get('current_answer')
    update.message.reply_text(f'Правильный ответ:\n{current_answer}')
    
    return CHOOSING


def show_user_score(update: Update, context: CallbackContext):
    pass


def handle_wrong_command(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Пожалуйста, выберите действие из меню'
    )

    return CHOOSING


def main():
    env = Env()
    env.read_env()
    bot_token: str = env('TELEGRAM_BOT_TOKEN')
    questions_dir: str = env('QUESTIONS_DIR')
    db_address: str = env('DB_ADDRESS')
    db_port: int = env.int('DB_PORT')
    db_username: str = env('DB_USERNAME')
    db_password: str = env('DB_PASSWORD')

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

    quiz_buttons = ReplyKeyboardMarkup([
        ['Новый вопрос', 'Сдаться'],
        ['Мой счёт']
    ])

    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data.update(
        {
            'questions_dir': questions_dir,
            'db_connection': db_connection,
            'quiz_buttons': quiz_buttons,
            'current_question': '',
            'current_answer': '',
        }
    )
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex(
                        '^Новый вопрос$'
                    ),
                    send_new_question
                ),
                MessageHandler(
                    Filters.regex(
                        '^Мой счёт$'
                    ),
                    show_user_score
                )
            ],
            ANSWERING: [
                MessageHandler(
                    Filters.text & ~Filters.command & ~Filters.regex(
                        '^Сдаться$'
                    ),
                    handle_answer
                ),
                MessageHandler(
                    Filters.regex(
                        '^Сдаться$'
                    ),
                    handle_giving_up
                )
            ]
        },
        fallbacks=[
            MessageHandler(
                Filters.text & ~Filters.command,
                handle_wrong_command
            )
        ]
    )
    dispatcher.add_handler(conv_handler)

    logger.info('Bot is running.')

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
