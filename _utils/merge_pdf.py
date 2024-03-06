from PyPDF2 import PdfWriter, PdfReader, PdfMerger
from io import BytesIO


def merge_pdfs(template, binary_overlay):

    with open(template, "rb") as file:
        template = file.read()
    template_pdf = PdfReader(BytesIO(template))
    overlay_pdf = PdfReader(BytesIO(binary_overlay))

    template_pdf.pages[0].merge_page(overlay_pdf.pages[0])

    finished_pdf = PdfWriter()
    finished_pdf.add_page(template_pdf.pages[0])

    binary_result = BytesIO()
    finished_pdf.write(binary_result)
    binary_result.seek(0)
    finished_pdf.close()
    return binary_result.read()


def combine_pdf_pages(pdf_pages):
    merger = PdfMerger()
    for page in pdf_pages:
        new_page = PdfReader(BytesIO(page["content"]))
        merger.append(new_page)

    binary_result = BytesIO()
    merger.write(binary_result)
    binary_result.seek(0)
    merger.close()
    return binary_result.read()