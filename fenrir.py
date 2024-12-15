import os
import requests
import subprocess
import sys

# Enlace RAW del archivo en GitHub
URL_SCRIPT_REMOTO = "https://raw.githubusercontent.com/ricardo015/FenrirSol-v1.0/main/fenrir.py"

# Nombre del archivo local y del ejecutable
SCRIPT_LOCAL = "fenrir.py"
EJECUTABLE = "fenrir.exe"

def descargar_y_actualizar():
    """
    Descarga el archivo remoto y lo actualiza localmente si hay cambios.
    """
    try:
        print("Verificando actualizaciones desde GitHub...")
        respuesta = requests.get(URL_SCRIPT_REMOTO)
        if respuesta.status_code == 200:
            contenido_remoto = respuesta.text
        else:
            print(f"Error al descargar el archivo remoto: {respuesta.status_code}")
            return False

        # Si el archivo local existe, comparar con el archivo remoto
        if os.path.exists(SCRIPT_LOCAL):
            with open(SCRIPT_LOCAL, "r") as archivo_local:
                contenido_local = archivo_local.read()
            if contenido_local == contenido_remoto:
                print("El archivo local ya está actualizado.")
                return False

        # Actualizar el archivo local
        with open(SCRIPT_LOCAL, "w") as archivo_local:
            archivo_local.write(contenido_remoto)
        print("El archivo local ha sido actualizado.")
        return True

    except Exception as e:
        print(f"Error durante la actualización: {e}")
        return False

def regenerar_ejecutable():
    """
    Regenera el ejecutable usando PyInstaller.
    """
    comando_pyinstaller = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        SCRIPT_LOCAL
    ]
    print("Regenerando el ejecutable...")
    resultado = subprocess.run(comando_pyinstaller)
    if resultado.returncode == 0:
        print("El ejecutable ha sido actualizado correctamente.")
        return True
    else:
        print("Error al intentar actualizar el ejecutable.")
        return False

if __name__ == "__main__":
    actualizado = descargar_y_actualizar()
    if actualizado:
        if regenerar_ejecutable():
            print("Actualización completada. Reinicia la aplicación para usar la nueva versión.")
            sys.exit(0)  # Salir con éxito
        else:
            print("Error al regenerar el ejecutable.")
            sys.exit(1)  # Salir con error
    else:
        print("No se detectaron cambios. La aplicación está actualizada.")



if __name__ == "__main__":

    crear_interfaz()
