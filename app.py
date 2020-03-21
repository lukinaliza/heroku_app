from flask import Flask, request, Response
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.pool import NullPool

from settings import TOKEN, WEBHOOK
from settings import HELLO_MESSAGE
from viberbot import Api
from settings import SAMPLE_KEYBOARD, START_KEYBOARD
from viberbot.api.messages import TextMessage, KeyboardMessage
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.viber_requests import ViberMessageRequest, ViberConversationStartedRequest
import random
import copy
import json
import sqlite3
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey

bot_configuration = BotConfiguration(
	name='Bot4',
	avatar='http://viber.com/avatar.jpg',
	auth_token=TOKEN
)
viber = Api(bot_configuration)
app = Flask(__name__)

engine = create_engine('postgres://uwtwamukjlaagw:7ccfda56ce5eb03e7d17e5988645061301a9d37da9e5e935e8e8d41c1bad0021@ec2-54-75-246-118.eu-west-1.compute.amazonaws.com:5432/d2jn4lvglieepl', poolclass=NullPool, echo = False)
# engine = create_engine('sqlite:///test.db', echo = False)
Base = declarative_base()
class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    examples = Column(String, nullable=False)

    var = relationship('User', back_populates = 'curword')

    def __repr__(self):
        return f'{self.id}. {self.word}: {self.translation} [{self.examples}]'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    full_name = Column(String, nullable=False, default='John Doe')
    viber_id = Column(String, nullable=False, unique=True)
    # currentword_id = Column(Integer, nullable=True)
    currentword_id = Column(Integer, ForeignKey('words.id'), nullable=True)
    correct_answers_session = Column(Integer, nullable=False, default=0)
    questionCount_session = Column(Integer, nullable=False, default=0)
    last_answer_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    time_reminder = Column(DateTime)

    words = relationship('Learning', back_populates='user')
    curword = relationship('Word', back_populates = 'var')
    def __repr__(self):
        return f'{self.id}: {self.full_name} [{self.viber_id}]'

class Learning(Base):
    __tablename__ = 'learning'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    word = Column(Integer, nullable=False)
    right_answers = Column(Integer, nullable=False, default=0)
    last_time_answer_word = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    user = relationship('User', back_populates='words')

    def __repr__(self):
        return f'{self.id}: {self.user_id} [{self.word} / {self.right_answers}] {self.last_time_answer_word}'

Session = sessionmaker(engine)

def initWords():
    session = Session()
    query = session.query(Word)
    if query.all().__len__() < 1:
        with open('english_words.json', encoding='utf-8') as f:
            english_words = json.load(f)
        for word in english_words:
            new_word = Word(word=word['word'], translation=word['translation'], examples = "".join(word['examples']))
            session.add(new_word)
    session.commit()
    session.close()


def get_four_words_for_user(user_id):
    session = Session()
    list = []
    dictSize = session.query(Word).all().__len__()
    while list.__len__() < 4:
        r = random.randint(1, dictSize)
        word = session.query(Word).filter(Word.id == r).first()
        check = session.query(Learning).filter(Learning.user_id == user_id).filter(Learning.word == word.id).first()
        if ((check == None or check.right_answers < 20) and word not in list):
            list.append(word)
    session.close()
    return list

def send_question(viber_request_sender_id, portion_words):
    session = Session()
    # заполнение клавиатуры
    user = session.query(User).filter(User.viber_id == viber_request_sender_id).first()
    curWord = portion_words[0]
    user.currentword_id = curWord.id
    user.last_answer_time = datetime.datetime.utcnow()
    session.commit()
    session.close()
    whichWordMessage = f'Как переводится слово {curWord.word}?'
    temp = copy.copy(portion_words)
    random.shuffle(temp)
    for button, w in zip(SAMPLE_KEYBOARD["Buttons"], temp):
        button["Text"] = w.translation
        button["ActionBody"] = w.translation
    messageKeyboard = KeyboardMessage(tracking_data='tracking_data', keyboard=SAMPLE_KEYBOARD)
    viber.send_messages(viber_request_sender_id, [
        TextMessage(text=whichWordMessage), messageKeyboard
    ])

def getStat(viber_id):
    session = Session()
    statistics = ""
    user = session.query(User).filter(User.viber_id == viber_id).first()
    wds_learnt = session.query(Learning).filter(Learning.user_id == user.id).filter(Learning.right_answers >=20).all().__len__()
    words_learning = session.query(Learning).filter(Learning.user_id == user.id).all().__len__() - wds_learnt
    statistics += "Количество выученных слов: " + str(wds_learnt) + "\n"
    statistics += "Количество слов на изучении: " + str(words_learning) + "\n"
    statistics += "Последнее посещение: " + str(user.last_answer_time).replace('-', '.')[:19]
    session.close()
    return statistics

