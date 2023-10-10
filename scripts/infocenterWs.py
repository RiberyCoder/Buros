import requests
ws_INFOCENTER = GetVar('ws_INFOCENTER')
url = ''+ws_INFOCENTER+''
xmlConsulta = GetVar('xmlConsultaIcenter')
motivo = GetVar('motivoIcenter')
tipoPersona = GetVar('tipoPersonaIcenter')
tipoReporte = GetVar('tipoReporteIcenter')
perror = GetVar('perrorIcenter')
mensaje = GetVar('mensajeIcenter')
prueba = GetVar('pruebaIcenter')

headers = {"Host":"21.10.0.75", "Content-Type":"text/xml; charset=utf-8", "SOAPAction":"http://tempuri.org/F8000_ConsultarInfocenter",'accept-encoding':'gzip,deflate'}
body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <F8000_ConsultarInfocenter xmlns="http://tempuri.org/">
      <xmlConsulta>"""+xmlConsulta+"""</xmlConsulta>
      <motivo>"""+motivo+"""</motivo>
      <tipoPersona>"""+tipoPersona+"""</tipoPersona>
      <tipoReporte>"""+tipoReporte+"""</tipoReporte>
      <perror>"""+perror+"""</perror>
      <mensaje>"""+mensaje+"""</mensaje>
      <prueba>"""+prueba+"""</prueba>
    </F8000_ConsultarInfocenter>
  </soap:Body>
</soap:Envelope>"""

response = requests.post(url,data=body,headers=headers,verify=False)
#print response.content
print(response.content)
SetVar('datos',response.content)