import os


def get_quiz(dirname: str) -> dict:
    quiz = dict()
    for root, _, files in os.walk(dirname):
        for file in files:
            with open(
                file=os.path.join(root, file),
                mode='r',
                encoding='koi8-r'
            ) as file:
                file_contents = file.read()
            qna = tuple(
                text
                for text in file_contents.split('\n\n')
                if 'Вопрос' in text or 'Ответ' in text
            )
            questions = tuple(
                '\n'.join([x for x in text.split('\n') if x][1:])
                for text in qna[::2]
            )
            answers = tuple(
                '\n'.join(text.split('\n')[1:])
                for text in qna[1::2]
            )
            quiz.update(dict(zip(questions, answers)))
    return quiz
