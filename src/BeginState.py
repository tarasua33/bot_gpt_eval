from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from State import State
from configs import class_9, class_8, class_7

GREETING_MESSAGE = "Вітаю! Виберіть одну з опцій:"


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=class_9)],
        [KeyboardButton(text=class_8)],
        [KeyboardButton(text=class_7)]
    ],
    resize_keyboard=True
)


class BeginState(State):
    def get_text(self):
        return GREETING_MESSAGE

    def get_markup(self):
        return main_menu
