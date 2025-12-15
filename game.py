import tkinter as tk
from tkinter import messagebox
import time
import random
from puzzles import generar_nonograma_unico 
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

        self.CELL_WIDTH = 4
        self.CELL_HEIGHT = 2

        self.mostrar_menu()

    # Menú principal

    def limpiar_ventana(self): # Elimina todos los widgets de la ventana actual, los widgets son los elementos gráficos
        for widget in self.master.winfo_children(): widget.destroy()  # winfo_children significa "obtener todos los hijos del widget"

    def mostrar_menu(self):  # Muestra el menú principal con opciones de dificultad y ranking
        self.limpiar_ventana()
        tk.Label(self.master, text="Selecciona la Dificultad:", font=('Century', 16, 'bold')).pack(pady=20) # Añade un título al menú
        for text, dif, color in [("Fácil (5x5)", "facil", "#e0ffe0"), ("Medio (7x7)", "medio", "#ffffcc"), ("Difícil (9x9)", "dificil", "#ffcccc")]:
            tk.Button(self.master, text=text, command=lambda d=dif: self.iniciar_juego(d), width=15, height=2, bg=color).pack(pady=10)
        tk.Button(self.master, text="Ver Ranking", command=self.mostrar_ranking, width=15, height=2).pack(pady=20)
        # Pady es el espacio vertical entre los elementos, pack() organiza los widgets en la ventana y lambda d=dif crea una función anónima para pasar el parámetro de dificultad
    # Juego del Nonograma

    def iniciar_juego(self, dificultad): # Inicializa un nuevo juego con la dificultad seleccionada
        self.dificultad = dificultad
        self.matriz_solucion, self.pistas_filas, self.pistas_columnas = generar_nonograma_unico(dificultad) # Establece la matriz solución y las pistas
        self.dim = len(self.matriz_solucion) # Dimensión del nonograma
        self.matriz_usuario = [[0]*self.dim for _ in range(self.dim)] # Matriz del usuario inicializada a 0 (vacío)
        self.dibujar_tablero() 
        self.tiempo_inicio = time.time()
        self.actualizar_cronometro() 

    def dibujar_tablero(self): # Dibuja el tablero del nonograma con las pistas y la cuadrícula
        self.limpiar_ventana()
        self.master.title(f"Nonograma - Nivel: {self.dificultad.capitalize()}")
        frame_principal = tk.Frame(self.master) # Contenedor principal para el tablero
        frame_principal.pack(padx=20, pady=20) # Empaqueta el frame con un padding de 20 píxeles, un padding es un espacio alrededor del widget

        # Pistas de columnas
        max_len_col = max(len(p) for p in self.pistas_columnas) # Longitud máxima de pistas de columnas
        frame_col_pistas = tk.Frame(frame_principal); frame_col_pistas.grid(row=0, column=1) # Grid es un gestor de geometría que organiza los widgets en una tabla
        for j in range(self.dim): 
            tk.Label(
                frame_col_pistas,
                text='\n'.join(map(str, self.pistas_columnas[j])), # Une las pistas con saltos de línea
                width=self.CELL_WIDTH,
                height=max_len_col*self.CELL_HEIGHT, # Ancho y alto de la celda
                borderwidth=1, 
                relief="solid", 
                bg='#f0f0f0', 
                justify=tk.CENTER
            ).grid(row=0, column=j) 
                    # Justify alinea el texto al centro, relief define el estilo del borde del widget, borderwidth es el grosor del borde
        # Pistas de filas
        max_len_row = max(len(p) for p in self.pistas_filas) # Longitud máxima de pistas de filas
        frame_row_pistas = tk.Frame(frame_principal); frame_row_pistas.grid(row=1, column=0) # Frame es un contenedor para otros widgets
        for i in range(self.dim): # Itera sobre cada fila 
            tk.Label(frame_row_pistas, 
                text=' '.join(map(str, self.pistas_filas[i])), # Une las pistas con espacios
                width=max_len_row*self.CELL_WIDTH, 
                height=self.CELL_HEIGHT,
                borderwidth=1, relief="solid", 
                bg='#f0f0f0', 
                anchor='c'  # Anchor alinea el texto a la derecha
            ).grid(row=i, column=0) 
                    # Justify alinea el texto al centro, relief define el estilo del borde del widget, borderwidth es el grosor del borde
       
        # Cuadrícula de juego
        frame_juego = tk.Frame(frame_principal); frame_juego.grid(row=1, column=1) # Contenedor para la cuadrícula del juego
        self.celdas_gui = [] # Lista para almacenar los botones de las celdas
        for i in range(self.dim): # Itera sobre cada fila
            fila = []
            for j in range(self.dim): # Itera sobre cada columna
                btn = tk.Button(frame_juego, width=self.CELL_WIDTH, height=self.CELL_HEIGHT,
                                command=lambda r=i, c=j: self.manejar_click(r,c), relief="solid", bd=1, bg='white', padx=0, pady=0, highlightthickness=0, takefocus=False) # Crea un botón para cada celda
                btn.bind("<FocusIn>", lambda e, r=i, c=j: self.actualizar_celda_seleccionada(r,c)) # Bind asocia un evento a una función, en este caso cuando el botón recibe el foco se actualiza la celda seleccionada
                btn.grid(row=i,column=j) # Coloca el botón en la cuadrícula
                fila.append(btn) # Añade el botón a la fila
            self.celdas_gui.append(fila) # Añade la fila a la lista de celdas GUI
        #if self.dim>0:
            #self.celdas_gui[0][0].focus_set(); self.celda_seleccionada=(0,0) # Establece el foco inicial en la primera celda

        # Controles y cronómetro con sus colores, fuentes y estilos
        frame_controles = tk.Frame(self.master); frame_controles.pack(pady=10) # Contenedor para los botones de control
        tk.Button(frame_controles, text="Resolver", command=self.resolver_nonograma, bg='#ff9999', fg='black', font=('Century',12,'bold')).pack(side=tk.LEFT,padx=10)
        tk.Button(frame_controles, text="Resetear Tablero", command=self.borrar_todo, bg='#99ccff', fg='black', font=('Century',12,'bold')).pack(side=tk.LEFT,padx=10)
        tk.Button(frame_controles, text="Menú", command=self.volver_al_menu, font=('Century',12,'bold')).pack(side=tk.LEFT,padx=10)
        self.cronometro_label = tk.Label(frame_controles, text="Tiempo: 00:00.0", font=('Century',12, 'bold'))
        self.cronometro_label.pack(side=tk.LEFT,padx=30)

    # Lógica de juego
    def actualizar_celda_seleccionada(self, fila, col): self.celda_seleccionada=(fila,col) # Actualiza la celda seleccionada
                                                 # col es la columna
    def manejar_click(self, fila, col): # Maneja el clic en una celda del tablero
        self.matriz_usuario[fila][col] = (self.matriz_usuario[fila][col]+1)%3 # Cicla entre 0 (vacío), 1 (relleno), 2 (marcado con X)
        self.actualizar_celda_gui(fila,col) # Actualiza la apariencia de la celda en la GUI
        self.celda_seleccionada=(fila,col) # Actualiza la celda seleccionada
        if self.matriz_usuario[fila][col]==1: self.comprobar_victoria() # Comprueba si el jugador ha ganado tras rellenar una celda

    def actualizar_celda_gui(self, fila, col):
        estado=self.matriz_usuario[fila][col]; btn=self.celdas_gui[fila][col] # Obtiene el estado de la celda y el botón correspondiente
        if estado==1: btn.config(bg='black', text='', relief="sunken") # Configura el botón para celda rellena
        elif estado==2: btn.config(bg='white', text='✕', fg='red', font=('Century',8), padx=0, pady=0) # Configura el botón para celda marcada con X
        else: btn.config(bg='white', text='', relief="raised") # Configura el botón para celda vacía


    def borrar_todo(self): # Resetea todo el progreso del jugador en el tablero
        if messagebox.askyesno("Confirmar Reseteo","¿Quieres resetear todo el progreso?"):
            for i in range(self.dim): # Itera sobre cada fila
                for j in range(self.dim): # Itera sobre cada celda
                    self.matriz_usuario[i][j]=0 # Resetea la celda a vacío
                    self.actualizar_celda_gui(i,j) # Actualiza la apariencia de la celda en la GUI
            messagebox.showinfo("Reseteado","Tablero reseteado a su estado inicial.")

    def comprobar_victoria(self): # Comprueba si el jugador ha completado correctamente el nonograma
        comparacion=[[1 if self.matriz_usuario[i][j]==1 else 0 for j in range(self.dim)] for i in range(self.dim)] # Crea una matriz de comparación con 1 para celdas rellenas y 0 para las demás
        if comparacion==self.matriz_solucion: self.terminar_juego(True) # Si la matriz del jugador coincide con la solución, el juego termina con victoria

    def terminar_juego(self, ganado): # Termina el juego, mostrando el tiempo y guardando en el ranking si es victoria
        if self.cronometro_id: self.master.after_cancel(self.cronometro_id); self.cronometro_id=None # Cancela el cronómetro
        tiempo_final=time.time()-self.tiempo_inicio # Calcula el tiempo final del juego
        if ganado:
            messagebox.showinfo("¡VICTORIA!", f"¡Felicidades! Tiempo: {tiempo_final:.2f} s")
            self.pedir_nombre_y_guardar_ranking(tiempo_final)
        else:
            messagebox.showinfo("Juego Finalizado", f"Juego terminado.\nTiempo: {tiempo_final:.2f} s")

    def pedir_nombre_y_guardar_ranking(self, tiempo): # Pide al jugador su nombre para guardar en el ranking
        win=tk.Toplevel(self.master); win.title("Guardar Puntuación"); win.geometry("300x100") 
        tk.Label(win,text="Introduce tu nombre para el Ranking:").pack(pady=5)
        entry=tk.Entry(win,width=30); entry.pack(pady=5); entry.focus_set() # Entry es un campo de entrada de texto
         # Focus_set establece el foco en el campo de entrada, para que el usuario pueda escribir directamente
        def guardar(): # Guarda el nombre y la puntuación en el ranking
            nombre=entry.get().strip() or "Anónimo" # Obtiene el nombre del campo de entrada, si está vacío usa "Anónimo"
            guardar_ranking(self.dificultad,nombre,tiempo)
            messagebox.showinfo("Ranking","Puntuación guardada.")
            win.destroy(); self.mostrar_ranking() # Destruye la ventana y muestra el ranking actualizado
        tk.Button(win,text="Guardar",command=guardar).pack(pady=10) # Guarda la puntuación al hacer clic en el botón
        win.transient(self.master); win.grab_set(); self.master.wait_window(win) # Hace que la ventana sea modal, es decir, que el usuario debe interactuar con ella antes de volver a la ventana principal
        # Transient hace que la ventana hija esté siempre encima de la ventana padre, grab_set captura todos los eventos para la ventana hija, wait_window espera a que la ventana hija se cierre
    def resolver_nonograma(self, event=None): # Rellena automáticamente el nonograma con la solución
        if messagebox.askyesno("Confirmar Solución","¿Deseas resolver el puzzle?"):
            for i in range(self.dim): 
                for j in range(self.dim):
                    self.matriz_usuario[i][j]=self.matriz_solucion[i][j] # Rellena la celda con la solución
                    self.actualizar_celda_gui(i,j) 
            self.terminar_juego(False) # Termina el juego sin victoria

    def volver_al_menu(self): # Vuelve al menú principal
        if self.cronometro_id: self.master.after_cancel(self.cronometro_id); self.cronometro_id=None # Cancela el cronómetro
        self.mostrar_menu()

    def actualizar_cronometro(self): # Actualiza el cronómetro cada 100 ms
        if self.tiempo_inicio:
            t=time.time()-self.tiempo_inicio
            minutos=int(t//60); segundos=int(t%60); decimas=int((t*10)%10) # Calcula minutos, segundos y décimas de segundo
            self.cronometro_label.config(text=f"Tiempo: {minutos:02}:{segundos:02}.{decimas}")
            self.cronometro_id=self.master.after(100,self.actualizar_cronometro) # Llama a esta función nuevamente después de 100 ms, creando un bucle

    # Ranking de mejores tiempos
    def mostrar_ranking(self): # Muestra el ranking de mejores tiempos en una nueva ventana
        win=tk.Toplevel(self.master); win.title("Ranking de Mejores Tiempos"); win.geometry("500x450") # Crea una ventana secundaria
         # Toplevel crea una nueva ventana hija, geometry establece el tamaño de la ventana
        tk.Label(win,text="🏆Top 10 Mejores Tiempos 🏆", font=('Century',18,'bold')).pack(pady=10) # 
        for dificultad in ['facil','medio','dificil']: # Itera sobre cada nivel de dificultad
            ranking=cargar_ranking(dificultad) # Carga el ranking para la dificultad actual
            frame=tk.Frame(win,padx=10,pady=5,borderwidth=1,relief="groove"); frame.pack(pady=10) # Crea un frame para cada dificultad
             # Groove crea un borde con efecto de ranura
            tk.Label(frame,text=f"Nivel: {dificultad.capitalize()}", font=('Century',12,'underline')).pack()
            if not ranking: tk.Label(frame,text="Aún no hay puntuaciones registradas.").pack(); continue # Si no hay puntuaciones, muestra un mensaje
             # Capitalize convierte la primera letra a mayúscula, underline subraya el texto
            for i,e in enumerate(ranking): 
                tk.Label(frame,text=f"#{i+1}. {e['nombre']} - {e['tiempo']:.2f} s", anchor='c', width=40).pack() # Muestra cada entrada del ranking
                 # Anchor alinea el texto a la izquierda, width establece el ancho del label
        tk.Button(win,text="Cerrar",command=win.destroy).pack(pady=10) # Botón para cerrar la ventana del ranking
        win.transient(self.master); win.grab_set(); self.master.wait_window(win) # Hace que la ventana sea modal
