import re
from BeginState import BeginState
from ChooseTopicState import ChooseTopicState
from LlmApi import LlmApi
from QuestionState import QuestionState
from ResultState import ResultState


class User:
    def __init__(self, llm_api, id: int):
        self.__llm_api = LlmApi(llm_api)
        self.__id = id
        self.__is_active_questions = False
        self.__begin_state = BeginState()
        self.__choose_topic_state = ChooseTopicState()
        self.__questions_states = None
        self.__result_state = None
        self.__qw_response = ""
        self.__ev_response = ""
        self.__active_state = self.__begin_state
        self.__messages = []
        self.__answers = []

    def get_main_menu(self):
        return self.__begin_state.get_markup()

    def get_greetings(self):
        return self.__begin_state.get_text()

    def generate_topics(self, class_id: str):
        self.__choose_topic_state.generate_topics(class_id)

    def get_topics_menu(self):
        return self.__choose_topic_state.get_markup()

    def get_topics_text(self):
        return self.__choose_topic_state.get_text()

    async def generate_questions(self, topic: str):
        self.__is_active_questions = False
        self.__answers = []

        try:
            self.__qw_response = await self.__llm_api.get_questions(topic)
            questions = re.findall(r"\d+\.\s\*\*(.*?)\*\*", self.__qw_response)
            self.__questions_states = []

            if len(questions) > 0:
                self.__is_active_questions = True
                # self.__questions = questions

                for i in range(len(questions)):
                    self.__questions_states.append(QuestionState(questions[i], i))

        except Exception as e:
            print(f"Помилка генерування питання: {e}")

        return self.__is_active_questions


    def get_question(self):
        state = self.__questions_states.pop(0)

        if len(self.__questions_states) == 0:
            self.__is_active_questions = False

        return state.get_text()

    def add_to_answers(self, answer: str):
        self.__answers.append(answer)

    async def get_result(self):
        # if self.__result_state is None:
        try:
            estimate = await self.__llm_api.evaluate_answer(self.__qw_response, self.__answers)
            self.__result_state = ResultState(estimate, True)
        except Exception as e:
            self.__result_state = ResultState("Результату ще немає, можливо спробуйте ще раз")
            print(f"Помилка оцінки відповіді: {e}")

        return self.__result_state.get_text()

    @property
    def is_active_questions(self):  # Getter
        return self.__is_active_questions

    # def get_state(self):
    #     return
