"""
Generador de Contraseñas Personalizado con GUI

Este programa permite al usuario generar contraseñas seguras basadas en sus preferencias:
- Longitud de la contraseña
- Incluir números
- Incluir símbolos especiales
- Tema de la contraseña (ej: trabajo, personal, juegos)
- Pista personal para recordar la contraseña

La contraseña generada puede ser copiada al portapapeles y guardada en un archivo de texto opcionalmente.

Autor: [Tu Nombre]
Fecha: [Fecha]
"""

import tkinter as tk
from tkinter import messagebox
import random
import string

# ----------------------------- FUNCIONES ----------------------------- #
def generar_contraseña():
    """
    Genera una contraseña según las preferencias del usuario.
    """
    longitud = int(entry_longitud.get())
    incluir_numeros = var_numeros.get()
    incluir_simbolos = var_simbolos.get()
    tema = entry_tema.get()
    pista = entry_pista.get()

    # Base de caracteres
    caracteres = string.ascii_letters  # Letras mayúsculas y minúsculas
    if incluir_numeros:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += string.punctuation

    # Generación de la contraseña
    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    contraseña_completa = f"{contraseña} ({tema})"

    # Mostrar la contraseña en el campo
    entry_resultado.delete(0, tk.END)
    entry_resultado.insert(0, contraseña_completa)

    # Guardar la contraseña con su pista en un archivo
    with open("contraseñas_guardadas.txt", "a") as f:
        f.write(f"Contraseña: {contraseña_completa} | Pista: {pista}\n")

    messagebox.showinfo("Contraseña Generada", "¡Contraseña generada y guardada con éxito!")

# ----------------------------- INTERFAZ GRÁFICA ----------------------------- #
# Crear ventana principal
ventana = tk.Tk()
ventana.title("Generador de Contraseñas Personalizado")
ventana.geometry("500x400")
ventana.config(bg="#f0f0f0")

# Título
tk.Label(ventana, text="Generador de Contraseñas", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

# Longitud de la contraseña
tk.Label(ventana, text="Longitud de la contraseña:", bg="#f0f0f0").pack()
entry_longitud = tk.Entry(ventana)
entry_longitud.pack()

# Incluir números
var_numeros = tk.BooleanVar()
tk.Checkbutton(ventana, text="Incluir números", variable=var_numeros, bg="#f0f0f0").pack()

# Incluir símbolos
var_simbolos = tk.BooleanVar()
tk.Checkbutton(ventana, text="Incluir símbolos", variable=var_simbolos, bg="#f0f0f0").pack()

# Tema de la contraseña
tk.Label(ventana, text="Tema de la contraseña (ej: trabajo, personal):", bg="#f0f0f0").pack()
entry_tema = tk.Entry(ventana)
entry_tema.pack()

# Pista personal
tk.Label(ventana, text="Pista personal para recordar la contraseña:", bg="#f0f0f0").pack()
entry_pista = tk.Entry(ventana)
entry_pista.pack()

# Botón para generar contraseña
tk.Button(ventana, text="Generar Contraseña", command=generar_contraseña, bg="#4CAF50", fg="white", font=("Helvetica", 12)).pack(pady=10)

# Resultado
tk.Label(ventana, text="Contraseña generada:", bg="#f0f0f0").pack()
entry_resultado = tk.Entry(ventana, width=50)
entry_resultado.pack(pady=5)

# Ejecutar ventana
ventana.mainloop()
