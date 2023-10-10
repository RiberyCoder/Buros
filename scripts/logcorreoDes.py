import os
import datetime

def asegurar_directorio(ruta):
    if not os.path.exists(ruta):
        os.makedirs(ruta)

def escribir_log(ruta, nombre_archivo, mensaje):
    ruta_completa = os.path.join(ruta, nombre_archivo)
    fecha_hora_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(ruta_completa, 'a') as archivo_log:
        archivo_log.write(f'[{fecha_hora_actual}] {mensaje}\n')

ruta_log = r'{rutaPadre}log'
nombre_archivo = 'correoDes.log'

asegurar_directorio(ruta_log)
mensaje_nuevo = """{error}"""

escribir_log(ruta_log, nombre_archivo, mensaje_nuevo)

print('Registro agregado al archivo de log.')
