from BeginState import main_menu
from State import State
import re
from configs.configs import POSITIVE_RANGE, GOOD_RANGE


class ResultState(State):
    def __init__(self, result, is_estimated=False):
        self.__res = result
        self.__is_estimated = is_estimated

    def get_text(self):
        resp = self.__res
        if self.__is_estimated:
            positive_count = len(re.findall(r"Позитивно", resp, re.IGNORECASE))
            good_count = len(re.findall(r"Задовільно", resp, re.IGNORECASE))
            negative_count = len(re.findall(r"Негативно", resp, re.IGNORECASE))

            mark = round(positive_count * POSITIVE_RANGE + good_count * GOOD_RANGE)

            resp += f"\n Позитивно - {positive_count}; Задовільно - {good_count}; Негативно - {negative_count}; \n ОЦІНКА: {mark}"
        return resp

    def get_markup(self):
        return main_menu
