import os

from clients.word import WordClient
from logic import IMGS_PATH, get_code_solutions

TEMPLATE_PATH = "assets/template.docx"


def main():
    os.makedirs(IMGS_PATH, exist_ok=True)

    doc = WordClient(doc_name=TEMPLATE_PATH)

    lesson_id = input("Введите id урока: ")
    current_no = int(input("Начать с номера: "))
    doc_name = input("Сохранить как: ")

    code_solutions = get_code_solutions(lesson_id=lesson_id)
    for solution in code_solutions:
        doc.add_solution(
            no=current_no,
            title=solution.title,
            descr="\n".join(solution.description),
            pic_path=solution.pic_path,
        )
        current_no += 1

    doc.save(doc_name=doc_name)


if __name__ == "__main__":
    main()
