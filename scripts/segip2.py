#from suds.client import Client
import requests
ws_SEGIP = GetVar('ws_SEGIP')
#url = 'https://wsconsultarui.segip.gob.bo/ServicioExternoInstitucion.svc?wsdl'
url = ''+ws_SEGIP+''

idinst = GetVar('codigo_institucion')
usuario = GetVar('user')
password = GetVar('pass')
clavefin = GetVar('clave_final')
numaut = GetVar('numero_autorizacion')
numdoc = GetVar('numero_documento')
numdoc = numdoc.replace("LP", "").replace("SC", "").replace("CB", "").replace("PD", "").replace("BE", "").replace("OR", "").replace("PO", "").replace("CH", "").replace("TJ", "")
complemento=GetVar('complemento')

headers = {'content-type': 'text/xml;charset=UTF-8','content-length':'<calculated when request is sent>','SOAPAction':'"http://tempuri.org/IServicioExternoInstitucion/ConsultaDatoPersonaCertificacion"','accept-encoding':'gzip,deflate'}
body = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
                <soapenv:Header/>
                <soapenv:Body>
                <tem:ConsultaDatoPersonaCertificacion>
                <tem:pCodigoInstitucion>"""+idinst+"""</tem:pCodigoInstitucion>
                <tem:pUsuario>"""+usuario+"""</tem:pUsuario>
                <tem:pContrasenia>"""+password+"""</tem:pContrasenia>
                <tem:pClaveAccesoUsuarioFinal>"""+clavefin+"""</tem:pClaveAccesoUsuarioFinal>
                <tem:pNumeroAutorizacion>"""+numaut+"""</tem:pNumeroAutorizacion>
                <tem:pNumeroDocumento>"""+numdoc+"""</tem:pNumeroDocumento>
                <tem:pComplemento>"""+complemento+"""</tem:pComplemento>
                <tem:pNombre xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                <tem:pPrimerApellido xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" />
                <tem:pSegundoApellido xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" />
                <tem:pFechaNacimiento xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" />
                </tem:ConsultaDatoPersonaCertificacion>
                </soapenv:Body>
</soapenv:Envelope>"""
response = requests.post(url,data=body,headers=headers)
print (response.content)
SetVar('data',response.content)
#<tem:pComplemento xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" />