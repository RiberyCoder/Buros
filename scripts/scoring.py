from datetime import datetime
from lxml import etree
from collections import Counter
deudaDirecta = []
deudaIndirecta = []
asfi=[]
print("""###################################
#           DATOS ASFI            #
###################################""")
archivoAsfi=GetVar('archivoAsfi')
print("ARCHIVOS ASFI :",archivoAsfi)
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
SetVar('cicCalificacion',calB[0])

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
SetVar('eifDirectasConPef',numEIFiPEF)



#######INFOCRED#######
rutaInfocred = GetVar("rutaInfocred")
#rutaInfocred = r'D:/AD/BUROS_05/descargas/BUROS/4189131/4189131.xml'
doc = etree.parse(rutaInfocred)
raiz=doc.getroot()
data = raiz.find("datosFinancieros/sISTEMAFINANCIERO/sISTEMAFINANCIERO")
historialDirecta = raiz.find("datosFinancieros/formatoHistorial/vwSaldosPersonaDeudaDirecta")
casas = raiz.find("datosFinancieros/cASASCOMERCIALES/cACOMER")
consultas = raiz.find("cONSULTASREALIZADAS")

print("""##################################
#               DATA             # 
##################################""")
print(data)
#1 Número de operaciones indirectas incluyendo PEF
cantGarante=0
for x in data:
    a=x.findtext('tIPOOBLIGADO')
    if str(a) == '02 - GARANTE':
        cantGarante=cantGarante+1
    print(a)
print(cantGarante)
SetVar('InfocredCantGarante',cantGarante)

#2 Número de EIF Directas incluyendo a PEF
cantDeudorCodeudor=0
for x in data:
    a=x.findtext('tIPOOBLIGADO').split(' ')
    if a[2] == 'DEUDOR': #'DEUDOR' in str(a):
        print("DEUDOR :",a)
        cantDeudorCodeudor=cantDeudorCodeudor+1
    deudor = x.findtext('tIPOOBLIGADO').split(' ')
    #print(deudor[2])
#print("""##################################
#     cantDeudorCodeudor         # 
##################################""")
print(cantDeudorCodeudor)
if cantDeudorCodeudor > 4:
    SetVar('cantDeudorCodeudor',4)
else:
    SetVar('cantDeudorCodeudor',cantDeudorCodeudor)
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
SetVar('calDirecta60',calDirecta60)


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
SetVar('calIndirecta60',calIndirecta60)


#5 Deudas en casa comerciales

listaCasas=[]
if(casas==None):
    countCasas=0
else:
    countCasas=(len(casas))    
print("estas son casas Comerciales")
print(countCasas)
print("---------------------------")
SetVar('countCasas',countCasas)
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
    
    SetVar('dCasas',a)
    #for x in listaCasas:
else:
    SetVar('dCasas','0')
    
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
if w>0 and w<=5000:
    SetVar("monOper","[0-5000]")
if w>5000 and w<=10000:
    SetVar('monOper','[5000-10000]')
if w>10000:
    SetVar('monOper','>10000')

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
else:
    SetVar('conEIF','No')

if int(len(listaConsulta)) > 3:
    SetVar('cantidadEIF','3')
else:
    SetVar('cantidadEIF',len(listaConsulta))


#8 Nro de EIF consultadas


    
'''    a=x.findtext('eSTADO2')
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
    asdasd
print(calIndirecta60)
#SetVar('calIndirecta60',calIndirecta60)
'''



