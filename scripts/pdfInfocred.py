import base64
carnet = GetVar('titularDocumento')
b64str = ""+GetVar('tokenInfocred')+""
with open('{rutaPadre}descargas/ENCRIPTADO_'+carnet+'.pdf', 'wb') as pdf:
    pdf.write(base64.b64decode(b64str))
