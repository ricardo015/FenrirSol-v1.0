import subprocess

import tkinter as tk

from tkinter import messagebox

import webbrowser

import pyperclip

import threading

import time

import re





# Ejecutar el actualizador antes de iniciar la aplicación

def ejecutar_updater():

    """

    Ejecuta el script updater.py para verificar y actualizar la aplicación.

    """

    try:

        print("Verificando actualizaciones...")

        resultado = subprocess.run(["python", "updater.py"], check=True)

        if resultado.returncode == 0:

            print("El actualizador se ejecutó correctamente.")

        else:

            print("Hubo un problema con el actualizador.")

    except Exception as e:

        print(f"Error al ejecutar el actualizador: {e}")



# Llamar al updater antes de iniciar la interfaz gráfica

ejecutar_updater()



# Variables globales para controlar el estado del monitoreo

monitoreo_activo = False

contenido_anterior = ""

contratos_abiertos = set()  # Para validar contratos únicos



# Resto de tu código sigue igual...

# Aquí inicia tu función crear_interfaz() y demás funciones.



# Variables globales para controlar el estado del monitoreo



monitoreo_activo = False



contenido_anterior = ""



contratos_abiertos = set()  # Para validar contratos únicos







# Validar si el contrato es válido



def es_contrato_valido(contrato):



    base58_regex = r'^[A-HJ-NP-Za-km-z1-9]{32,44}$'



    return re.match(base58_regex, contrato) is not None







# Abrir las páginas en Brave



def abrir_paginas_brave(contrato):



    urls = [



       f"https://rugcheck.xyz/tokens/{contrato}",



       f"https://bullx.io/terminal?chainId=1399811149&address={contrato}"



    ]







    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"



    webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))







    for url in urls:



        webbrowser.get('brave').open(url)



        time.sleep(1)







    print(f"Páginas abiertas para el contrato: {contrato}")







# Función para monitorear el portapapeles



def monitorear_portapapeles(texto_contrato):



    global monitoreo_activo, contenido_anterior, contratos_abiertos







    while monitoreo_activo:



        try:



            contenido_actual = pyperclip.paste().strip()



        except Exception as e:



            print(f"Error al leer el portapapeles: {e}")



            contenido_actual = ""







        if contenido_actual != contenido_anterior and contenido_actual:



            if es_contrato_valido(contenido_actual):



                if contenido_actual not in contratos_abiertos:  # Validar contrato único



                    contenido_anterior = contenido_actual



                    contratos_abiertos.add(contenido_actual)



                    texto_contrato.set(f"Contrato detectado: {contenido_actual}")



                    print(f"Nuevo contrato detectado: {contenido_actual}")



                    abrir_paginas_brave(contenido_actual)



                else:



                    texto_contrato.set("Contrato ya procesado.")



            else:



                texto_contrato.set("El contenido copiado no es un contrato válido.")







        time.sleep(1)







# Iniciar monitoreo



def iniciar_monitoreo(texto_contrato):



    global monitoreo_activo



    if not monitoreo_activo:



        monitoreo_activo = True



        texto_contrato.set("Monitoreo activado.")



        threading.Thread(target=monitorear_portapapeles, args=(texto_contrato,), daemon=True).start()



        messagebox.showinfo("Monitoreo", "El monitoreo del portapapeles ha comenzado.")



    else:



        messagebox.showinfo("Monitoreo", "El monitoreo ya está activo.")







# Pausar monitoreo



def pausar_monitoreo(texto_contrato):



    global monitoreo_activo



    if monitoreo_activo:



        monitoreo_activo = False



        texto_contrato.set("Monitoreo pausado.")



        messagebox.showinfo("Monitoreo", "El monitoreo del portapapeles se ha pausado.")



    else:



        messagebox.showinfo("Monitoreo", "El monitoreo ya está pausado.")







# Salir del programa



def salir(ventana):



    global monitoreo_activo



    monitoreo_activo = False



    ventana.destroy()



# Crear interfaz gráfica



def crear_interfaz():



    ventana = tk.Tk()



    ventana.title("Fenrir v1.0 - Solana")



    ventana.geometry("400x200")



    



    # Texto para mostrar el contrato detectado



    texto_contrato = tk.StringVar()



    texto_contrato.set("Estado: Esperando contrato de solana...")







    etiqueta_contrato = tk.Label(ventana, textvariable=texto_contrato, wraplength=380, justify="center")



    etiqueta_contrato.pack(pady=10)







    # Botones



    boton_iniciar = tk.Button(ventana, text="Iniciar Monitoreo", command=lambda: iniciar_monitoreo(texto_contrato), width=20)



    boton_iniciar.pack(pady=5)







    boton_pausar = tk.Button(ventana, text="Pausar Monitoreo", command=lambda: pausar_monitoreo(texto_contrato), width=20)



    boton_pausar.pack(pady=5)







    boton_salir = tk.Button(ventana, text="Salir", command=lambda: salir(ventana), width=20, bg="red", fg="white")



    boton_salir.pack(pady=10)







    ventana.mainloop()







if __name__ == "__main__":



    crear_interfaz()

