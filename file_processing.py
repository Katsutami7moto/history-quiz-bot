def check_only_quiz(text: str) -> bool:
    is_question = 'Вопрос' in text
    is_answer = 'Ответ' in text
    return is_question or is_answer


def get_question(text: str) -> str:
    return '\n'.join([x for x in text.split('\n') if x][1:])


def get_answer(text: str) -> str:
    return '\n'.join(text.split('\n')[1:])


def get_structured_quiz(filename: str) -> dict:
    with open(file=filename, mode='r', encoding='koi8-r') as file:
        file_contents = file.read()
    qna = tuple(filter(check_only_quiz, file_contents.split('\n\n')))
    questions = tuple(map(get_question, qna[::2]))
    answers = tuple(map(get_answer, qna[1::2]))
    return dict(zip(questions, answers))
