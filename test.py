from datetime import datetime


def greeting(time):
    if 5 < time.hour < 12:
        return 'Доброе утро'
    elif 12 < time.hour < 17:
        return 'Добрый день'
    elif 17 < time.hour < 24:
        return 'Добрый вечер'
    else:
        return 'Доброй ночи'


print(greeting(datetime.now()))

