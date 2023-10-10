#################### HOJA DE RIESGOS #########################
data=GetVar('docCompleto')
if 'CLIENTE NO REGISTRADO EN LA BASE DE CREDITOS DEL BANCO' in data:
    print('No existe')

x=data.split("F/PROC")
print('////////////////////////// valor X ///////////////////////////////////////')
#print(x)
x=x[1].split('CAPTACIONES')
print("""####################################
#      VALOR X[1]   CAPTACIONES    #
####################################""")
#print(x)
c=x[0]
print("""####################################
#               VALOR C[0]         #
####################################""")
#print(c)
c=c.strip().split('\n')
print("""####################################
#              VALOR C.SPLIT()     #
####################################""")
#print(c)
lista1=[]
for t in c:
    w=t.split()
    #print(len(w))
    if len(w)==14:
        lista1.append(t.split())
        #print(t.split())
#print(lista1)

condonacion = []
atraso = []

for r in lista1:
    # Convertir solo los valores numéricos a enteros y agregar a las listas
    if 'COBROS' in r[0]:
        #print(r[0])
        try:
            condonacion.append(int(r[9].replace('.', '')))
        except ValueError:
            pass  # Ignorar elementos no numéricos

        try:
            atraso.append(int(r[13]))
        except ValueError:
            pass  # Ignorar elementos no numéricos
#print(condonacion)
#print(atraso)
condonacion.sort(reverse=True)
atraso.sort(reverse=True)

# Verificar que las listas no estén vacías antes de intentar acceder al primer elemento
if condonacion:
    ccc = condonacion[0]
    print("Mayor valor de condonación:", ccc)
else:
    print("La lista de condonación está vacía.")

if atraso:
    max_atraso = atraso[0]
    print("Mayor valor de atraso:", max_atraso)
else:
    print("La lista de atraso está vacía.")


#1 Máximo de diás de atraso

maxx=int(atraso[0])
#print('maxx :',maxx)
if maxx == 0:
    SetVar('atrasos','0')
if maxx >=1 and maxx<=5:
    SetVar("atrasos","'[0-5]")
if maxx >=6 and maxx<=8:
    SetVar("atrasos","'[5-8]")
if maxx >=9 and maxx<=15:
    SetVar("atrasos","'[9-15]")
if maxx > 15:
    SetVar("atrasos","'>15")

#2 Condonaciones

if int(ccc)>0:
    SetVar('condonaciones','No')
else:
    SetVar('condonaciones','Si')
#SetVar('prueba',data)"""
