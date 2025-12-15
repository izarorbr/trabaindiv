import tkinter as tk
from game import NonogramGame

if __name__ == '__main__': # Punto de entrada principal del programa
    root = tk.Tk() # Crea la ventana principal de la aplicación
    app = NonogramGame(root) # Inicializa la clase del juego NonogramGame
    root.mainloop() # Inicia el bucle principal de la interfaz gráfiñca
