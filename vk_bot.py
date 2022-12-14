import logging
import random

from environs import Env
from redis import Redis
from vk_api import VkApi
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

from quiz import get_quiz

logger = logging.getLogger(__name__)


def send_new_question(uid, db_connection: Redis, _quiz):
    question, answer = random.choice(tuple(_quiz.items()))
    db_connection.set(f'{uid}_current_question', question)
    db_connection.set(f'{uid}_current_answer', answer)
    return question


def handle_answer(uid, db_connection: Redis, attempt):
    current_answer: str = db_connection.get(f'{uid}_current_answer')
    if attempt == current_answer.split('.')[0].split('(')[0]:
        db_connection.set(f'{uid}_current_question', '')
        db_connection.set(f'{uid}_current_answer', '')
        return 'Правильно! Для следующего вопроса нажми «Новый вопрос»'
    return 'Неправильно… Попробуешь ещё раз?'


def handle_giving_up(uid, db_connection: Redis):
    current_answer: str = db_connection.get(f'{uid}_current_answer')
    db_connection.set(f'{uid}_current_question', '')
    db_connection.set(f'{uid}_current_answer', '')

    if current_answer:
        return f'Правильный ответ:\n{current_answer}'
    return 'Вы не получили вопрос.'


def show_user_score():
    return 'Ведение счёта в разработке'


def get_message(uid, request, db_connection: Redis, _quiz):
    current_question = db_connection.get(f'{uid}_current_question')

    if request == 'Новый вопрос':
        return send_new_question(uid, db_connection, _quiz)
    if request == 'Сдаться':
        return handle_giving_up(uid, db_connection)
    if request == 'Мой счёт':
        return show_user_score()
    if current_question:
        return handle_answer(uid, db_connection, request)
    return 'Пожалуйста, выберите действие из меню'


def main():
    env = Env()
    env.read_env()
    vk_club_token = env('VK_CLUB_TOKEN')
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
        logger.error('Redis DB is not connected.')
        exit(1)

    keyboard = VkKeyboard()
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.SECONDARY)

    _quiz = get_quiz(questions_dir)

    vk_session = VkApi(token=vk_club_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.info('Bot is running.')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            uid = event.user_id
            request = event.text
            _message = get_message(
                uid, request, db_connection, _quiz
            )
            vk.messages.send(
                peer_id=uid,
                message=_message,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )


if __name__ == '__main__':
    main()
