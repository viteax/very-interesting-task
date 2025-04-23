from bs4 import BeautifulSoup

from clients.client import Client


def test_client():
    client = Client()
    lesson = client.get_lesson(id=265121)
    step = client.get_step(id=lesson.steps[-1])

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

    print(client.get_solution_code(step_id=lesson.steps[-1]))

    assert 1 == 1
