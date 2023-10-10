import base64
usuario = GetVar('userinfocenter')
tipoPersona = GetVar('consultaTipoPersona')
codDocumento = GetVar('consultaCodDocumento')
tipoDocumento = GetVar('consultaTipoDocumento')
numeroDocumentoIcenter = GetVar('numeroDocumentoIcenter')

data=""
if tipoPersona == 'N':
    complemento = GetVar('consultaComplemento')
    extension = GetVar('consultaExtension')
    nombre1 = GetVar('consultaNombre1')
    nombre2 = GetVar('consultaNombre2')
    apPaterno = GetVar('consultaApPaterno')
    apMaterno = GetVar('consultaApMaterno')
    apCasada = GetVar('consultaApCasada')
    data="""<![CDATA[<CONSULTAS><CONSULTA><COD_DOCUMENTO>"""+codDocumento+"""</COD_DOCUMENTO><COMPLEMENTO>"""+complemento+"""</COMPLEMENTO><TIPO_DOCUMENTO>"""+tipoDocumento+"""</TIPO_DOCUMENTO><EXTENSION>"""+extension+"""</EXTENSION><NOMBRE1>"""+nombre1+"""</NOMBRE1><NOMBRE2>"""+nombre2+"""</NOMBRE2><AP_PATERNO>"""+apPaterno+"""</AP_PATERNO><AP_MATERNO>"""+apMaterno+"""</AP_MATERNO><AP_CASADA>"""+apCasada+"""</AP_CASADA><RAZON_SOCIAL/><NOMBRE_COMERCIAL/></CONSULTA></CONSULTAS>]]>"""
#data=data.encode("UTF-8")
#result=base64.b64encode(data)
SetVar('xmlConsultaIcenter',data)
print(data)