"""
def cliente_asfi(contadorAceptados,contadorRechazados, contadorRecomendado):

    try:
       
        calificacion = ""
        validadorCalificacion = ""
        cantidadDeudaDirecta = 0
        entidadAsfi = ""
        acumuladorValidadorDirecta = ""
        acumuladorVigenteVencido = ""
        acumuladorEntidad = ""
        vencida = ""
        vigente = ""
        validadorVigente=""
        validadorVencida=""
        cantidadCalificacionDistintas = 0
        cantidadCalificacionDistintasDirectas = 0
        cantidadCalificacionDistintasIndirectas = 0
        
        cantidadDeudasEjecucion = 0
        cantidadDeudasCastigadas = 0
        deudaSaldo=0
        
        cantidadCuentasRehabilitadas=0
        cantidadDeudasCC_AFP_SAFIS=0
        
        
        tamanioDirecta = 0
        tamanioDirecta = len(deudaDirecta)
        tamanioIndirecta = 0
        tamanioIndirecta = len(deudaIndirecta)
        
        
        if tamanioDirecta >= 1:
        
    # VALIDACION ASFI
            #Directas
            for directa in deudaDirecta:
                #1 Periodo 
                
                # 2. Suma total de Deuda Directa mas Deuda Cotingente
                directa = directa.split("|")
                directa[9] =directa[9].replace(",","")
                directa[10] =directa[10].replace(",","")
               
                deudaSaldo=deudaSaldo+float(directa[9])+float(directa[10])
                deudaSaldo = round(deudaSaldo, 2)
                
                # 3. Si tiene 4 o más deudas directas, se rechaza
                #entidadAsfi = directa[0]
                #if entidadAsfi != "PEF":
                cantidadDeudaDirecta += 1
                
                if validadorCalificacion == "ACEPTADO" and validadorVencida == "ACEPTADO" and validadorVigente == "ACEPTADO":
                    contadorAceptados += 1
                else:
                    contadorRechazados += 1
                
                # 4. Si tiene una calificación distinta a  "A" se rechaza
                #directa = directa.split("|")
                calificacion = directa[2]
                
                if calificacion != "A":
                    validadorCalificacion = "RECHAZADO"
                    cantidadCalificacionDistintasDirectas += 1
                    
                    contadorRecomendado+=1
                else:
                    validadorCalificacion = "ACEPTADO"
                    
                         
          
            if cantidadDeudaDirecta >= 4:
                acumuladorEntidad = "RECHAZADO"
            else:
                acumuladorEntidad = "ACEPTADO"
            
            if acumuladorEntidad == "ACEPTADO":
                contadorAceptados += 1
            else:
                contadorRechazados += 1
        
        
    
        
        
       
                
        
        #cantidadCalificacionDistintas=cantidadCalificacionDistintasDirectas+cantidadCalificacionDistintasIndirectas
        
        SetVar('cantidadDeudaDirecta',cantidadDeudaDirecta)
        #SetVar('cantidadCalificacionDistintas',cantidadCalificacionDistintas)
        SetVar('cantidadCalificacionDistintas',cantidadCalificacionDistintasDirectas)
        SetVar('cantidadDeudasEjecucion',cantidadDeudasEjecucion)
        SetVar('cantidadDeudasCastigadas',cantidadDeudasCastigadas)
        SetVar ('deudaSaldo',deudaSaldo)
    except Exception as e:
        PrintException()
        raise e
    
    # VALIDACION INFOCRED
rutaInfocred = GetVar("rutaInfocred")
print(rutaInfocred)
doc = etree.parse(rutaInfocred)
raiz=doc.getroot()
data = raiz.find("datosFinancieros/sISTEMAFINANCIERO/sISTEMAFINANCIERO")
ubicacion = raiz.find("datosFinancieros/sISTEMAFINANCIERO/sISTEMAFINANCIERO")
rehabilitacion = raiz.find("datosFinancieros/cUENTASCORRIENTES/cUENTASCORRIENTES")
casas = raiz.find("datosFinancieros/cASASCOMERCIALES/cACOMER")
afps = raiz.find("datosFinancieros/aFP/dEUDASAFPS")
safis = raiz.find("datosSafis")

contadorInfocredAceptados=0
contadorInfocredRechazados=0
cant = 0
def contar_deudas(ubicacion):
    try:
        if ubicacion == None:
            cant = 0
        else:
            cant = len(ubicacion)
            
        return cant
        
    except:
        print('contar_deudas')


# 1. Ultima fecha de Actualizacion
def cliente_fechaActualizacion(ubicacion,cant):
    try: 
        i=0
        fechaActualizacion=""
        fechaAct = "01/01/1900"
        
        while i<cant:
            fechaActualizacion = ubicacion[i].findtext("fECHAACTUALIZACION")
            formatted_fecha1 = datetime.datetime.strptime(fechaAct, "%d/%m/%Y")
            formatted_fecha2 = datetime.datetime.strptime(fechaActualizacion, "%d/%m/%Y")
            if(formatted_fecha2 > formatted_fecha1):
                fechaAct=fechaActualizacion
            i+=1;
        SetVar('ultimaFechaActualizacionInfocred',fechaActualizacion)
       
    except:
        print('cliente_fechaActualizacion')

def cliente_calificacion(ubicacion,cant,contadorInfocredAceptados,contadorInfocredRechazados):
    try:
        i=0
        j=0
        p=0
        calificacion=""
        calificacion_acumulado=''
        while i<cant:
            calificacion=ubicacion[i].findtext("cALIFICACION")
            if calificacion != "A" and calificacion != "B" and len(calificacion)>0:
                j=j+1
            i=i+1;
        if j==0:
            SetVar('validacionCalificacionInfocred','ACEPTADO')
            contadorInfocredAceptados += 1
        else:
            SetVar('validacionCalificacionInfocred','RECHAZADO')
            contadorInfocredRechazados += 1
        #SetVar('validacion3_calificacion',calificacion_acumulado)
    except:
        print('cliente_calificacion')

# 2. Saldo total mas contingente
def cliente_saldoTotalyContingente(ubicacion,cant):
    try: 
        saldo=""
        i=0
        contingente=""
        saldoyContingente=0
        
        
        while i<cant:
            
            if ubicacion[i].findtext("tIPOOBLIGADO").find("GARANTE")==(-1):
                
                saldo = ubicacion[i].findtext("sALDO")
                if len(saldo)>0:
                    saldo=saldo.replace(",","")
                
                    saldoyContingente=float(saldoyContingente)+float(saldo)
                
                contingente = str(ubicacion[i].findtext("cONTINGENTE"))
                if len(contingente)>0:
                    contingente=contingente.replace(",","")
                
                    saldoyContingente=float(saldoyContingente)+float(contingente)
                
            
            i+=1;
        SetVar('saldoyContingente',saldoyContingente)
       
    except:
        print('cliente_saldoTotalyContingente')


def cliente_estado(ubicacion,cant,contadorInfocredAceptados,contadorInfocredRechazados):
    try:
        i=0
        j=0
        j_ind=0
        p=0
        k=0
        ind=0
        estado=""
        estado_acumulado=''
        estado_acumulado_indirecta=''
        cantidadMoraEjecucion = 0
        descripcionCaedec = ""
        while i<cant:
            estado=ubicacion[i].findtext("eSTADO")
            entidad = ubicacion[i].findtext("eNTIDAD")
            monto = ubicacion[i].findtext("sALDO")
            banca = ubicacion[i].findtext("tIPOCREDITO")
            caedec = ubicacion[i].findtext("aCTECONO")
            fechaInicio = ubicacion[i].findtext("fECHAINICIO")
            actecono = ubicacion[i].findtext("aCTECONO")
            tIPOOBLIGADO = ubicacion[i].findtext("tIPOOBLIGADO")
            if len(estado)>0:
                if estado != "VIGENTE" or estado != "MORA" and len(estado)>0:
                    j=j+1
            i=i+1
            
            if tIPOOBLIGADO.find("MORA") > 0 or tIPOOBLIGADO.find("EJECUCION") > 0 or tIPOOBLIGADO.find("CASTIGADO") > 0:
                cantidadMoraEjecucion += 1
                
            if caedec != "" and fechaInicio != "":
                if descripcionCaedec == "":
                    descripcionCaedec = caedec+"|"+fechaInicio+"---"
                else:
                    descripcionCaedec = descripcionCaedec + caedec+"|"+fechaInicio+"---"
        if j==0:
            if k==0:
                SetVar('validacion2_res','ACEPTADO')
                contadorInfocredAceptados += 1
        else:
            SetVar('validacion2_res','RECHAZADO')
            contadorInfocredRechazados += 1
        SetVar('cantidadMoraEjecucion', cantidadMoraEjecucion)
        SetVar('descripcionCaedec',descripcionCaedec)
    except:
        print('cliente_estado')
# 3. Si los estados son distintos a vigentes

def cliente_distintosaVigente(ubicacion,cant, contadorRecomendado):
    try: 
        estadoCantidad=0
        estado=""
        i=0
        cantDistintoVigente=0
                
        while i<cant:
            estado = ubicacion[i].findtext("eSTADO")
            if len(estado)>0:
                if estado !="VIGENTE" :
                    estadoCantidad+=1
                    contadorRecomendado+=1
            i+=1;
        SetVar('estadoCantidad',estadoCantidad)
        
       
    except:
        print('cliente_distintosaVigente')



# 4. Cantidad de cuentas rehabilitadas de cuentas clausuradas

def cliente_cuentas_rehabilitadas(rehabilitacion):
    #rehabilitacion
    try: 
        countHab=0
        #cuentas_rehabilitadas
        if(rehabilitacion==None):
            rehabilitacion=0
        else:
            countHab=(len(rehabilitacion))    
        print("estas son cuentas rehabilitadas")
        print(countHab)
        print("---------------------------")
        SetVar('cantidadCuentasRehabilitadas',countHab)
       
    except:
        print('cliente_cuentas_rehabilitadas')

# 5. Cantidad deudas distintas a vigentes en casas comerciales,AFP,SAFIS

def cliente_deudas_CC_AFP_SAFIS(casas,afps,safis):
    try: 
    
        countCasas=0
        contCasasNV=0
        countAfps=0   
        countSafis=0   
        count_CC_AFP_SAFIS=0
        mensaje_CC=''
        mensaje_AFP=''
        mensaje_SAFIS=''
        deudaCasas=[]
        i=0
        
        #casas Comerciales
        if(casas==None):
            countCasas=0
        else:
            countCasas=(len(casas))    
        print("estas son casas Comerciales")
        print(countCasas)
        print("---------------------------")
        
        if(countCasas>0):
            mensaje_CC="*Verificar deudas de casas comerciales."
            print(mensaje_CC)
            #SetVar('mensaje_CC',mensaje_CC)
            SetVar('countCasas',countCasas)
            while i<countCasas:
                deudaCasas.append([])
                entidadCasas = casas[i].findtext("eNTIDAD")
                montoCasas = casas[i].findtext("mONTO")
                fechaCasas = casas[i].findtext("fECHAINICIOOPERACION")
                estadoCasas = casas[i].findtext("eSTADODEUDA")
                print(estadoCasas)
                if estadoCasas == 'VIGENTE':
                    print('casa Vigente')
                else:
                    contCasasNV=contCasasNV+1
                    print('casa NO Vigente')
                tipoCasas = casas[i].findtext("tIPOOBLIGADO")
                deudaCasas[i].append(entidadCasas)
                deudaCasas[i].append("Monto: "+str(montoCasas))
                deudaCasas[i].append(str(fechaCasas)+"   "+estadoCasas+" - "+tipoCasas)
                i+=1
            print(deudaCasas)
            SetVar('deudaCasas',deudaCasas)
        
        #AFP
        if(afps==None):
            countAfps=0
        else:
            countAfps=(len(afps))
        print("estas son afps")
        print(countAfps)
        print("---------------------------")

        if(countAfps>0):
            mensaje_AFP="*Verificar deudas de AFPs."
            print(mensaje_AFP)
            SetVar('mensaje_AFP',mensaje_AFP)
        #SAFIS
        if(safis==None):
            countSafis=0
        else:
            countSafis=(len(safis))
            
        print("estas son safis")
        print(countSafis)
        print("---------------------------")
        
        if(countSafis>0):
            mensaje_SAFIS="*Verifica deudas de SAFIS."
            print(mensaje_SAFIS)
            SetVar('mensaje_SAFIS',mensaje_SAFIS)
        
        count_CC_AFP_SAFIS=contCasasNV+countAfps+countSafis
        SetVar('cantidadDeudasCC_AFP_SAFIS',count_CC_AFP_SAFIS)
        
       
    except:
        print('cliente_deudas_CC_AFP_SAFIS')



def cliente_entidades(ubicacion,cant,cuantas_entidades,contadorInfocredAceptados,contadorInfocredRechazados):
    try:
        i=0
        j=0
        p=0
        entidad=""
        entidad_acumulado=''
        entidad_acumalador = ""
        cantidadIndirectaInfocred = 0
        while i<cant:
            entidad = ubicacion[i].findtext("eNTIDAD")
            monto = ubicacion[i].findtext("sALDO")
            tIPOOBLIGADO = ubicacion[i].findtext("tIPOOBLIGADO")            
            entidad_acumalador = entidad_acumalador + entidad + " "
            if len(monto)>0:
                if tIPOOBLIGADO.find("GARANTE") > 0:
                    j=j+1
                    cantidadIndirectaInfocred += 1
            i=i+1;
        if j<=cuantas_entidades:
            contadorInfocredAceptados += 1
        else:
            contadorInfocredRechazados += 1
        SetVar("cantidadIndirectaInfocred",cantidadIndirectaInfocred)
    except :
        print('cliente_entidades')

def cliente_historial(ubicacion,cant,contadorInfocredAceptados,contadorInfocredRechazados):
    
    try:
        i=0
        j=0
        p=0
        j_ind=0
        p_ind=0
        historial=""
        historial_acumulado=''
        historial_acumulado_ind=''
        historicoCrediticio = ""
        while i<cant:
            historial=ubicacion[i].findtext("hISTORICO")
            numeros = list(map(int,str(historial)))
            entidad = ubicacion[i].findtext("eNTIDAD")
            monto = ubicacion[i].findtext("sALDO")
            tIPOOBLIGADO = ubicacion[i].findtext("tIPOOBLIGADO")
            if len(historial)>0:
                if (str(historial).find("2") > 0 or str(historial).find("3") > 0 or str(historial).find("4") > 0):
                    validacion5_historial = "RECHAZADO"
                    
                else:
                    validacion5_historial = "ACEPTADO"
                    
            i=i+1;
        if validacion5_historial == "ACEPTADO":
            historicoCrediticio = "BUENO"
            contadorInfocredAceptados += 1
        else:
            historicoCrediticio = "MALO"
            contadorInfocredRechazados += 1
        SetVar('historicoCrediticio',historicoCrediticio)
        print (historicoCrediticio)
    except :
        print('cliente_historial')
    
try:
    cliente_asfi(contadorAceptados,contadorRechazados,contadorRecomendado=0)
    contadorInfocredAceptados = 0
    contadorInfocredRechazados = 0
    cant=contar_deudas(ubicacion) 
    
    
    if cant >= 0:
        cliente_calificacion(ubicacion,cant,contadorInfocredAceptados,contadorInfocredRechazados)
        cliente_estado(ubicacion,cant,contadorInfocredAceptados,contadorInfocredRechazados)
        cliente_entidades(ubicacion,cant,3,contadorInfocredAceptados,contadorInfocredRechazados)
        cliente_historial(ubicacion,cant,contadorInfocredAceptados,contadorInfocredRechazados)
        
        cliente_fechaActualizacion(ubicacion,cant)
        cliente_saldoTotalyContingente(ubicacion,cant)
        cliente_distintosaVigente(ubicacion,cant,contadorRecomendado)
        cliente_cuentas_rehabilitadas(rehabilitacion)
        cliente_deudas_CC_AFP_SAFIS(casas,afps,safis)
    else:
        SetVar("cantidadIndirectaInfocred",0)
        SetVar('historicoCrediticio',"BUENO")
        SetVar('cantidadMoraEjecucion', 0)
        SetVar('descripcionCaedec', "Ninguno")
        
    
    print (contadorRecomendado)
    if contadorRecomendado>0:
        SetVar('recomendado',"NO RECOMENDADO")
    else:
        SetVar('recomendado',"RECOMENDADO")    
        
    if contadorInfocredRechazados > 0 or contadorRechazados > 0:
        aceptadoRechazado = "OBSERVADO"
    else:
        aceptadoRechazado = "RECOMENDADO"
    SetVar('aceptadoRechazado',aceptadoRechazado)
except :
    print ('error en set')
"""