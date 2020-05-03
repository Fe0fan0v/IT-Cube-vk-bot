import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from working_table import Table
from datetime import datetime

t = Table('1eOHupW8CiZ9bJn0D7DQVjX1nDHssO97y05DhyXpBHxc')


def create_main_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Расписание', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Закрыть', color=VkKeyboardColor.DEFAULT)
    return keyboard.get_keyboard()


def create_schedule_keyboard():
    keyboard = VkKeyboard(one_time=False)
    buttons = 0
    for subject in t.data.keys():
        if buttons == 3:
            keyboard.add_line()
            buttons = 0
        keyboard.add_button(subject[:40], color=VkKeyboardColor.POSITIVE)
        buttons += 1
    keyboard.add_line()
    keyboard.add_button('Главное меню', color=VkKeyboardColor.DEFAULT)
    return keyboard.get_keyboard()


def close_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard.get_empty_keyboard()
    return keyboard


def greeting(time):
    if 5 < time.hour < 12:
        return 'Доброе утро'
    elif 12 < time.hour < 17:
        return 'Добрый день'
    elif 17 < time.hour < 24:
        return 'Добрый вечер'
    else:
        return 'Доброй ночи'


def main():
    vk_session = vk_api.VkApi(token='7134ec534a2db42ab0f89995ff9d70322962a332aa0629077663f16a828435f466c18e42e9f4ed6e7cddc')
    longpoll = VkBotLongPoll(vk_session, '182910816')
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.obj['message']
            print('Новое входящее сообщение:')
            print(message['text'])
            user_id = message['from_id']
            if message['text'].lower() == 'привет':
                user_name = vk_session.method('users.get', {'user_id': user_id})[0]['first_name']
                user_surname = vk_session.method('users.get', {'user_id': user_id})[0]['last_name']
                time = datetime.now()
                vk.messages.send(
                    user_id=user_id,
                    random_id=get_random_id(),
                    message=f'{greeting(time)}, {user_name} {user_surname}',
                    keyboard=create_main_keyboard()
                )
            elif message['text'].lower() == 'закрыть':
                vk.messages.send(
                    user_id=user_id,
                    random_id=get_random_id(),
                    message=f'Всего хорошего!',
                    keyboard=close_keyboard()
                )
            elif message['text'].lower() == 'расписание':
                vk.messages.send(
                    user_id=user_id,
                    random_id=get_random_id(),
                    message=f'Расписание',
                    keyboard=create_schedule_keyboard()
                )
            elif message['text'] in list(t.data):
                vk.messages.send(
                    user_id=user_id,
                    random_id=get_random_id(),
                    message='\n'.join(t.data[message['text']])
                )
                print(t.data[message['text']])
            elif message['text'].lower() == 'главное меню':
                vk.messages.send(
                    user_id=user_id,
                    random_id=get_random_id(),
                    message=f'Ещё что-нибудь?',
                    keyboard=create_main_keyboard()
                )
        else:
            print(event.type)


if __name__ == '__main__':
    main()
