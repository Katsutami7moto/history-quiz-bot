import logging

from environs import Env
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext
)

from quiz import get_random_question

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    quiz_buttons = [['Новый вопрос', 'Сдаться'], 
                    ['Мой счёт']]
    reply_markup = ReplyKeyboardMarkup(quiz_buttons)
    update.message.reply_text(
        'Привет! Я бот для викторин',
        reply_markup=reply_markup
    )


def send_new_question(update: Update, context: CallbackContext):
    question = get_random_question(
        context.bot_data.get('questions_dir')
    )
    update.message.reply_text(question[0])


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

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.INFO)

    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data.update(
        {
            'questions_dir': questions_dir,
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
