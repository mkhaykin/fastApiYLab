import random
import string


def random_word(length: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def round_price(price: str) -> str:
    return f'{round(float(price), 2):.2f}'


def compare_response(answer, standard: dict) -> bool:
    # assert answer.__dict__
    return all(key in answer and value == answer[key] for key, value in standard.items())


def compare_response_strict(answer, standard) -> bool:
    return answer == standard
