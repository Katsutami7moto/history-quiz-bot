import logging
import random

from environs import Env

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

logger = logging.getLogger(__name__)


def echo(event, vk_api_method):
    vk_api_method.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
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
    vk_api_method = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.info('Bot is running.')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api_method)


if __name__ == '__main__':
    main()
