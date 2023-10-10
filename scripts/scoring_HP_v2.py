# script.py

from datetime import datetime
from datetime import timedelta
from lxml import etree
from collections import Counter
import logging

logging.basicConfig(filename='D:\AD\BUROS_05\scoring\logfile.log', level=logging.INFO) 

deudaDirecta = []
deudaIndirecta = []
asfi=[]
archivoAsfi=GetVar('archivoAsfi')

def salto(mensaje):
    print("_________________")
    print(" ")
    print(mensaje)
    for x in range(0,3):
        print("_________________")
        
deudaDirecta=archivoAsfi.split("deudaDirecta =")[1].split("deudaIndirecta =")[0].strip("\n").strip(" ")
deudaDirecta=deudaDirecta.split('],')
deudaDirecta=deudaDirecta[1:]
deudaDirecta=str(deudaDirecta).replace("'[","'")
deudaDirecta=str(deudaDirecta).replace("]]']","']")
#print(deudaDirecta)
#print("INDIRECTA")
deudaIndirecta=str(archivoAsfi).split("deudaIndirecta =")[1].strip(" ")
#print(deudaIndirecta)

deudaDirecta = eval(deudaDirecta)
DD=[]
for x in deudaDirecta:
    sp=x.split('|')
    DD.append(sp)
print(DD)
salto('CIC calificacion')
#######CIC#######
#1 CIC calificacion
calA=[]
calB=[]
for x in DD:
    calB.append(x[2])
calB.sort(reverse=True)
print(calB[0])
cicCalificacion = calB[0]
SetVar('cicCalificacion', cicCalificacion)
logging.info('SetVar cicCalificacion = %s', cicCalificacion)

#2 CIC Número de EIF Directas incluyendo a PEF
salto('CIC numero EIF con PEF')
cont=0
eifWpef=[]
for x in DD:
    #print(x[0])
    eifWpef.append(x[0])
#print(eifWpef)
numEIFiPEF=len(set(eifWpef))-1
print(numEIFiPEF)
SetVar('eifDirectasConPef', numEIFiPEF)
logging.info('SetVar eifDirectasConPef = %s', numEIFiPEF)

#######INFOCRED#######
rutaInfocred = GetVar("rutaInfocred")
print(rutaInfocred)
doc = etree.parse(rutaInfocred)
raiz=doc.getroot()
data = raiz.find("datosFinancieros/sISTEMAFINANCIERO/sISTEMAFINANCIERO")
historialDirecta = raiz.find("datosFinancieros/formatoHistorial/vwSaldosPersonaDeudaDirecta")
casas = raiz.find("datosFinancieros/cASASCOMERCIALES/cACOMER")
consultas = raiz.find("cONSULTASREALIZADAS")



#1 Número de operaciones indirectas incluyendo PEF
cantGarante=0
for x in data:
    a=x.findtext('tIPOOBLIGADO')
    if str(a) == '02 - GARANTE':
        cantGarante=cantGarante+1
    print(a)
print(cantGarante)
SetVar('InfocredCantGarante', cantGarante)
logging.info('SetVar InfocredCantGarante = %s', cantGarante)

#2 Número de EIF Directas incluyendo a PEF
cantDeudorCodeudor=0
for x in data:
    a=x.findtext('tIPOOBLIGADO') 
    if 'DEUDOR' in str(a):
        cantDeudorCodeudor=cantDeudorCodeudor+1
    print(a)
print(cantDeudorCodeudor)
SetVar('cantDeudorCodeudor', cantDeudorCodeudor) 
logging.info('SetVar cantDeudorCodeudor = %s', cantDeudorCodeudor)

#3 Historial - Calificación directa últimos 60 meses
listHDirecta=[]
calDirecta60=5
for x in historialDirecta:
    a=x.findtext('eSTADO1')
    listHDirecta.append(a)
    a=x.findtext('eSTADO2')
    listHDirecta.append(a)
    a=x.findtext('eSTADO3')
    listHDirecta.append(a)
    a=x.findtext('eSTADO4')
    listHDirecta.append(a)
    a=x.findtext('eSTADO5')
    listHDirecta.append(a)
listHDirecta=list(set(listHDirecta))
listHDirecta.reverse()
print(listHDirecta)
for y in listHDirecta:
    if y=='4':
        calDirecta60=4
        break
    else:
        if y=='3':
            calDirecta60=3
            break
        else:
            if y=='2':
                calDirecta60=2
                break
            else:
                if y=='1':
                    calDirecta60=1
                    break
