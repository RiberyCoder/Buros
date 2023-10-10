from inputimeout import inputimeout, TimeoutOccurred
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from plyer import notification
from cryptography.fernet import Fernet
import threading
import configparser
import os
import time
import threading
import sys
import base64

# Rutas de archivos
ruta_archivo_config = "D:/AD/DESEMBOLSO/config/config_desembolsos2.ini"
ruta_archivo_clave = "D:/AD/DESEMBOLSO/scripts/Key2.key"

# Ejemplo de uso
notification_timeout = 3  
icon_path = "D:/AD/DESEMBOLSO/scripts/logoAlldigital.ico"

# Crear una nueva clave privada protegida con una contraseña inicial
clave_privada_path = "D:/AD/DESEMBOLSO/scripts/private.pem"
clave_publica_path = "D:/AD/DESEMBOLSO/scripts/public.pem"

# Ruta completa al archivo .ini en "D:\AD\DESEMBOLSO"
#ruta_archivo_ini = "D:/AD/DESEMBOLSO/config/config_desembolsos.ini"

resultado = []
########################################################
#            CREACION DE LA CLAVE PRIVADA              #
########################################################

def crear_clave_privada_con_contraseña(clave_privada_path, nueva_contraseña):
    global serialization
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    clave_privada_encriptada = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(nueva_contraseña)
    )

    with open(clave_privada_path, "wb") as key_file:
        key_file.write(clave_privada_encriptada)

    return private_key
    
def serializar_y_guardar_clave_publica(clave_publica, nombre_archivo):
    global serialization
    clave_publica_pem = clave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(nombre_archivo, "wb") as public_key_file:
        public_key_file.write(clave_publica_pem)
        
########################################################
#              FUNCIÓN DE NOTIFICACIÓN                 #
########################################################

def mostrar_notificacion(titulo, mensaje, duracion, icono=None):
    global notification
    notification.notify(
        title=titulo,
        message=mensaje,
        timeout=duracion,
        app_icon=icono
    )

########################################################
#              CREACION DE CLAVE FORNET                #
########################################################

# Función para generar una nueva clave
def generar_nueva_clave():
    global Fernet
    return Fernet.generate_key()

# Función para encriptar datos con una clave específica
def encriptar_datos(datos, clave):
    global Fernet
    datos = str(datos)
    fernet = Fernet(clave)
    datos_encriptados = fernet.encrypt(datos.encode("utf-8"))
    return datos_encriptados

# Función para desencriptar datos con una clave específica
def desencriptar_datos(datos, clave):
    global Fernet
    try:
        fernet = Fernet(clave)
        datos_desencriptados = fernet.decrypt(datos)
        return datos_desencriptados.decode("utf-8")
    except Exception as e:
        print(f"Error al desencriptar datos: {e}")

########################################################
#                 CAMBIO DE CONTRASEÑA                 #
########################################################

# Cambiar la contraseña de la clave privada
def cambiar_contraseña(clave_privada_path, contraseña_actual, nueva_contraseña):
    global serialization
    try:
        # Cargar la clave privada original con la contraseña actual
        with open(clave_privada_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=contraseña_actual
            )

        # Volver a encriptar la clave privada con la nueva contraseña
        nueva_clave_privada_encriptada = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(nueva_contraseña)
        )

        # Guardar la nueva versión de la clave privada con la nueva contraseña
        with open(clave_privada_path, "wb") as new_key_file:
            new_key_file.write(nueva_clave_privada_encriptada)

    except Exception as e:
        print("Error:", str(e))

########################################################
#        FUNCION PARA PEDIR NUEVO PASSWORD             #
########################################################
#contraseña_actual = None

def cambiar_contraseña_si_es_necesario(clave_privada_path, contraseña_actual):
    global inputimeout
    global TimeoutOccurred
    global resultado
    try:
        respuesta = inputimeout(prompt="¿Desea cambiar la contraseña (S/N)? ", timeout=10)
    except TimeoutOccurred:
        respuesta = "n"
    except Exception as e:
        print("Ocurrió un error:", str(e))
        
    if respuesta.lower() == "s":
        nueva_contraseña = input("Ingrese la nueva contraseña: ")
        nueva_contraseña_bytes = nueva_contraseña.encode("utf-8")
        cambiar_contraseña(clave_privada_path, contraseña_actual.encode("utf-8"), nueva_contraseña_bytes)
        print("La contraseña ha sido cambiada exitosamente.")
        resultado.append(nueva_contraseña_bytes)
    elif respuesta.lower() == "n":
        nueva_contraseña = contraseña_actual
        print("La contraseña no ha sido cambiada.")
        resultado.append(nueva_contraseña)
    else:
        nueva_contraseña = contraseña_actual
        print("Respuesta no válida. La contraseña no ha sido cambiada.")
        resultado.append(nueva_contraseña)
    #return contraseña_actual

#######################################################
#  ENCRIPTACIONES DE TEXTO y DESENCRIPTACION E2E       #
########################################################

def cargar_clave_privada(ruta_archivo_clave_privada, contraseña):
    global serialization
    with open(ruta_archivo_clave_privada, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=contraseña
        )
    return private_key
