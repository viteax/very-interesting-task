from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

from clients.stepik import StepikClient
from models.stepik import CodeProblem, CodeSolution

PADDING = 20
FONT_SIZE = 24
PICS_PATH = "images"
FONT_PATH = "assets/JetBrainsMono-Regular.ttf"


def save_code_picture(pic_path: str, code_str: str) -> None:
    """Saves picture"""

    img = Image.new("RGB", (500, 500))
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

    img = Image.new(
        "RGB", (line_length + PADDING, line_height + PADDING), (255, 255, 255)
    )
    d = ImageDraw.Draw(img)

    d.text(
        (PADDING, PADDING),
        code_str,
        fill=(0, 0, 0),
        font=font,
    )
    img.save(pic_path, "PNG")


def parse_block_text(html_text: str) -> CodeProblem:
    soup = BeautifulSoup(html_text, "html.parser")
    problem_title: str = soup.h2.text
    problem_descriptions = []
    for p in soup.find_all("p"):
        text: str = p.text
        if text.startswith("Формат входных данных"):
            break
        problem_descriptions.append(text.replace("\xa0", " "))

    problem_title = problem_title.replace("\xa0", " ")
    return CodeProblem(title=problem_title, description=problem_descriptions)


def get_code_solutions(lesson_id: int) -> list[CodeSolution]:
    client = StepikClient()

    lesson = client.get_lesson(id=lesson_id)
    code_solutions = []
    for step_id in lesson.steps:
        step = client.get_step(id=step_id)
        if step.block.name == "code":
            code_problem = parse_block_text(step.block.text)
            code_str = client.get_solution_code(step_id=step_id)
            path_to_pic = f"{PICS_PATH}/{code_problem.title}.png"
            save_code_picture(pic_path=path_to_pic, code_str=code_str)
            code_solutions.append(
                CodeSolution(
                    title=code_problem.title,
                    description=code_problem.description,
                    pic_path=path_to_pic,
                )
            )

    return code_solutions


if __name__ == "__main__":
    code_solutions = get_code_solutions(lesson_id=265122)
    print(*code_solutions, sep="\n\n")
    print(len(code_solutions))
