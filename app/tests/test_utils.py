import random
import string


def random_word(length: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def round_price(price: str) -> str:
    return f'{round(float(price), 2):.2f}'


def compare_response(answer: dict, expected_answer: dict) -> bool:
    return all(key in answer and value == answer[key] for key, value in expected_answer.items())


def compare_response_strict(answer: dict, expected_answer: dict) -> bool:
    return answer == expected_answer


def dict_in_list(_dict: dict, _list: list) -> bool:
    """
    Проверяет, что словарь _dict присутствует в списке _list.
    Проверка не строгая, т.е. элемент списка может быть иметь больше ключей, чем словарь.
    :param _dict:
    :param _list:
    :return:
    """
    return any(compare_response(item, _dict) for item in _list)
