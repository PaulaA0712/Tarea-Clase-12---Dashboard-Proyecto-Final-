# envios.py

import sqlite3


class EnvioDB:

    def __init__(self, db_name):
        self.db_name = db_name

    # ==========================================================================
    # CONEXIÓN
    # ==========================================================================

    def conectar(self):
        return sqlite3.connect(self.db_name)

    # ==========================================================================
    # CREAR TABLAS
    # ==========================================================================

    def crear_tabla(self):

        conn = self.conectar()
        cursor = conn.cursor()

        # ----------------------------------------------------------------------
        # TABLA CLIENTES (DIMENSIÓN)
        # ----------------------------------------------------------------------

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL
        )
        """)

        # ----------------------------------------------------------------------
        # TABLA ENVIOS (HECHOS)
        # ----------------------------------------------------------------------

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS envios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            peso REAL,
            destino TEXT,
            tipo TEXT,
            costo REAL,

            FOREIGN KEY(id_cliente)
            REFERENCES clientes(id_cliente)
        )
        """)

        conn.commit()
        conn.close()

    # ==========================================================================
    # CREATE
    # ==========================================================================

    def insertar(self, id_cliente, peso, destino, tipo, costo):

        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO envios (
            id_cliente,
            peso,
            destino,
            tipo,
            costo
        )
        VALUES (?, ?, ?, ?, ?)
        """, (id_cliente, peso, destino, tipo, costo))

        conn.commit()
        conn.close()

    # ==========================================================================
    # READ
    # ==========================================================================

    def consultar(self):

        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            envios.id,
            clientes.nombre,
            envios.peso,
            envios.destino,
            envios.tipo,
            envios.costo

        FROM envios

        LEFT JOIN clientes
        ON envios.id_cliente = clientes.id_cliente

        ORDER BY envios.peso DESC
        """)

        datos = cursor.fetchall()

        conn.close()

        return datos

    # ==========================================================================
    # UPDATE
    # ==========================================================================

    def actualizar(self, id_envio, nuevo_destino):

        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE envios
        SET destino = ?
        WHERE id = ?
        """, (nuevo_destino, id_envio))

        conn.commit()
        conn.close()

    # ==========================================================================
    # DELETE
    # ==========================================================================

    def eliminar(self, id_envio):

        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM envios
        WHERE id = ?
        """, (id_envio,))

        conn.commit()
        conn.close()