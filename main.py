import os

from clients.stepik import StepikClient
from clients.word import WordClient
from logic import IMGS_PATH, get_code_solutions

TEMPLATE_PATH = "assets/template.docx"


def main():
    os.makedirs(IMGS_PATH, exist_ok=True)

    doc = WordClient(doc_path=TEMPLATE_PATH)
    stepik = StepikClient()

    course_id = int(input("Введите id курса: "))
    section_no = int(input("Введите номер секции: "))
    current_no = int(input("Начать нумерацию с: "))
    doc_name = input("Сохранить как: ")

    lessons = stepik.get_lessons(course_id, section_no)
    for heading_no, lesson in enumerate(lessons):
        doc.add_heading2(lesson.title, heading_no=heading_no)
        code_solutions = get_code_solutions(lesson_id=lesson.id)
        for solution in code_solutions:
            doc.add_solution(
                no=current_no,
                title=solution.title,
                descr="\n".join(solution.description),
                img_path=solution.img_path,
            )
            current_no += 1
        doc.add_page_break()

    doc.save(doc_name=doc_name)


if __name__ == "__main__":
    main()
