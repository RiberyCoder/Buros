import shutil
import os

ruta_origen = r"D:\AD\BUROS\robot\buros.db"
ruta_destino_base = r"D:\AD\BUROS_{:02d}\robot\buros.db"

num_carpetas = 10  # Cambia esto al número de carpetas que tengas

opcion = input("¿Deseas reemplazar en una carpeta específica (S/N)? ").strip().lower()

if opcion == "s":
    numero_carpeta = int(input("Ingrese el número de carpeta en la que desea reemplazar (1-10): "))
    if 1 <= numero_carpeta <= num_carpetas:
        ruta_destino = ruta_destino_base.format(numero_carpeta)
        try:
            if os.path.exists(ruta_destino):
                shutil.copy2(ruta_origen, ruta_destino)  # Reemplazar el archivo
                print(f"Archivo reemplazado en {ruta_destino}")
            else:
                shutil.copy2(ruta_origen, ruta_destino)  # Copiar el archivo
                print(f"Archivo copiado a {ruta_destino}")
        except Exception as e:
            print(f"Error en {ruta_destino}: {e}")
    else:
        print("Número de carpeta fuera de rango.")
else:
    for i in range(1, num_carpetas + 1):
        ruta_destino = ruta_destino_base.format(i)
        try:
            if os.path.exists(ruta_destino):
                shutil.copy2(ruta_origen, ruta_destino)  # Reemplazar el archivo
                print(f"Archivo reemplazado en {ruta_destino}")
            else:
                shutil.copy2(ruta_origen, ruta_destino)  # Copiar el archivo
                print(f"Archivo copiado a {ruta_destino}")
        except Exception as e:
            print(f"Error en {ruta_destino}: {e}")

"""import shutil
import os

ruta_origen = r"D:\AD\BUROS\robot\buros.db"
ruta_destino_base = r"D:\AD\BUROS_{:02d}\robot\buros.db"

num_carpetas = 10  # Cambia esto al número de carpetas que tengas

for i in range(1, num_carpetas + 1):
    ruta_destino = ruta_destino_base.format(i)
    try:
        if os.path.exists(ruta_destino):
            shutil.copy2(ruta_origen, ruta_destino)  # Reemplazar el archivo
            print(f"Archivo reemplazado en {ruta_destino}")
        else:
            shutil.copy2(ruta_origen, ruta_destino)  # Copiar el archivo
            print(f"Archivo copiado a {ruta_destino}")
    except Exception as e:
        print(f"Error en {ruta_destino}: {e}")"""
