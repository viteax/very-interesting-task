from clients.word_client import WordClient
from logic import get_code_solutions


def main():
    doc = WordClient(doc_name="assets/temp.docx")

    lesson_id = input("Введите id урока: ")
    current_no = int(input("Начать с номера: "))

    code_solutions = get_code_solutions(lesson_id=lesson_id)
    for solution in code_solutions:
        doc.add_solution(
            no=current_no,
            title=solution.title,
            descr="\n".join(solution.description),
            pic_path=solution.path_to_pic,
        )
        current_no += 1

    doc.save()


if __name__ == "__main__":
    main()
