from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


class WordClient:
    def __init__(self, doc_name: str):
        self.doc_name = doc_name
        self.doc = Document(docx=doc_name)

    def add_solution(self, no: int, title: str, descr: str, img_path: str) -> None:
        self.doc.add_paragraph(f'"{title}"')
        self.doc.add_paragraph(f"{descr}")
        self.doc.add_paragraph()

        pic_p = self.doc.add_paragraph()
        pic_p.add_run().add_picture(img_path)
        pic_p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        label = self.doc.add_paragraph(f'Рисунок 2.{no} — решение задачи "{title}".')
        label.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        self.doc.add_paragraph()

    def save(self, doc_name: str) -> None:
        self.doc.save(doc_name)
