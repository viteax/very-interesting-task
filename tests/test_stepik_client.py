import pytest
from bs4 import BeautifulSoup

from clients.stepik import StepikClient


def test_get_lessons():
    stepik = StepikClient()
    lessons = stepik.get_lessons(
        course_id=58852,
        section_no=1,
    )

    assert [lesson.id for lesson in lessons] == [290248, 363342, 1086413, 1602702]


def test_get_lessons_ids_invalid():
    stepik = StepikClient()
    with pytest.raises(IndexError):
        stepik.get_lessons(
            course_id=58852,
            section_no=17,
        )


def test_client():
    stepik = StepikClient()
    lesson = stepik.get_lesson(id=265121)
    step = stepik.get_step(id=lesson.steps[-1])

    print()
    print(lesson)
    print()
    print(step)
    print()

    descr = step.block.text
    soup = BeautifulSoup(descr, "html.parser")
    # problem_name = soup.h2.text
    problem_descr = []
    for p in soup.find_all("p"):
        text: str = p.text
        if text.startswith("Формат входных данных"):
            break
        problem_descr.append(text)
    print(soup.h2.text)
    print(*problem_descr, sep="\n")

    print(stepik.get_solution_code(step_id=lesson.steps[-1]))

    assert 1 == 1
