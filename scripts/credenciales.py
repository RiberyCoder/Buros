import os

# Directorio base
directorio_base = "D:\\AD"

while True:
    # Solicita al usuario ingresar los nuevos valores
    nuevo_correo_user = input("Ingrese el nuevo correoUser: ")
    nueva_pass_correo = input("Ingrese la nueva passCorreo: ")

    # Solicita confirmación para iniciar el proceso
    confirmacion_inicial = input("¿Está seguro de actualizar los archivos? (S/N): ").strip().lower()

    if confirmacion_inicial != 's':
        print("Proceso cancelado.")
    else:
        for i in range(1, 11):
            carpeta = f"BUROS_{i:02}"
            ruta_config = os.path.join(directorio_base, carpeta, "scripts", "config_buros.ini")

            # Abre y modifica el archivo config_buros.ini
            with open(ruta_config, 'r') as archivo:
                lineas = archivo.readlines()

            for j in range(len(lineas)):
                if lineas[j].startswith("correoUser ="):
                    lineas[j] = f"correoUser = {nuevo_correo_user}\n"
                elif lineas[j].startswith("passCorreo ="):
                    lineas[j] = f"passCorreo = {nueva_pass_correo}\n"

            # Guarda los cambios en el archivo
            with open(ruta_config, 'w') as archivo:
                archivo.writelines(lineas)

            print(f"Se han actualizado los valores en {ruta_config}")

        confirmacion_final = input("¿Desea continuar con otra actividad? (S/N): ").strip().lower()

        if confirmacion_final != 's':
            print("Proceso finalizado.")
            break