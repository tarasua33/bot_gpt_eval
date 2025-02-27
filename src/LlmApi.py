from src.configs.configs import BASE_QUESTIONS_NUMBER, TOPICS_DESCRIPTOR


class LlmApi:
    def __init__(self, connection):
        self.__connection = connection
        self.__last_user_content = ""

    async def get_questions(self, topic: str):
        topics = TOPICS_DESCRIPTOR[topic]
        self.__last_user_content = f"Згенеруй {BASE_QUESTIONS_NUMBER} запитань на теми {topics}. Не добавляй відповіді. Виділи початок кожного питання символами **"
        messages = [
            {"role": "system",
             "content": "Ти є TR_Estimation-GPT оцінювачем успішності студентів на основі вивченої теми. Чат генерує кількість запитань яку вказує користувач. Питання повинні бути відкриті. Для Відповіді студентів достатньо 1 речення."},
            {"role": "user",
             "content": self.__last_user_content}
        ]

        response = await self.__connection.chat.completions.create(
            model="sonar",
            messages=messages,
            temperature=0.35
        )

        content = response.choices[0].message.content

        return content

    async def evaluate_answer(self, questions: str, answers: [str]):
        answers_input = "User: Ось мої відповіді: \n"

        for idx, ans in enumerate(answers, start=1):
            answers_input += f"Відповідь {idx}: {ans} \n"
        messages_st2 = [
            {"role": "system", "content": """Ти є TR_Estimation-GPT оцінювачем успішності студентів на основі вивченої теми. Чат генерує питання, Після відповіді студентів на всі питання, TR_Estimation-GPT оцінює ці відповіді як позитивну, задовільну або негативну. Якщо відповідь повна правильна - оцінка позитивна. Якщо відповідь частково правильна - оцінка задовільна. Питання повинні бути відкриті. Для Відповіді студентів достатньо 1 речення/
                Приклад питань, відповідей та оцінок:
                TR_Estimation-GPT: Питання:
                1. ** З чого складається атом? **
                2. ** Яка швидкість світла у вакуумі? **
                3. ** Які види відновлювальних джерел енергії? **
                
                User: Ось мої відповіді:
                Відповідь 1: Протони електрони нейтрони
                Відповідь 2: 300 кілометрів
                Відповідь 3: вареники, сметана
                
                TR_Estimation-GPT: Оцінки на питання:
                Питання 1: Оцінка **Позитивно**
                Питання 2: Оцінка **Позитивно**
                Питання 3: Оцінка **Негативно**
                """},
            {"role": "user",
             "content": self.__last_user_content},
            {"role": "assistant", "content": questions},
            {"role": "user", "content": f"{answers_input}"}
        ]

        response = await self.__connection.chat.completions.create(
            model="sonar",
            messages=messages_st2
            #   response_format={
            # "type": "json_schema",
            #       "json_schema": {"schema": AnswerFormat.model_json_schema()},
            #   }
        )

        return response.choices[0].message.content

