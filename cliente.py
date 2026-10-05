import requests

URL_BASE = "http://127.0.0.1:5000"

sesion = requests.Session()

def registrar():

    print("\n--- REGISTRO DE USUARIO ---")

    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    datos = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    respuesta = sesion.post(
        f"{URL_BASE}/registro",
        json=datos
    )

    print("\nRespuesta del servidor:")

    print(respuesta.json())

def login():

    print("\n--- INICIO DE SESIÓN ---")

    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    datos = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    respuesta = sesion.post(
        f"{URL_BASE}/login",
        json=datos
    )

    print("\nRespuesta del servidor:")

    print(respuesta.json())

def ver_tareas():

    print("\n--- TAREAS ---")

    respuesta = sesion.get(
        f"{URL_BASE}/tareas"
    )

    if respuesta.status_code == 200:
        print(respuesta.text)

    else:
        print(respuesta.json())

def logout():

    print("\n--- CERRAR SESIÓN ---")

    respuesta = sesion.post(
        f"{URL_BASE}/logout"
    )

    print(respuesta.json())

def mostrar_menu():

    print("\n==============================")
    print("   SISTEMA DE GESTIÓN")
    print("==============================")

    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Ver tareas")
    print("4. Cerrar sesión")
    print("5. Salir")

    return input("\nSeleccione una opción: ")

while True:

    opcion = mostrar_menu()

    if opcion == "1":
        registrar()

    elif opcion == "2":
        login()

    elif opcion == "3":
        ver_tareas()

    elif opcion == "4":
        logout()

    elif opcion == "5":
        print("\nPrograma finalizado.")
        break

    else:
        print("\nOpción incorrecta.")