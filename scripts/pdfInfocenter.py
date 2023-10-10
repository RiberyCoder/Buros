import base64
carnet = GetVar('numeroDocumentoIcenter')
b64str = ""+GetVar('token')+""
with open('{rutaPadre}descargas/INFOCENTER'+"_"+carnet+'.pdf', 'wb') as pdf:
    pdf.write(base64.b64decode(b64str))