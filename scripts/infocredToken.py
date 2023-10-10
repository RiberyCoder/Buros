from lxml import etree
file=GetVar('rutaInfocred')
doc = etree.parse(file)
raiz=doc.getroot()
token = raiz.findtext("reportePdfBase64")
SetVar('tokenInfocred',token)
print(token)