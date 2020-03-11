from settings import TOKEN
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import TextMessage
from lab6 import START_KEYBOARD, Session, User
import datetime

bot_configuration = BotConfiguration(
    name='EnglishBotPro',
    avatar='http://viber.com/avatar.jpg',
    auth_token=TOKEN
)
viber = Api(bot_configuration)

# словарь соответствий пользователя и времени последнего напоминания
users_reminders = {}

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    session = Session()
    users = session.query(User)
    for u in users:
        if datetime.datetime.utcnow() - u.last_answer_time > datetime.timedelta(minutes=5):
            if ((u not in users_reminders) or (
                    datetime.datetime.utcnow() - users_reminders[u] > datetime.timedelta(minutes=3))):
                users_reminders[u] = datetime.datetime.utcnow()
                viber.send_messages(u.viber_id, [TextMessage(text="Время повторить слова", keyboard=START_KEYBOARD,
                                                             tracking_data='tracking_data')])


sched.start()