import base64
carnet = GetVar('numero_documento')
b64str = ""+GetVar('token')+""
with open('{rutaPadre}descargas/segip_b64_'+carnet+'.pdf', 'wb') as pdf:
    pdf.write(base64.b64decode(b64str))
	
