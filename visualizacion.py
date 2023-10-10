import pyautogui
import threading
import time
import sys
#sys.path.append("D:/AD/DESEMBOLSO/scripts/scripts/")
import funciones
import requests
import base64
import json
import pytesseract
from PIL import Image
import cv2
import os
import logging
import subprocess
#########################################################
#          FUNCION PARA FINALIZAR PROCESOS .EXE         #
#########################################################

def cerrar_proceso(proceso):
    try:
        subprocess.run(['taskkill', '/F', '/IM', proceso], check=True)
        print(f'Proceso {proceso} cerrado exitosamente.')
    except subprocess.CalledProcessError as e:
        print(f'Error al cerrar el proceso {proceso}: {e}')

#########################################################
#       FUNCION PARA ESCRIBIR LOG SEGUN EL TICKET       #
#########################################################
#########################################################
#       FUNCION PARA ESCRIBIR LOG SEGUN EL TICKET       #
#########################################################

def registrar_log(nombre_log, log_name, log_value, log_level=logging.INFO):
    # Obtener la ruta completa del archivo de registro
    log_directory = r"D:\AD\DESEMBOLSO\logs"
    log_filename = os.path.join(log_directory, f'{nombre_log}.log')

    logger = logging.getLogger("DESEMBOLSO")

    if not logger.handlers:
        # Configurar el nivel del logger
        logger.setLevel(log_level)

        # Crear un manejador de archivo
        file_handler = logging.FileHandler(log_filename)

        # Configurar el nivel del manejador de archivo
        file_handler.setLevel(log_level)

        # Configurar el formato del manejador de archivo
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # Agregar el manejador de archivo al logger
        logger.addHandler(file_handler)

        # Verificar si el archivo ya existe
        file_exists = os.path.isfile(log_filename)

        # Si el archivo no existe, crea un nuevo registro
        if not file_exists:
            logger.info(f"Archivo creado. Nombre: {log_name}, Valor: {log_value}")

    # Si el archivo ya existe, agrega un nuevo registro
    logger.log(log_level, f"Nombre: {log_name}, Valor: {log_value}")

# Ejemplo de uso
#log_to_file("PrimerLog", "Este es un mensaje de nivel INFO")
#log_to_file("SegundoLog", "Este es un mensaje de nivel WARNING", log_level=logging.WARNING)
#log_to_file("TercerLog", "Este es un mensaje de nivel ERROR", log_level=logging.ERROR)


#########################################################
#       FUNCION PERSONALIZADA TIEMPO DE ESPERAS         #
#########################################################

def temporizador_personalizado(segundos):
    # Obtiene el tiempo actual en segundos
    tiempo_inicial = time.time()

    while True:
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicial

        if tiempo_transcurrido >= segundos:
            break

        tiempo_restante = int(segundos - tiempo_transcurrido)
        #print(f"Tiempo restante: {tiempo_restante} segundos", end="\r")

    print("\n¡El temporizador ha terminado!", tiempo_transcurrido)

#########################################################
#        FUNCION LECTURA DE OCR-GOOGLE POR IMG          #
#########################################################

def ocr_google_cloud(api_key, image_path):
    if image_path.startswith("http"):
        image = {
            "source": {
                "imageUri": image_path
            }
        }
    else:
        with open(image_path, 'rb') as image_file:
            img = image_file.read()
            content = base64.b64encode(img).decode()

        image = {
            "content": content
        }

    body = {
        "requests": [
            {
                "image": image,
                "features": [
                    {
                        "type": "TEXT_DETECTION"
                    }
                ]
            }
        ]
    }
    body = json.dumps(body)

    try:
        response = requests.post("https://vision.googleapis.com/v1/images:annotate?key={key}".format(key=api_key),
                                 data=body)
        json_resp = response.json()

        if "error" in json_resp:
            return json_resp["error"]["message"]
        if "responses" in json_resp:
            return json.dumps(json_resp["responses"])

    except Exception as e:
        return str(e)

#########################################################
#      FUNCION LECTURA DE OCR-TESSERACT POR IMG         #
#########################################################

