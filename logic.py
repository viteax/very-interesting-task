import logging

from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

from clients.stepik import StepikClient
from models.stepik import CodeProblem, CodeSolution, Lesson

PADDING = 0
FONT_SIZE = 64
FONT_PATH = "assets/JetBrainsMono-Regular.ttf"
IMGS_PATH = "images"

logger = logging.getLogger(__name__)


def save_code_picture(img_path: str, code_str: str) -> None:
    """Saves picture"""

    img = Image.new("RGB", (1, 1), (255, 255, 255))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    code_str = code_str.strip()
    box_size = d.textbbox(
        (PADDING, PADDING),
        code_str,
        font=font,
    )
    line_length = box_size[2]
    line_height = box_size[3]

    img = img.resize((line_length + PADDING, line_height + PADDING))
    d = ImageDraw.Draw(img)
    d.text(
        (PADDING, PADDING),
        code_str,
        fill=(0, 0, 0),
        font=font,
    )
    img.save(img_path, "PNG")


def parse_block_text(html_text: str) -> CodeProblem | None:
    soup = BeautifulSoup(html_text, "html.parser")
    if not soup.h2:
        return None

    problem_title: str = soup.h2.text
    problem_descriptions = []
    for p in soup.find_all("p"):
        text: str = p.text
        if text.startswith("Формат входных данных"):
            break
        problem_descriptions.append(text.replace("\xa0", " "))

    problem_title = problem_title.replace("\xa0", " ")
    return CodeProblem(title=problem_title, description=problem_descriptions)


def legalize_title(title: str) -> str:
    return "".join(
        symb
        for symb in title
        if symb not in ("\\", "/", ":", "*", "?", '"', "<", ">", "|")
    )


def get_code_solutions(lesson: Lesson) -> list[CodeSolution]:
    logger.info(f"Getting code solutions «{lesson.title}»\n")
    stepik = StepikClient()

    code_solutions = []
    for step_id in lesson.steps:
        step = stepik.get_step(id=step_id)
        if step.block.name != "code":
            continue

        code_problem = parse_block_text(step.block.text)
        if not code_problem:
            continue

        code_str = stepik.get_solution_code(step_id=step_id)
        if not code_str:
            continue

        title = legalize_title(code_problem.title)
        img_path = f"{IMGS_PATH}/{title}.png"

        save_code_picture(img_path, code_str)
        code_solutions.append(
            CodeSolution(
                title=code_problem.title,
                description=code_problem.description,
                img_path=img_path,
            )
        )
    return code_solutions


if __name__ == "__main__":
    code_solutions = get_code_solutions(lesson_id=265122)
    print(*code_solutions, sep="\n\n")
    print(len(code_solutions))
