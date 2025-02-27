from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.State import State
from src.configs.configs import TOPICS_SCHEME

MESSAGE = "Оберіть тему:"


class ChooseTopicState(State):
    def __init__(self):
        self.__menu = None

    def get_text(self):
        return MESSAGE

    def get_markup(self):
        return self.__menu

    def generate_topics(self, class_id: str):
        topics = TOPICS_SCHEME[class_id]
        sorted_topics = [topics[i: i + 2] for i in range(0, len(topics), 2)]
        self.__menu = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=topic) for topic in arr] for arr in sorted_topics],
            resize_keyboard=True,
            one_time_keyboard=True
        )