print(calDirecta60)
SetVar('calDirecta60', calDirecta60)
logging.info('SetVar calDirecta60 = %s', calDirecta60)

#4 Historial - Calificación indirecta últimos 60 meses
listHIndirecta=[]
calIndirecta60=5
for x in historialDirecta:
   a=x.findtext('eSTADO1')
   listHIndirecta.append(a)
   a=x.findtext('eSTADO2')
   listHIndirecta.append(a)
   a=x.findtext('eSTADO3')
   listHIndirecta.append(a)
   a=x.findtext('eSTADO4')
   listHIndirecta.append(a)
   a=x.findtext('eSTADO5')
   listHIndirecta.append(a)
listHIndirecta=list(set(listHIndirecta)) 
listHIndirecta.reverse()
print(listHIndirecta)
for y in listHIndirecta:
    if y=='4':
        calIndirecta60=4
        break
    else:
        if y=='3':
            calIndirecta60=3
            break
        else:
            if y=='2':
                calIndirecta60=2
                break
            else:
                if y=='1':
                    calIndirecta60=1
                    break
print(calIndirecta60)
SetVar('calIndirecta60', calIndirecta60)
logging.info('SetVar calIndirecta60 = %s', calIndirecta60)

#5 Deudas en casa comerciales

listaCasas=[]
if(casas==None):
    countCasas=0
else:
    countCasas=(len(casas))
print("estas son casas Comerciales")
print(countCasas) 
print("---------------------------")
SetVar('countCasas', countCasas)
logging.info('SetVar countCasas = %s', countCasas)

if(countCasas>0):
    i=0
    while i<countCasas:
        estadoCasas = casas[i].findtext("eSTADODEUDA")
        listaCasas.append(estadoCasas)
        i+=1
    print(listaCasas)
    listaCasas.sort()
    a=listaCasas[0]
    if a in 'VIGENTE':
        a='Vigente'
    if a in 'CASTIGADA':
        a='Castigado' 
    if a in 'VENCIDA':
        a='Vencido'

    SetVar('dCasas', a)
    logging.info('SetVar dCasas = %s', a)
    
else:
    SetVar('dCasas','0')
    logging.info('SetVar dCasas = 0')

#6 Monto de la operaciones 

listaOper=[]
for x in historialDirecta:
    a=int(x.findtext('sALDO1').replace(',',''))
    listaOper.append(a)
    a=int(x.findtext('sALDO2').replace(',',''))
    listaOper.append(a)
    a=int(x.findtext('sALDO3').replace(',',''))
    listaOper.append(a)
    a=int(x.findtext('sALDO4').replace(',','')) 
    listaOper.append(a)
    a=int(x.findtext('sALDO5').replace(',',''))
    listaOper.append(a)
print(listaOper) 
listaOper=list(set(listaOper))
listaOper.sort(reverse=True)
print(listaOper)
w=int(listaOper[0])
if w==0:
    SetVar('monOper','0')
    logging.info('SetVar monOper = 0')
if w>0 and w<=5000:
   SetVar('monOper','[0-5000]')
   logging.info('SetVar monOper = %s', '[0-5000]') 
if w>5000 and w<=10000:
   SetVar('monOper','[5000-10000]')
   logging.info('SetVar monOper = %s', '[5000-10000]')
if w>10000:
   SetVar('monOper','>10000')
   logging.info('SetVar monOper = %s', '>10000')

#7 Consulta en otras EIF en los últimos 90 días 
listaConsulta=[]
now = datetime.now()
Dats= now - timedelta(days=90)
print(Dats)

for x in consultas:
   f=x.findtext('fECHA')
   fecha_dt = datetime.strptime(f, '%d/%m/%Y %H:%M:%S')
   #print(fecha_dt)
   if fecha_dt>=Dats:
       a=x.findtext('iNSTITUCION')
       if 'ECOFUTURO' in a:
           print('hay ECOFUTURO')
       else:
           listaConsulta.append(a)
#print(listaConsulta)
listaConsulta=list(set(listaConsulta))
print(len(listaConsulta))
if int(len(listaConsulta)) > 0:
    SetVar('conEIF','Si')
    logging.info('SetVar conEIF = Si')  
else:
    SetVar('conEIF','No')
    logging.info('SetVar conEIF = No')

if int(len(listaConsulta)) > 3:
    SetVar('cantidadEIF','3')
    logging.info('SetVar cantidadEIF = 3')
else:
    SetVar('cantidadEIF',len(listaConsulta)) 
    logging.info('SetVar cantidadEIF = %s', len(listaConsulta))