import requests
import json
import os
from base64 import b64decode
from datetime import datetime


try:
    netbank_user=GetVar ('ws_netbank_user')
    netbank_pass=GetVar ('ws_netbank_pass')
    authenticate=GetVar ('ws_authenticate')
    ConsultaCliente=GetVar ('ws_ConsultaCliente')
    ImpresionHojaRiesgo=GetVar ('ws_ImpresionHojaRiesgo')
    ci_cliente=GetVar('paraCarnet')
    url = authenticate
    payload = json.dumps({"Username": netbank_user,"Password": netbank_pass})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    #SetVar('response_robot',response.text)
    oauth_consumer_key = response.text.replace('"','') 
    url = ConsultaCliente
    payload = json.dumps(ci_cliente)
    headers = {
    'Authorization': 'Bearer {0}'.format(oauth_consumer_key),
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload,verify=False)
    #deudas=response.text
    #deudas=deudas.split('"numero":')
    deudas=json.loads(response.text)
    #SetVar('response_robot',deudas)
    print(deudas)
    #if not os.path.exists('c:/test/'+str(ci_cliente)):
    #    os.mkdir('c:/test/'+str(ci_cliente))
    url = ImpresionHojaRiesgo
    contador_vigentes=0
    contador_total=0
    deudas_array=[]
    for deuda in deudas:
            print(str(deuda['numero']) + " " + str(deuda['estado']))
            contador_total=contador_total+1
            deudas_array.append(deuda['numero'])
            if deuda['estado'] == "VIGENTE":
                contador_vigentes=contador_vigentes+1 
                payload = json.dumps({'NumeroPrestamo': deuda['numero'],  'TipoImpresion': 2})
                headers = {'Authorization': 'Bearer {0}'.format(oauth_consumer_key),'Content-Type': 'application/json'}
                response = requests.request("POST", url, headers=headers, data=payload,verify=False)
                print (response)
                print (response.text)
                if str(response) != "<Response [500]>":
                    pdf=json.loads(response.text)
                    b64 = (pdf['PDF'])
                    bytes = b64decode(b64, validate=True)
                    if bytes[0:4] != b'%PDF':
                        raise ValueError('Missing the PDF file signature')
                    f = open('D:/AD/BUROS/descargas/{0}_{1}.pdf'.format(ci_cliente,str(deuda['relacion'])+"_Hoja_de_Riesgo_"+str(deuda['numero'])), 'wb')
                    f.write(bytes)
                    f.close()
    print (str(deudas_array))
    print (str(contador_total))
    print (str(contador_vigentes))
    SetVar('contador_total',contador_total)
    SetVar('contador_vigentes',contador_vigentes)
    if contador_vigentes==0 and contador_total>0:
        no_vigente=max(deudas_array)
        print (str(no_vigente))
        payload = json.dumps({'NumeroPrestamo': no_vigente,  'TipoImpresion': 2})
        headers = {'Authorization': 'Bearer {0}'.format(oauth_consumer_key),'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print (response)
        print (response.text)
        if str(response) != "<Response [500]>":
            pdf=json.loads(response.text)
            b64 = (pdf['PDF'])
            bytes = b64decode(b64, validate=True)
            if bytes[0:4] != b'%PDF':
                raise ValueError('Missing the PDF file signature')
            f = open('D:/AD/BUROS/descargas/{0}_{1}.pdf'.format(ci_cliente,str(deuda['relacion'])+"_Hoja_de_Riesgo_"+str(no_vigente)), 'wb')
            f.write(bytes)
            f.close()
    if contador_vigentes==0 and contador_total==0:
        now = datetime.now() 
        fecha=now.strftime("%m-%d-%Y")
        hora=now.strftime("%H:%M:%S")
        from fpdf import FPDF   
        pdf = FPDF('P', 'mm', 'Letter')
        leftmargin = 1.5
        rightmargin = 1.5
        topmargin = 1.5
        pdf.set_margins(leftmargin, topmargin, rightmargin)
        pdf.set_auto_page_break(False)
        pdf.add_page()
        pdf.set_font('Courier', '', 6)
        cuerpo1="PRESTAMOS                                                 BANCO PYME ECOFUTURO S.A.                                           PAGINA: 1:       "
        cuerpo2="{0}                                                        HOJA DE RIESGO                                                FECHA :{1}".format(fecha,hora)
        cuerpo3="TDR:10:10                                                      NUMERO :{0}                                                                 ".format(ci_cliente)
        cuerpo4="-----------------------------------------------------------------------------------------------------------------------------------------------"
        cuerpo5="                                CLIENTE NO REGISTRADO EN LA BASE DE CREDITOS DEL BANCO                                                         "
        cuerpo6="    E**OBSERVACIONES Y/O COMENTARIOS AL CLIENTE** F M                                                                                          "
        cuerpo7="-----------------------------------------------------------------------------------------------------------------------------------------------"
        cuerpo8="**FIN REPORTE pr106.r **                                                                                                                       "
        cuerpo9="                   ** ESTE INFORME ESTA SUJETO AL *SECRETO BANCARIO* CONFORME A LA LEY DE BANCOS Y ENTIDADES FINANCIERAS **                    "
        cuerpo0="                                       ** DEUDA SISTEMA FINANCIERO ACTUALIZABLE CADA 15 DE CADA MES **                                         "
        pdf.cell(w=0,h=10, txt=cuerpo1, border=2,  align='C', fill=0)
        pdf.ln(5)
        pdf.cell(w=0,h=10, txt=cuerpo2, border=2,  align='C', fill=0)
        pdf.ln(5)
        pdf.cell(w=0,h=10, txt=cuerpo3, border=2,  align='C', fill=0)
        pdf.ln(5)
        pdf.cell(w=0,h=10, txt=cuerpo4, border=2,  align='C', fill=0)
        pdf.ln(5)
        pdf.cell(w=0,h=10, txt=cuerpo5, border=2,  align='C', fill=0)
        pdf.ln(5)
        pdf.cell(w=0,h=10, txt=cuerpo6, border=2,  align='C', fill=0)
        pdf.ln(5)
        pdf.cell(w=0,h=10, txt=cuerpo7, border=2,  align='C', fill=0)
        pdf.ln(5)
        pdf.cell(w=0,h=10, txt=cuerpo8, border=2,  align='C', fill=0)
        pdf.ln(5)
        pdf.cell(w=0,h=10, txt=cuerpo9, border=2,  align='C', fill=0)
        pdf.ln(5)
        pdf.cell(w=0,h=10, txt=cuerpo0, border=2,  align='C', fill=0)
        pdf.ln(5)
        
        #pdf.output('{ruta}CheckList_{fechaReporte}.pdf', 'F').encode('latin-1', 'ignore').decode('latin-1')
        pdf.output('D:/AD/BUROS/descargas/{0}_{1}.pdf'.format(ci_cliente,"Hoja_de_Riesgo"), 'F')
except Exception as e:
    PrintException()
    raise e
