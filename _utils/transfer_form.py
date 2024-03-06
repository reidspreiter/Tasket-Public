import fpdf
from _utils.merge_pdf import merge_pdfs

def create_transfer_form(name, unit, move_out, fee, res_num):
    template = "api/static/assets/pdf_templates/transfer_form_template.pdf"
    title = f"Relet Form {unit}{name.split()[0]}{name.split()[1]}.pdf"

    pdf = fpdf.FPDF(format = "letter", unit = "pt")
    pdf.add_page()

    pdf.set_font("Arial", style = "", size = 10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(69, 408)
    pdf.cell(0, txt = name)
    pdf.set_xy(69, 453)
    pdf.cell(0, txt = move_out)
    pdf.set_xy(69, 499)
    pdf.cell(0, txt = res_num)
    pdf.set_xy(358, 408)
    pdf.cell(0, txt = unit)
    pdf.set_xy(358, 453)
    pdf.cell(0, txt = fee)

    binary_overlay = pdf.output(dest="S").encode("latin1")
    binary_result = merge_pdfs(template, binary_overlay)
    return {"title": title, "content": binary_result}