def extraer_texto_desde_imagen(ruta_imagen, path_tesseract):
    if os.path.exists(ruta_imagen):
        try:
            # Configura la ruta de Tesseract OCR
            pytesseract.pytesseract.tesseract_cmd = os.path.join(path_tesseract, 'tesseract.exe')

            # Lee la imagen y aplica el OCR
            imagen = cv2.imread(ruta_imagen)
            imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            _, imagen_umbral = cv2.threshold(imagen_gris, 200, 255, cv2.THRESH_BINARY)
            texto_extraido = pytesseract.image_to_string(imagen_umbral)

            # Elimina la imagen
            try:
                os.remove(ruta_imagen)
            except Exception as e:
                print(f"No se pudo eliminar el archivo PNG: {str(e)}")

            return texto_extraido
        except Exception as e:
            print(f"Error al procesar la imagen: {str(e)}")
            return None
    else:
        print(f"El archivo de imagen '{ruta_imagen}' no existe. No se realizó ninguna operación.")
        return None

#########################################################
#    FUNCION PARA REALIZAR CLICK POR IMAGEN-CENTER      #
#########################################################

def hacer_clic_en_imagen(img_path, seg, confidence=0.7, region=(0, 0, 1920, 1080)):
    global temporizador_personalizado
    try:
        temporizador_personalizado(seg)
        posicion_parte = pyautogui.locateOnScreen(img_path, confidence=confidence, region=region)

        if posicion_parte is not None:
            x, y, ancho, alto = posicion_parte
            centro_x = x + (ancho / 2)
            centro_y = y + (alto / 2)
            pyautogui.click(centro_x, centro_y)

        return (centro_x, centro_y)
        else:
            print(f'La parte de la imagen "{img_path}" no se encontró en la imagen completa.')
    except Exception as e:
        print(f'Se produjo un error: {e}')

#########################################################
#  FUNCION PARA ESPERAR POR IMAGEN CON TIEMPO DESEADO   #
#########################################################

def esperar_y_buscar_imagen(imagen, tiempo_limite, seg):
    global time
    tiempo_inicio = time.time()
    while time.time() - tiempo_inicio < tiempo_limite:
        try:
            x, y = pyautogui.center(pyautogui.locateOnScreen(imagen, confidence=0.7))
            print(f'Imagen "{imagen}" encontrada')
            return x, y
        except:
            pass
        temporizador_personalizado(seg)
    print(f'Imagen "{imagen}" no encontrada')
    return None, None
    
#########################################################
#          FUNCION PARA CAPTURA DE IMG DESEADO          #
#########################################################

def obtener_screenshot_si_existe(imagen_cancel_edge, distancia_deseada, margen_derecho, altura, distancia_alt_baj, imagen_path, seg): #distancia_deseada, margen_derecho,
    #print(imagen_cancel_edge, distancia_deseada, margen_derecho, altura, imagen_path, seg)
    global esperar_y_buscar_imagen
    x_cancel, y_cancel = esperar_y_buscar_imagen(imagen_cancel_edge, 10.0, 1.0)
    if x_cancel is not None and y_cancel is not None:
        try:
            # Calcula las coordenadas de la región en función de la distancia
            #distancia_deseada = 200
            #margen_derecho = 200
            left = int(x_cancel - distancia_deseada)
            #top = y_cancel + 9  # Ajusta esta distancia hacia abajo según sea necesario
            top = y_cancel + distancia_alt_baj
            width = int(distancia_deseada + margen_derecho)
            height = altura  # Ajusta el valor según sea necesario 70
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            screenshot.save(imagen_path)
            
            temporizador_personalizado(seg)
        except Exception as e:
            print(f"Error al obtener la imagen: {str(e)}")
    else:
        print(f"No se encontró la imagen : {imagen_path}")


#########################################################
#      FUNCION PARA EXTRAER EL DATO DE LA IMG-OCR       #
#########################################################

def extraer_data_y_eliminar_imagen(api_key, imagen_path):
    #global funciones
    global ocr_google_cloud
    global json
    try:
        # Extrae la data del data table de codeudores
        resultado = ocr_google_cloud(api_key, imagen_path)
        data = json.loads(resultado)
        #print("Datos extraido con OCR-Google :", data)
        if data and data[0].get("textAnnotations"):
            text = data[0]["textAnnotations"][0]["description"]
            Codeudores = text.split('\n')
            #print("Data extraída exitosamente text:", text)
            print("Data extraída exitosamente.", Codeudores)
            try:
                # Elimina la imagen
                #os.remove(imagen_path)
                print(f"Imagen '{imagen_path}' eliminada exitosamente.")
            except FileNotFoundError:
                print(f"La imagen '{imagen_path}' no existe.")
            except Exception as e:
                print(f"No se pudo eliminar la imagen: {str(e)}")
            
            return Codeudores
        else:
            print("No se encontró ningún resultado de OCR.")
            return None
    except Exception as e:
        print(f"Error al extraer la data: {str(e)}")
        return None

