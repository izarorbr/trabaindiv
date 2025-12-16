import tkinter as tk
from game import NonogramGame

"""
Este programa es un juego de Nonogramas creado con Tkinter.
Permite seleccionar la dificultad, jugar rellenando la cuadrícula según las pistas
y además muestra un cronómetro durante la partida.
Al finalizar correctamente el puzzle, el tiempo se guarda en un ranking
de mejores puntuaciones por nivel.
Incluye opciones para reiniciar, resolver el tablero y volver al menú principal.
"""

if __name__ == '__main__': # Punto de entrada principal del programa
    root = tk.Tk() # Crea la ventana principal de la aplicación
    app = NonogramGame(root) # Inicializa la clase del juego NonogramGame
    root.mainloop() # Inicia el bucle principal de la interfaz gráfiñca
