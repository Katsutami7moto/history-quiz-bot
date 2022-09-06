import logging

from environs import Env

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

logger = logging.getLogger(__name__)


def get_keyboard():
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()


def echo(event, vk):
    vk.messages.send(
        peer_id=event.user_id,
        message=event.text,
        random_id=get_random_id(),
        keyboard=get_keyboard()
    )


def main():
    env = Env()
    env.read_env()
    vk_club_token = env('VK_CLUB_TOKEN')

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    vk_session = vk_api.VkApi(token=vk_club_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.info('Bot is running.')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk)


if __name__ == '__main__':
    main()