def send_example(viber_id):
    session = Session()
    val = (session.query(Word).join(User).filter(User.viber_id == viber_id)).first().examples
    session.close()
    return val

def correct_answer(viber_id, text):
    session = Session()
    user = session.query(User).filter(User.viber_id == viber_id).first()
    if text == (session.query(Word).join(User).filter(Word.id == user.currentword_id)).first().translation:
        # обновление слова в таблице learning
        str = session.query(Learning).filter(Learning.user_id == user.id) \
            .filter(Learning.word == user.currentword_id).first()
        if (str != None):
            str.last_time_answer_word = datetime.datetime.utcnow()
            str.right_answers += 1
            session.commit()
        else:
            user.words.append(Learning(word=user.currentword_id, right_answers=1))
            session.commit()
        user.correct_answers_session += 1
        session.commit()
        viber.send_messages(viber_id, [TextMessage(text=f"Верно! :)")])
    else:
        viber.send_messages(viber_id, [TextMessage(text=f"Неверно! :(")])
    user.questionCount_session += 1
    # обновление последнего времени ответа
    user.last_answer_time = datetime.datetime.utcnow()
    session.commit()
    session.close()

def checkEndSession(viber_id):
    session = Session()
    user = session.query(User).filter(User.viber_id == viber_id).first()
    if user.questionCount_session >= SESSION_WORDS:
        final = TextMessage(text=f"Количество правильных ответов: {user.correct_answers_session} из {SESSION_WORDS}")
        viber.send_messages(viber_id, [final])
        user.correct_answers_session = 0
        user.questionCount_session = 0
        session.commit()
        session.close()
        return True
    session.close()
    return False

count = 0
@app.route("/")
def hello():
    global count
    count += 1
    return f"hello {count}"

mes_tokens = set()
portion_words = []
init = False
SESSION_WORDS = 5
TIME_INTERVAL = 5
@app.route('/incoming', methods = ['POST'])
def incoming():
    Base.metadata.create_all(engine)
    global init
    if (init == False):
        initWords()
        init = True
    global portion_words
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberConversationStartedRequest):
        session = Session()
        if (session.query(User).filter(User.viber_id == viber_request.user.id).first() == None):
            user_0 = User(full_name=viber_request.user.name, viber_id=viber_request.user.id)
            session.add(user_0)
            session.commit()
        viber.send_messages(viber_request.user.id, [
            TextMessage(text=HELLO_MESSAGE, keyboard=START_KEYBOARD, tracking_data='tracking_data')
        ])

    elif isinstance(viber_request, ViberMessageRequest):
        if viber_request.message_token not in mes_tokens:
            mes_token = viber_request.message_token
            mes_tokens.add(mes_token)
            message = viber_request.message
            session = Session()
            user = session.query(User).filter(User.viber_id == viber_request.sender.id).first()
            if isinstance(message, TextMessage):
                text = message.text
                print(text)
                if text == "Start":
                    stat = getStat(viber_request.sender.id)
                    user.time_reminder = datetime.datetime.utcnow() + datetime.timedelta(minutes=TIME_INTERVAL)
                    session.commit()
                    viber.send_messages(viber_request.sender.id, [TextMessage(text=stat)])
                    portion_words = get_four_words_for_user(user.id)
                    # заполнение клавиатуры
                    send_question(viber_request.sender.id, portion_words)
                elif text == "showExample":
                    resp = send_example(viber_request.sender.id)
                    viber.send_messages(viber_request.sender.id, [
                        TextMessage(text=resp)])
                    # заполнение клавиатуры
                    send_question(viber_request.sender.id, portion_words)
                elif text == "Later":
                    user.time_reminder = datetime.datetime.utcnow() + datetime.timedelta(minutes=TIME_INTERVAL)
                    session.commit()
                    viber.send_messages(viber_request.sender.id, [
                        TextMessage(text=f"Жду тебя! Нажми на Start как будешь готов"),
                        KeyboardMessage(tracking_data='tracking_data', keyboard=START_KEYBOARD)])
                else:
                    # проверка на правильность ответа
                    correct_answer(viber_request.sender.id, text)
                    if (checkEndSession(viber_request.sender.id)):
                        willContinue = TextMessage(text=f"Сыграем ещё раз?")
                        messageKeyboard = KeyboardMessage(tracking_data='tracking_data', keyboard=START_KEYBOARD)
                        viber.send_messages(viber_request.sender.id, [willContinue, messageKeyboard])
                    else:
                        portion_words = get_four_words_for_user(user.id)
                        # заполнение клавиатуры
                        send_question(viber_request.sender.id, portion_words)
            session.close()
        else:
            pass
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 82)