#########################################################
#     FUNCION PARA EXTRAER IMG DE 2CAPTCHA NETBANK      #
#########################################################

def capturar_imagen_seguridad(x_segurity, y_segurity, img_2captcha,seg):
    if x_segurity is not None and y_segurity is not None:
        try:
            temporizador_personalizado(seg)
            region = (x_segurity + 78, y_segurity - 15.8, 130, 27)
            screenshot = pyautogui.screenshot(region=region)
            screenshot.save(img_2captcha)
            temporizador_personalizado(seg)
            print("Imagen de seguridad capturada exitosamente.")
        except Exception as e:
            print(f"Error al obtener la imagen: {str(e)}")
    else:
        print("No se encontró la imagen 'img_segurity.png'")

#########################################################
#    FUNCION PARA CAPTURAR IMG ERROR SESSION NETBANK    #
#########################################################

def capturar_imagen_error_session(x_cancel, y_cancel, guardar_img_sesion_error, seg):
    if x_cancel is not None and y_cancel is not None:
        try:
            # Calcula la distancia deseada y el margen derecho
            distancia_deseada = 150  # Ajusta según sea necesario
            margen_derecho = 170  # Ajusta según sea necesario

            # Calcula las coordenadas de la región en función de la distancia
            left = int(x_cancel - distancia_deseada)
            top = y_cancel + 48  # Ajusta esta distancia hacia abajo según sea necesario
            width = int(distancia_deseada + margen_derecho)
            height = 60  # Ajusta según sea necesario
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            screenshot.save(guardar_img_sesion_error)
            
            temporizador_personalizado(seg)
            print("Imagen capturada exitosamente.")
        except Exception as e:
            print(f"Error al obtener la imagen: {str(e)}")
    else:
        print("No se encontró la imagen 'Cancel_Netbank.png'")

#########################################################
#       FUNCION PARA REALIZAR CLICK CON EL MAUSE        #
#########################################################

def mover_mause_y_click(imagen_objetivo, desplazamiento_x):
    global esperar_y_buscar_imagen
    try:
        x, y = esperar_y_buscar_imagen(imagen_objetivo, tiempo_limite=10, seg=1)
        
        if x is not None and y is not None:
            nueva_x = x + desplazamiento_x
            nueva_y = y
            pyautogui.moveTo(nueva_x, nueva_y, duration=0.2)
            # Realizar un clic o alguna otra acción si es necesario
            pyautogui.click()
            return True
        else:
            print("La imagen objetivo no se encontró en el tiempo especificado.")
            return False
    except Exception as e:
        print(f"Se produjo una excepción: {str(e)}")

#########################################################
#  FUNCION PARA OBTENER DATOS DE GARANTES Y CODEUDORES  #
#########################################################

def procesar_datos_img_Table(img_referencia, api_key, imagen_cancel_edge, distancia_deseada, margen_derecho, altura, distancia_alt_baj, imagen_path):
    global hacer_clic_en_imagen
    global obtener_screenshot_si_existe
    global extraer_data_y_eliminar_imagen
    try:
        hacer_clic_en_imagen(img_referencia, 3)
        obtener_screenshot_si_existe(imagen_cancel_edge,distancia_deseada, margen_derecho, altura, distancia_alt_baj, imagen_path, 5)
        data_OCR = extraer_data_y_eliminar_imagen(api_key, imagen_path)
        return data_OCR
    except Exception as e:
        print(f'Se produjo un error: {e}')
        return None

#########################################################
#    FUNCION PARA CAPTURAR IMG Y OBTENER OCR-GOOGLE     #
#########################################################
def procesar_datos_img(api_key, imagen_cancel_edge, distancia_deseada, margen_derecho, altura, distancia_alt_baj, imagen_path):
    global obtener_screenshot_si_existe
    global extraer_data_y_eliminar_imagen
    try:
        obtener_screenshot_si_existe(imagen_cancel_edge,distancia_deseada, margen_derecho, altura, distancia_alt_baj, imagen_path, 5)
        data_OCR = extraer_data_y_eliminar_imagen(api_key, imagen_path)
        return data_OCR
    except Exception as e:
        print(f'Se produjo un error: {e}')
        return None

# Uso de la funciones ejemplo
"""try:
    hacer_clic_en_imagen(img_codeudor_referencia)
    distancia_deseada = 200
    margen_derecho = 200
    obtener_screenshot_si_existe(imagen_cancel_edge, distancia_deseada, margen_derecho)
    extraer_data_y_eliminar_imagen(api_key, imagen_path)
except Exception as e:
    print(f'Se produjo un error: {e}')"""
