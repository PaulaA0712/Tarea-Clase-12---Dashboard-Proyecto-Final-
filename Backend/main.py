# main.py

import os
from paquetes import Paquete
from envios import EnvioDB

# ==============================================================================
# RUTA DINÁMICA
# ==============================================================================

DB_NAME = os.path.join(os.path.dirname(__file__), "ruta_optima.db")

# ==============================================================================
# CREAR BASE DE DATOS
# ==============================================================================

def crear_base_datos():

    if not os.path.exists(DB_NAME):
        print("📁 Creando base de datos...")

    db = EnvioDB(DB_NAME)
    db.crear_tabla()

# ==============================================================================
# REGISTRAR ENVÍO
# ==============================================================================

def registrar_envio():

    try:

        id_cliente = int(input("Ingrese ID cliente: "))

        peso = float(input("Ingrese peso (kg): "))

        if peso <= 0:
            print("❌ El peso debe ser positivo")
            return

        destino = input("Ingrese destino: ").strip()

        if destino == "":
            print("❌ Destino no válido")
            return

        paquete = Paquete(peso, destino)

        costo = paquete.calcular_costo()

        db = EnvioDB(DB_NAME)

        db.insertar(
            id_cliente,
            peso,
            destino,
            paquete.tipo,
            costo
        )

        print(f"✅ Registrado: {paquete.tipo} - ${costo}")

    except ValueError:
        print("❌ Error: ingrese un dato válido")

# ==============================================================================
# VER ENVÍOS
# ==============================================================================

def ver_envios():

    db = EnvioDB(DB_NAME)

    datos = db.consultar()

    print("\n📦 MANIFIESTO DE ENVÍOS:")

    for d in datos:
        print(d)

# ==============================================================================
# ACTUALIZAR ENVÍO
# ==============================================================================

def actualizar_envio():

    try:

        id_envio = int(input("Ingrese ID del envío: "))

        nuevo_destino = input("Nuevo destino: ").strip()

        db = EnvioDB(DB_NAME)

        db.actualizar(id_envio, nuevo_destino)

        print("✅ Envío actualizado")

    except ValueError:
        print("❌ Error de digitación")

# ==============================================================================
# ELIMINAR ENVÍO
# ==============================================================================

def eliminar_envio():

    try:

        id_envio = int(input("Ingrese ID del envío a eliminar: "))

        db = EnvioDB(DB_NAME)

        db.eliminar(id_envio)

        print("🗑️ Envío eliminado")

    except ValueError:
        print("❌ Error de digitación")

# ==============================================================================
# MENÚ
# ==============================================================================

def menu():

    while True:

        print("\n========== MENÚ ==========")
        print("1. Registrar envío")
        print("2. Ver envíos")
        print("3. Actualizar envío")
        print("4. Eliminar envío")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_envio()

        elif opcion == "2":
            ver_envios()

        elif opcion == "3":
            actualizar_envio()

        elif opcion == "4":
            eliminar_envio()

        elif opcion == "5":
            print("👋 Saliendo del sistema...")
            break

        else:
            print("❌ Opción inválida")

# ==============================================================================
# EJECUCIÓN
# ==============================================================================

if __name__ == "__main__":

    crear_base_datos()

    menu()