from lxml import etree
#ruta="D:\\AD\\BUROS\\descargas\\5334195.xml"
doc = etree.parse(GetVar('rutaInfocred'))
raiz=doc.getroot()

"""CONTAR FILAS"""
def contar_filas(lugar):
    try:
        if lugar == None:
            cant = 0
        else:
            cant = len(lugar)
        return cant
        
    except Exception as e:
        PrintException()
        raise e

"""CONSULTA CONSULTAS REALIZADAS"""
institucion=[]
fecha=[]
consulta=[]

cons = raiz.find("cONSULTASREALIZADAS")
cant1=contar_filas(cons)
i=0
while i<cant1:
    texto=cons[i].findtext("iNSTITUCION")
    institucion.append(texto)
    
    texto=cons[i].findtext("fECHA")
    fecha.append(texto)
    
    texto=cons[i].findtext("cONSULTA")
    consulta.append(texto)
    i=i+1;


"""CONSULTA CASAS COMERCIALES"""
comercial_entidad=[]
comercial_monto=[]
comercial_estado=[]

ubicacion = raiz.find("datosFinancieros/cASASCOMERCIALES/cACOMER")
cant2=contar_filas(ubicacion)
i=0
while i<cant2:
    texto=ubicacion[i].findtext("eNTIDAD")
    comercial_entidad.append(texto)

    texto=ubicacion[i].findtext("mONTO")
    comercial_monto.append(texto)

    texto=ubicacion[i].findtext("eSTADODEUDA")
    comercial_estado.append(texto)
    i=i+1;
 
"""CONSULTA CAEDEC"""
caedec=""
ubicacion = raiz.find("datosFinancieros/sISTEMAFINANCIERO/dESCRIPCIONCAEDECACTECONO")
    
cant3=contar_filas(ubicacion)
i=0
while i<cant3:
    texto=ubicacion[i].findtext("dESCRIPCIONREPORTECAEDECACTECO")
    caedec+=texto+" __ \n "
    i=i+1;

SetVar('largo_listas',cant1)
SetVar('largo_listas2',cant2)

SetVar('con_institucion',institucion)
SetVar('con_fecha',fecha)
SetVar('con_consulta',consulta)

SetVar('comercial_entidad',comercial_entidad)
SetVar('comercial_monto',comercial_monto)
SetVar('comercial_estado',comercial_estado)

SetVar('con_caedec',caedec)