import base64
rutaCpop = GetVar("rutaCpop")
with open(""+rutaCpop"+", "wb") as pdf_file:
    encoded_string = base64.b64encode(pdf_file.read())
SetVar('documento',encoded_string)