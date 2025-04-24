from bs4 import BeautifulSoup

from clients.stepik import StepikClient


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
