from _utils.delunit import DelUnit
from _utils.sort_to_walk import sort_to_walk
from _utils.make_map import make_map
from _utils.merge_pdf import combine_pdf_pages, merge_pdfs
import fpdf

# Stores delinquent units and creates delinquency documents
class DelUnits:

    def __init__(self):
        self.del_units = []
        self.ntv_pdfs = []
        self.master_file_name = "Master_Delinquency_File.pdf"

    
    def get_delinquency(self, delinquency, property_name, curr_date, due_date):
        self.store_delinquency_data(delinquency, property_name)
        self.sort()
        self.get_map()
        self.write_ntv_pdfs(curr_date, due_date)
        return self.ntv_pdfs


    def store_delinquency_data(self, delinquency, property_name):

        delinquency = delinquency.splitlines()
        for line in delinquency:
            line = line.split("\t")

            if line[0] != property_name:              
                break
            name = line[3]                    

            if line[4] == "Guarantor" or line[4] == "": 
                self.del_units[-1].add_guarantor(name)      
                continue

            if line[4] == "Responsible":                            
                self.del_units[-1].add_occupant(name)
                continue               

            unit_number = int(line[1])                                 
            balance = line[11]
            self.del_units.append(DelUnit(name, unit_number, balance))   


    def sort(self):
        sorted_units = sort_to_walk([x.unit_number for x in self.del_units])
        for unit in self.del_units:
            sorted_units[sorted_units.index(unit.unit_number)] = unit
        self.del_units = sorted_units


    def get_map(self):
        map = make_map([x.unit_number for x in self.del_units])
        self.ntv_pdfs.append(map)


    def write_ntv_pdfs(self, curr_date, due_date):

        template = "api/static/assets/pdf_templates/delinquency_template.pdf"

        for unit in self.del_units:
            finished_file = f"3_Day_NTV_{unit.unit_number}{unit.initials}.pdf"

            pdf = fpdf.FPDF(format = "letter", unit = "pt")
            pdf.add_page()
            pdf.set_font("Arial", style = "B", size = 7.9)
            pdf.set_text_color(255, 0, 0)

            pdf.set_xy(68, 158)
            pdf.cell(0, txt = unit.occupants)
            pdf.set_xy(426, 158)
            pdf.cell(0, txt = curr_date)
            pdf.set_xy(404, 187)
            pdf.cell(0, txt = unit.guarantor)

            pdf.set_font("Arial", style = "", size = 7.9)
            pdf.set_text_color(0, 0, 0)
            pdf.set_xy(68, 187)
            pdf.cell(0, txt = unit.address)

            pdf.set_font("Arial", style = "B", size = 10)
            pdf.set_text_color(255, 0, 0)
            pdf.set_xy(49, 274)
            pdf.cell(0, txt = unit.balance_in_words)

            pdf.set_font("Arial", style = "", size = 8.9)
            pdf.set_text_color(0, 0, 0)
            pdf.set_xy(328, 288)
            pdf.cell(0, txt = unit.address)

            pdf.set_font("Arial", style = "B", size = 10)
            pdf.set_text_color(255, 0, 0)
            pdf.set_xy(150, 338)
            pdf.cell(0, txt = due_date)

            binary_overlay = pdf.output(dest="S").encode("latin1")
            binary_result = merge_pdfs(template, binary_overlay)
            self.ntv_pdfs.append({"title": finished_file, "content": binary_result})

        binary_master = combine_pdf_pages(self.ntv_pdfs)
        self.ntv_pdfs.append({"title": self.master_file_name, "content": binary_master})