def cargar_clave_privada(ruta_archivo_clave_privada, contraseña):
    global serialization
    try:
        with open(ruta_archivo_clave_privada, "rb") as key_file:
            password = contraseña.strip()
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=password
            )
        return private_key
    except Exception as e:
        print(f"Error al cargar la clave privada: {e}")

def cargar_clave_publica(clave_privada):
    return clave_privada.public_key()

def encriptar_mensaje(mensaje, clave_publica):
    global padding
    global hashes
    mensaje_encriptado = clave_publica.encrypt(
        mensaje.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return mensaje_encriptado

def desencriptar_mensaje(mensaje_encriptado, clave_privada):
    global padding
    global hashes
    mensaje_descifrado = clave_privada.decrypt(
        mensaje_encriptado,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return mensaje_descifrado.decode("utf-8")

########################################################
#         GUARDAR EL TEXTO EN UN .INI                  #
########################################################

# Función para cargar, encriptar y guardar un archivo INI
def cargar_encriptar_guardar_ini(ruta_archivo_ini, clave_privada,config):
    global desencriptar_mensaje
    global encriptar_mensaje
    try:
        print("-------------------Función para cargar, encriptar y guardar un archivo INI-------------------")
        # Obtener la clave pública correspondiente a la clave privada
        clave_publica = clave_privada.public_key()

        secciones_y_claves = [
            ("CONF", "odbcdriver"),
            ("CONF", "odbcserver"),
            ("CONF", "odbcbd"),
            ("CONF", "odbcu"),
            ("CONF", "odbcp"),
            ("SERVER_BUROS", "sesion"),
            ("SERVER_BUROS", "db"),
            ("SERVER_BUROS", "uss"),
            ("SERVER_BUROS", "pass"),
            ("SERVER_BUROS", "serv"),
            ("SERVER_CORREO", "uss_cor"),
            ("SERVER_CORREO", "pass_cor"),
            ("SERVER_CORREO", "serv_cor"),
            ("SERVER_CORREO", "cpy_cor"),
            ("NETBANK", "uss_nb"),
            ("NETBANK", "pass_nb"),
            ("NETBANK", "2captcha"),
            ("NETBANK", "ocrgoogle"),
            ("NETBANK", "login"),
            ("NETBANK", "prestamos"),
            ("NETBANK", "cuentasahoro"),
            ("NETBANK", "desembolso"),
            ("NETBANK", "logout"),
            ("AlimentarInfo", "data_sql0"),
            ("Enviar_Buros_PCCU", "insergrupo"),
            ("Enviar_Buros_PCCU", "consulpccu"),
            ("Enviar_Buros_PCCU", "inserpccu"),
            ("Enviar_Buros_PCCU", "enviopccu"),
            ("SolFallida", "data_sql1"),
            ("EsperaPccu", "sqllistapccu"),
            ("EsperaPccu", "coincidencia"),
            ("EsperaPccu", "aceppccuno"),
            ("EsperaPccu", "procdpccuno_ok"),
            ("EsperaPccu", "plandesbno_ok"),
            ("EsperaPccu", "errook"),
            ("DebitoAutomatico", "data_sql3"),
            ("MaestroPrestamos", "inserprestamo"),
            ("MaestroPrestamos", "aptostate"),
            ("MaestroCuentasAhorros", "updateretenciones"),
            ("ActualizarDatos", "actprestamo"),
            ("ActualizarDatos", "proceso"),
            ("Desembolso", "updatedesembolsos")
        ]

        # Iterar a través de las secciones y claves
        for seccion, clave in secciones_y_claves:
            valor_actual = config[seccion][clave]
            print(valor_actual)

            if valor_actual.startswith("ENCRYPTED:"):
                print("entro a desemcriptar")
                valor_encriptado_base64 = valor_actual[len("ENCRYPTED:"):]
                valor_encriptado_bytes = base64.b64decode(valor_encriptado_base64)
                valor_desencriptado = desencriptar_mensaje(valor_encriptado_bytes, clave_privada)
                #config[seccion][clave] = valor_desencriptado #Descomenta y comentar el resto
                print(clave,"=",valor_desencriptado)
                #SetVar(f"{clave}", valor_desencriptado)

                valor_reencriptado = encriptar_mensaje(valor_desencriptado, clave_publica)
                valor_reencriptado_base64 = base64.b64encode(valor_reencriptado).decode("utf-8")
                config[seccion][clave] = "ENCRYPTED:" + valor_reencriptado_base64
                
            else:
                #print(clave,"=",valor_desencriptado)
                valor_encriptado = encriptar_mensaje(valor_actual, clave_publica)
                valor_encriptado_base64 = base64.b64encode(valor_encriptado).decode("utf-8")
                config[seccion][clave] = "ENCRYPTED:" + valor_encriptado_base64

        try:
            with open(ruta_archivo_ini, "w") as configfile:
                config.write(configfile)
        except Exception as e:
            print(f"Error al guardar los cambios en el archivo INI: {e}")

    except (configparser.NoSectionError, configparser.NoOptionError, FileNotFoundError) as e:
        print("Error al cargar el archivo INI:", e)


########################################################
#                LOGICA ENCRIPTACION                   #
########################################################

if os.path.isfile(ruta_archivo_config):
    config = configparser.ConfigParser()
    config.read(ruta_archivo_config, encoding='latin1') #encoding='latin1' encoding='utf-16'
    # Imprimir el contenido de la configuración
    #for section in config.sections():
        #print(f"Sección: {section}")
        #for key, value in config.items(section):
            #print(f"  {key}: {value}")
    clave_secreta = generar_nueva_clave()
    print(clave_secreta)
    # Verifica si la sección y la clave existen en el archivo config.ini
    if "PASSWORESTREMO" in config and "authentication" in config["PASSWORESTREMO"]:
        contraseña = config["PASSWORESTREMO"]["authentication"]

        # Verifica si la contraseña está encriptada (por ejemplo, comprobando un prefijo)
        if contraseña.startswith("ENCRYPTED:"):
            try:
                # Remueve el prefijo y desencripta la contraseña con la clave actual
                contraseña = contraseña[len("ENCRYPTED:"):]
                with open(ruta_archivo_clave, 'rb') as archivo_clave:
                    clave_secreta_actual = archivo_clave.read()
                contraseña_desencriptada = desencriptar_datos(contraseña.encode("utf-8"), clave_secreta_actual)
                contraseña_desencriptada_str = contraseña_desencriptada.replace("b'","").replace("'","")
                #contraseña_cambiada_event = threading.Event()
                
                #temporizador = threading.Thread(target=cambiar_contraseña_si_es_necesario, args=(clave_privada_path, contraseña_desencriptada, contraseña_desencriptada))
                temporizador = threading.Thread(target=cambiar_contraseña_si_es_necesario, args=(clave_privada_path, contraseña_desencriptada_str))
                temporizador.start()
                temporizador.join()
                contraseña_desencriptada = resultado[0]
                nueva_contraseña_inicial = str(contraseña_desencriptada).replace("b'","").replace("'","")
                nueva_contraseña_inicial2 = contraseña_desencriptada if isinstance(contraseña_desencriptada, bytes) else contraseña_desencriptada.encode('utf-8')

                if not os.path.exists(clave_privada_path):
                    clave_privada = crear_clave_privada_con_contraseña(clave_privada_path, nueva_contraseña_inicial2)
                    clave_publica = clave_privada.public_key()
                    serializar_y_guardar_clave_publica(clave_publica, clave_publica_path)
                else:
                    print("Ya existe la llave, se usara la funcion cargar_encriptar_guardar_ini")
                    clave_privada = cargar_clave_privada(clave_privada_path, nueva_contraseña_inicial2)
                    clave_publica = cargar_clave_publica(clave_privada)
                    cargar_encriptar_guardar_ini(ruta_archivo_config, clave_privada, config)


                contraseña_encriptada = encriptar_datos(nueva_contraseña_inicial2, clave_secreta)
                with open(ruta_archivo_clave, 'wb') as archivo_clave:
                    archivo_clave.write(clave_secreta)

                config["PASSWORESTREMO"]["authentication"] = "ENCRYPTED:" + contraseña_encriptada.decode("utf-8")
                with open(ruta_archivo_config, 'w') as archivo_config:
                    config.write(archivo_config)

                notification_title = "IF : Exitoso"
                notification_message = "Contraseña desencriptada y reencriptada con nueva clave, y actualizada en el archivo de configuración."
                mostrar_notificacion(notification_title, notification_message, notification_timeout, icon_path)

            except Exception as e:
                notification_title = "Error"
                notification_message = f"No se pudo desencriptar la contraseña. Error: {str(e)}"
                mostrar_notificacion(notification_title, notification_message, notification_timeout, icon_path)
        else:
            
            # Encripta la nueva contraseña con la nueva clave
            contraseña = contraseña.encode("utf-8")
            nueva_contraseña_encriptada = encriptar_datos(contraseña, clave_secreta)

            # Guarda la nueva clave_secreta en el archivo Key.key
            with open(ruta_archivo_clave, 'wb') as archivo_clave:
                archivo_clave.write(clave_secreta)

            # Actualiza la contraseña encriptada en el archivo de configuración .ini
            config["PASSWORESTREMO"]["authentication"] = "ENCRYPTED:" + nueva_contraseña_encriptada.decode("utf-8")
            with open(ruta_archivo_config, 'w') as archivo_config:
                config.write(archivo_config)
                
            notification_title = "ELSE : Exitoso"
            notification_message = "Nueva contraseña encriptada y actualizada en el archivo de configuración."
            mostrar_notificacion(notification_title, notification_message, notification_timeout, icon_path)
    else:
        notification_title = "Error"
        notification_message = "La sección o la clave no existen en el archivo config.ini."
        mostrar_notificacion(notification_title, notification_message, notification_timeout, icon_path)
else:
    notification_title = "Error"
    notification_message = "El archivo config.ini no existe en la ruta especificada."
    mostrar_notificacion(notification_title, notification_message, notification_timeout, icon_path)
