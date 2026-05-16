import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import sys

# ==============================================================================
# CONEXIÓN BACKEND
# ==============================================================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'Backend'
        )
    )
)

from Backend.paquetes import Paquete

# ==============================================================================
# RUTA DB
# ==============================================================================

DB_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'Backend',
        'ruta_optima.db'
    )
)

# ==============================================================================
# INTERFAZ
# ==============================================================================

class PantallaEnvios:

    def __init__(self, root):

        self.root = root

        # VENTANA

        self.root.title("Ruta Óptima 🚚")
        self.root.geometry("500x650")
        self.root.configure(bg="#f4f5f9")
        self.root.resizable(False, False)

        # LOGO

        try:

            ruta_logo = os.path.join(
                os.path.dirname(__file__),
                "logo.png"
            )

            img_original = Image.open(ruta_logo)

            img_redimensionada = img_original.resize((180, 180))

            self.logo = ImageTk.PhotoImage(img_redimensionada)

            lbl_logo = tk.Label(
                self.root,
                image=self.logo,
                bg="#f4f5f9"
            )

            lbl_logo.pack(pady=10)

        except Exception:

            tk.Label(
                self.root,
                text="🚚 RUTA ÓPTIMA",
                font=("Arial", 20, "bold"),
                bg="#f4f5f9"
            ).pack(pady=20)

        # TÍTULO

        tk.Label(
            self.root,
            text="Registro de Envíos",
            font=("Arial", 16, "bold"),
            bg="#f4f5f9"
        ).pack(pady=10)

        # ID CLIENTE

        tk.Label(
            self.root,
            text="ID Cliente:",
            bg="#f4f5f9"
        ).pack()

        self.entry_cliente = tk.Entry(
            self.root,
            font=("Arial", 12),
            justify="center"
        )

        self.entry_cliente.pack(pady=5)

        # PESO

        tk.Label(
            self.root,
            text="Peso del paquete (kg):",
            bg="#f4f5f9"
        ).pack()

        self.entry_peso = tk.Entry(
            self.root,
            font=("Arial", 12),
            justify="center"
        )

        self.entry_peso.pack(pady=5)

        # DESTINO

        tk.Label(
            self.root,
            text="Destino:",
            bg="#f4f5f9"
        ).pack()

        self.entry_destino = tk.Entry(
            self.root,
            font=("Arial", 12),
            justify="center"
        )

        self.entry_destino.pack(pady=5)

        # BOTÓN REGISTRAR

        btn_registrar = tk.Button(
            self.root,
            text="📦 Registrar Envío",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            cursor="hand2",
            command=self.registrar_envio
        )

        btn_registrar.pack(
            pady=20,
            fill="x",
            padx=60
        )

        # BOTÓN LIMPIAR

        btn_limpiar = tk.Button(
            self.root,
            text="🧹 Limpiar Campos",
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            cursor="hand2",
            command=self.limpiar_campos
        )

        btn_limpiar.pack(
            fill="x",
            padx=100
        )

    # ==========================================================================
    # REGISTRAR ENVÍO
    # ==========================================================================

    def registrar_envio(self):

        str_cliente = self.entry_cliente.get().strip()
        str_peso = self.entry_peso.get().strip()
        str_destino = self.entry_destino.get().strip()

        try:

            # VALIDACIONES

            if not all([str_cliente, str_peso, str_destino]):
                raise ValueError(
                    "Debe completar todos los campos."
                )

            id_cliente = int(str_cliente)

            peso = float(str_peso)

            if peso <= 0:
                raise ValueError(
                    "El peso debe ser mayor a cero."
                )

            # CLASIFICAR

            paquete = Paquete(peso, str_destino)

            tipo = paquete.tipo

            costo = paquete.calcular_costo()

            # SQLITE

            conexion = sqlite3.connect(DB_PATH)

            cursor = conexion.cursor()

            cursor.execute("""
            INSERT INTO envios (
                id_cliente,
                peso,
                destino,
                tipo,
                costo
            )
            VALUES (?, ?, ?, ?, ?)
            """, (
                id_cliente,
                peso,
                str_destino,
                tipo,
                costo
            ))

            conexion.commit()

            conexion.close()

            # ÉXITO

            messagebox.showinfo(
                "Envío Registrado",
                f"✅ Tipo: {tipo}\n"
                f"💰 Costo: ${costo:,.0f}\n"
                f"📍 Destino: {str_destino}"
            )

            self.limpiar_campos()

        except ValueError as ve:

            messagebox.showwarning(
                "Error",
                str(ve)
            )

        except Exception as e:

            messagebox.showerror(
                "Error Crítico",
                str(e)
            )

    # ==========================================================================
    # LIMPIAR
    # ==========================================================================

    def limpiar_campos(self):

        self.entry_cliente.delete(0, tk.END)
        self.entry_peso.delete(0, tk.END)
        self.entry_destino.delete(0, tk.END)

# ==============================================================================
# EJECUCIÓN
# ==============================================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = PantallaEnvios(root)

    root.mainloop()