from State import State

# def text_wrapper_execution(func):
#
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#
#         return f"Дайте відповідь на це питання: {result}"
#
#     return wrapper


class QuestionState(State):
    def __init__(self, qw, idx):
        # super().__init__()
        self.__qw = qw
        self.__idx = idx

    # @text_wrapper_execution
    def get_text(self):
        return f"Дайте відповідь на це питання N{self.__idx + 1}: {self.__qw}"
