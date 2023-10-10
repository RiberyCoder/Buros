import os
import configparser

config_file_path = '{rutaPadre}/config/router_config.ini'
robot = "{robot}" 
print(robot)
print("{ruta_txt}")
print("{ruta_xml}")
# Verificar si existe el archivo
if os.path.exists(config_file_path):
  # Leer el archivo
  config = configparser.ConfigParser()
  config.read(config_file_path)

  # Verificar si existe la sección 
  if 'RUTAS' in config:
    if robot  == 'ASFI':
        config['RUTAS']['ruta_txt'] = "{ruta_txt}"  
    elif robot == 'INFOCRED':
        config['RUTAS']['ruta_xml'] = "{ruta_xml}"
    elif robot == 'BUROS':
        config['RUTAS']['ruta_txt'] = "{ruta_txt}"
        config['RUTAS']['ruta_xml'] = "{ruta_xml}"
  else:
    # Agregar sección completa
    config['RUTAS'] = {
      'ruta_txt': "{ruta_txt}",
      'ruta_xml': "{ruta_xml}"
    }
    print("Archivo actualizado")
else:
  # Crear objeto de configuración
  config = configparser.ConfigParser()
  # Agregar sección completa
  config['RUTAS'] = {
    'ruta_txt': "{ruta_txt}",
    'ruta_xml': "{ruta_xml}" 
  }
  
# Guardar archivo actualizado
with open(config_file_path, 'w') as f:
  config.write(f)  

print("Archivo Creado")
