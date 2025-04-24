import os

from clients.stepik import StepikClient
from clients.word import WordClient
from logic import IMGS_PATH, get_code_solutions

TEMPLATE_PATH = "assets/template.docx"
PYTHON_COURSE_ID = 58852


def main():
    os.makedirs(IMGS_PATH, exist_ok=True)

    doc = WordClient(doc_path=TEMPLATE_PATH)
    stepik = StepikClient()

    course_id = int(input("Введите id курса: ") or PYTHON_COURSE_ID)
    section_no = int(input("Введите номер раздела: "))

    section = stepik.get_section(stepik.get_section_id(course_id, section_no))
    doc_name = input("Сохранить как: ") or f"{section_no}-{section.title}"

    current_no = 1
    heading_no = 1

    lessons = stepik.get_lessons(course_id, section_no)
    for lesson in lessons:
        code_solutions = get_code_solutions(lesson_id=lesson.id)
        if not code_solutions:
            continue
        doc.add_heading2(lesson.title, heading_no=heading_no)
        for solution in code_solutions:
            doc.add_solution(
                no=current_no,
                title=solution.title,
                descr="\n".join(solution.description),
                img_path=solution.img_path,
            )
            current_no += 1
        doc.add_page_break()
        heading_no += 1

    doc.save(doc_name=doc_name)


if __name__ == "__main__":
    main()
