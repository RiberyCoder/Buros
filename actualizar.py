import os

directorio_base = "D:\\AD"

while True:
    # Solicitar al usuario elegir entre cambiar todos los campos o un campo específico
    opcion = input("¿Desea cambiar todos los campos (T) o un campo específico (E)? (T/E): ").strip().lower()
    if opcion == 't':
        # Solicitar al usuario ingresar los nuevos valores para todos los campos
        bdUsuarioBuros = input("Ingrese el nuevo valor para bdUsuarioBuros: ")
        bdPassBuros = input("Ingrese el nuevo valor para bdPassBuros: ")
        correoUser1 = input("Ingrese el nuevo valor para correoUser1: ")
        correoUser2 = input("Ingrese el nuevo valor para correoUser2: ")
        correoUser3 = input("Ingrese el nuevo valor para correoUser3: ")
        correoUser4 = input("Ingrese el nuevo valor para correoUser4: ")
        correo1 = input("Ingrese el nuevo valor para correo1: ")
        correo2 = input("Ingrese el nuevo valor para correo2: ")
        correo3 = input("Ingrese el nuevo valor para correo3: ")
        correo4 = input("Ingrese el nuevo valor para correo4: ")
        passCorreo = input("Ingrese el nuevo valor para passCorreo: ")
        passCorreo1 = input("Ingrese el nuevo valor para passCorreo1: ")
        serverCorreo = input("Ingrese el nuevo valor para serverCorreo: ")
        serverIp = input("Ingrese el nuevo valor para serverIp: ")
        copiaCorreo = input("Ingrese el nuevo valor para copiaCorreo: ")


    elif opcion == 'e':
        # Solicitar al usuario ingresar el nombre del campo específico
        campo_especifico = input("Ingrese el nombre del campo específico que desea cambiar: ")

        # Solicitar al usuario ingresar el nuevo valor para el campo específico
        nuevo_valor = input(f"Ingrese el nuevo valor para {campo_especifico}: ")

    else:
        print("Opción no válida. Por favor, ingrese 'T' para cambiar todos los campos o 'E' para un campo específico.")
        continue

    # Solicitar confirmación para iniciar el proceso
    confirmacion_inicial = input("¿Está seguro de actualizar los archivos? (S/N): ").strip().lower()

    if confirmacion_inicial != 's':
        print("Proceso cancelado.")
        break  # Salir del bucle while si el usuario elige no continuar

    # Iterar a través de las carpetas BUROS_01 a BUROS_10
    for i in range(1, 11):
        carpeta = f"BUROS_{i:02}"  # Generar el nombre de la carpeta con formato "BUROS_XX"
        ruta_config = os.path.join(directorio_base, carpeta, "scripts", "config_buros.ini")

        # Manejo de errores al intentar abrir el archivo
        try:
            with open(ruta_config, 'r') as archivo:
                lineas = archivo.readlines()
        except FileNotFoundError:
            print(f"Archivo no encontrado en {ruta_config}. Saltando esta carpeta.")
            continue

        # Crear un diccionario para almacenar los campos y valores actuales
        campos_actuales = {}
        for linea in lineas:
            if '=' in linea:
                campo, valor = linea.strip().split('=', 1)
                campos_actuales[campo.strip()] = valor.strip()

        # Modificar los campos específicos si se eligió la opción "E"
        if opcion == 'e':
            campos_actuales[campo_especifico] = nuevo_valor

            # Si el campo específico no existe en el archivo, agrégalo al final
            if campo_especifico not in campos_actuales:
                campos_actuales[campo_especifico] = nuevo_valor

        # Modificar todos los campos si se eligió la opción "T"
        elif opcion == 't':
            campos_a_modificar = {
                "bdServidorBuros": bdServidorBuros,
                "bdNombreBuros": bdNombreBuros,
                "bdUsuarioBuros": bdUsuarioBuros,
                "bdPassBuros": bdPassBuros,
                "correoUser1": correoUser1,
                "correoUser2": correoUser2,
                "correoUser3": correoUser3,
                "correoUser4": correoUser4,
                "correo1": correo1,
                "correo2": correo2,
                "correo3": correo3,
                "correo4": correo4,
                "passCorreo": passCorreo,
                "passCorreo1": passCorreo1,
                "serverCorreo": serverCorreo,
                "serverIp": serverIp,
                "copiaCorreo": copiaCorreo
            }
            
            for campo, nuevo_valor in campos_a_modificar.items():
                campos_actuales[campo] = nuevo_valor

        # Guardar los cambios en el archivo
        with open(ruta_config, 'w') as archivo:
            for campo, valor in campos_actuales.items():
                archivo.write(f"{campo} = {valor}\n")

        print(f"Se han actualizado los valores en {ruta_config}")

    # Solicitar confirmación para continuar
    confirmacion_final = input("¿Desea continuar con otra actividad? (S/N): ").strip().lower()

    if confirmacion_final != 's':
        print("Proceso finalizado.")
        break  # Salir del bucle while si el usuario elige no continuar
