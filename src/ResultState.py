from src.BeginState import main_menu
from src.State import State
import re
from src.configs.configs import POSITIVE_RANGE, GOOD_RANGE, EMAIL, EMAIL_PASS
from src.mail_sender import send_email


class ResultState(State):
    def __init__(self, user_id, result, is_estimated=False):
        self.__user_id = user_id
        self.__res = result
        self.__is_estimated = is_estimated

    def get_text(self):
        resp = self.__res
        if self.__is_estimated:
            positive_count = len(re.findall(r"Позитивно", resp, re.IGNORECASE))
            good_count = len(re.findall(r"Задовільно", resp, re.IGNORECASE))
            negative_count = len(re.findall(r"Негативно", resp, re.IGNORECASE))

            mark = round(positive_count * POSITIVE_RANGE + good_count * GOOD_RANGE)

            self.__res += f"\n Позитивно - {positive_count}; Задовільно - {good_count}; Негативно - {negative_count}; \n ОЦІНКА: {mark}"
        return self.__res

    def get_markup(self):
        return main_menu

    async def report_result(self):
        await send_email(EMAIL, EMAIL_PASS, EMAIL, "Result", f"id: {self.__user_id} ;\n{self.__res}")
