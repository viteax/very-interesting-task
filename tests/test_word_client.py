from clients.word import WordClient
from main import TEMPLATE_PATH


def test_headings():
    doc = WordClient(doc_path=TEMPLATE_PATH)
    doc.add_heading2("Купи слона", heading_no=1)
    doc.add_page_break()
    doc.add_heading2("Делай деньги", heading_no=2)
    doc.save("temp.docx")
    assert doc
