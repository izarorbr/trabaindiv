import tkinter as tk
from tkinter import messagebox
import time
import random
from puzzles import generar_pistas, generar_puzzle_por_dificultad
from ranking import cargar_ranking, guardar_ranking

class NonogramGame: # Clase principal del juego Nonograma
    def __init__(self, master):
        self.master = master # Master es la ventana principal de Tkinter
        master.title("Nonogramas") 
        master.resizable(True, True) # Permite redimensionar la ventana

        # Variables del juego que se van a usar
        self.dificultad = None 
        self.matriz_solucion = None
        self.matriz_usuario = None
        self.pistas_filas = None
        self.pistas_columnas = None
        self.dim = 0 
        self.celdas_gui = []
        self.tiempo_inicio = None
        self.cronometro_id = None
        self.celda_seleccionada = None

        # Tamaños unificados para TODO el tablero
        self.CELL_WIDTH = 4
        self.CELL_HEIGHT = 2
        self.FONT_CELL = ('Courier New', 12, 'bold')

        self.mostrar_menu()

    # Menú principal

    def limpiar_ventana(self): # Elimina todos los widgets de la ventana actual, los widgets son los elementos gráficos
        for widget in self.master.winfo_children(): widget.destroy()  # winfo_children significa "obtener todos los hijos del widget"

    def mostrar_menu(self):  # Muestra el menú principal con opciones de dificultad y ranking
        self.limpiar_ventana()
        tk.Label(self.master, text="Selecciona la Dificultad:", font=('Century', 16, 'bold')).pack(pady=20)
        for text, dif, color in [
            ("Fácil (5x5)", "facil", "#e0ffe0"),
            ("Medio (7x7)", "medio", "#ffffcc"),
            ("Difícil (9x9)", "dificil", "#ffcccc")
        ]:
            tk.Button(self.master, text=text, command=lambda d=dif: self.iniciar_juego(d),
                      width=15, height=2, bg=color).pack(pady=10)
        tk.Button(self.master, text="Ver Ranking", command=self.mostrar_ranking,
                  width=15, height=2).pack(pady=20)

    # Juego del Nonograma

    def iniciar_juego(self, dificultad): # Inicializa un nuevo juego con la dificultad seleccionada
        self.dificultad = dificultad
        self.matriz_solucion, self.pistas_filas, self.pistas_columnas = generar_puzzle_por_dificultad(dificultad)
        self.dim = len(self.matriz_solucion)
        self.matriz_usuario = [[0]*self.dim for _ in range(self.dim)]
        self.dibujar_tablero() 
        self.tiempo_inicio = time.time()
        self.actualizar_cronometro() 

    def dibujar_tablero(self): # Dibuja el tablero del nonograma con las pistas y la cuadrícula
        self.limpiar_ventana()
        self.master.title(f"Nonograma - Nivel: {self.dificultad.capitalize()}")

        frame_tablero = tk.Frame(self.master)
        frame_tablero.pack(padx=20, pady=20)

        # Pistas de columnas
        for j in range(self.dim): 
            tk.Label(
                frame_tablero,
                text='\n'.join(map(str, self.pistas_columnas[j])),
                width=self.CELL_WIDTH,
                height=self.CELL_HEIGHT * 2,
                font=self.FONT_CELL,
                borderwidth=1,
                relief="solid",
                justify=tk.CENTER,
                bg='#f0f0f0'
            ).grid(row=0, column=j+1, sticky="nsew")

        # Pistas de filas
        for i in range(self.dim):
            tk.Label(
                frame_tablero,
                text=' '.join(map(str, self.pistas_filas[i])),
                width=self.CELL_WIDTH * 2,
                height=self.CELL_HEIGHT,
                font=self.FONT_CELL,
                borderwidth=1,
                relief="solid",
                justify=tk.CENTER,
                bg='#f0f0f0'
            ).grid(row=i+1, column=0, sticky="nsew")

        # Cuadrícula de juego
        self.celdas_gui = []
        for i in range(self.dim):
            fila = []
            for j in range(self.dim):
                btn = tk.Button(
                    frame_tablero,
                    width=self.CELL_WIDTH,
                    height=self.CELL_HEIGHT,
                    font=self.FONT_CELL,
                    command=lambda r=i, c=j: self.manejar_click(r,c),
                    relief="solid",
                    bd=1,
                    bg='white',
                    highlightthickness=0, # Elimina borde punteado
                    takefocus=False       # Evita foco visual
                )
                btn.grid(row=i+1, column=j+1, sticky="nsew")
                fila.append(btn)
            self.celdas_gui.append(fila)

        # Controles y cronómetro
        frame_controles = tk.Frame(self.master)
        frame_controles.pack(pady=10)

        tk.Button(frame_controles, text="Resolver",
                  command=self.resolver_nonograma,
                  bg='#ff9999', fg='black',
                  font=('Century',12,'bold')).pack(side=tk.LEFT,padx=10)

        tk.Button(frame_controles, text="Resetear Tablero",
                  command=self.borrar_todo,
                  bg='#99ccff', fg='black',
                  font=('Century',12,'bold')).pack(side=tk.LEFT,padx=10)

        tk.Button(frame_controles, text="Menú",
                  command=self.volver_al_menu,
                  font=('Century',12,'bold')).pack(side=tk.LEFT,padx=10)

        self.cronometro_label = tk.Label(
            frame_controles,
            text="Tiempo: 00:00.0",
            font=('Century',12, 'bold')
        )
        self.cronometro_label.pack(side=tk.LEFT,padx=30)

    # Lógica de juego
    def actualizar_celda_seleccionada(self, fila, col): self.celda_seleccionada=(fila,col)

    def manejar_click(self, fila, col):
        self.matriz_usuario[fila][col] = (self.matriz_usuario[fila][col]+1)%3
        self.actualizar_celda_gui(fila,col)
        self.celda_seleccionada=(fila,col)
        if self.matriz_usuario[fila][col]==1: self.comprobar_victoria()

    def actualizar_celda_gui(self, fila, col):
        estado=self.matriz_usuario[fila][col]
        btn=self.celdas_gui[fila][col]
        if estado==1:
            btn.config(bg='black', text='', relief="sunken")
        elif estado==2:
            btn.config(bg='white', text='X', fg='red',
                       font=('Courier New',12,'bold'), relief="raised")
        else:
            btn.config(bg='white', text='', relief="raised")

