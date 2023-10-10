from fpdf import FPDF

archivoNetbank = GetVar("archivoNetbank")
fichero = open("{rutaPadre}descargas/"+archivoNetbank+".txt","r")
pdf = FPDF(orientation='P')
pdf.add_page()
pdf.set_font("COURIER",size=6)
line=1

for linea in fichero:
    pdf.cell(100,3,txt=linea,ln=line)
    
pdf.output("{rutaPadre}descargas/"+archivoNetbank+".pdf")
fichero.close()

