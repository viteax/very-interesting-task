from PIL import Image

from logic import PICS_PATH, parse_block_text, save_code_picture


def test_save_picture():
    pic_path = f"{PICS_PATH}/test.png"

    save_code_picture(pic_path=pic_path, code_str="lmao")
    img = Image.open(pic_path)

    assert img


def test_parse_block_text():
    html_text = (
        "<h2>Заголовок</h2>\n<p>Доброе утро, мальчик</p>\n  <p>Как ты поживаешь?</p>"
    )
    ans = ["Доброе утро, мальчик", "Как ты поживаешь?"]

    code_problem = parse_block_text(html_text=html_text)

    assert code_problem.description == ans
