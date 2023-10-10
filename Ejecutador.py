import subprocess

ruta_archivo_py = "D:/AD/DESEMBOLSO/scripts/inilee.py"

result = subprocess.run(["python", ruta_archivo_py], stdout=subprocess.PIPE, universal_newlines=True)
if result.returncode == 0:
    salida_estandar = result.stdout.strip()
    lineas = salida_estandar.split('\n')
    for linea in lineas:
        partes = linea.split('=')
        if len(partes) == 2:
            clave, valor_desencriptado = partes[0], partes[1]
            SetVar(f"{clave}", valor_desencriptado)

else:
    print(f"Error al ejecutar el script. Código de retorno: {result.returncode}")
    print("Salida de error:")
    print(result.stderr)
