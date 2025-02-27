from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from State import State
from configs import TOPICS_SCHEME

MESSAGE = "Оберіть тему:"


class ChooseTopicState(State):
    def get_text(self):
        return MESSAGE

    def get_markup(self):
        return self._menu

    def generate_topics(self, class_id: str):
        topics = TOPICS_SCHEME[class_id]
        sorted_topics = [topics[i: i + 2] for i in range(0, len(topics), 2)]
        self._menu = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=topic) for topic in arr] for arr in sorted_topics],
            resize_keyboard=True,
            one_time_keyboard=True
        )
