import os
from tkinter import messagebox

def cargar_ranking(dificultad): # Carga el ranking desde un archivo según la dificultad
    nombre_archivo = f'ranking_{dificultad}.txt'
    ranking = [] # Lista vacía para almacenar las entradas del ranking
    if os.path.exists(nombre_archivo): # Verifica si el archivo existe
        try: 
            with open(nombre_archivo, 'r') as f: #  Abre el archivo en modo lectura 
                for linea in f: 
                    try:
                        nombre, tiempo = linea.strip().split(',') # Divide la línea en nombre y tiempo
                        ranking.append({'nombre': nombre, 'tiempo': float(tiempo)}) # Añade la entrada al ranking
                    except ValueError: # Maneja líneas mal formateadas
                        continue
        except IOError: # Maneja errores de lectura del archivo
            messagebox.showerror("Error", f"No se pudo leer el archivo {nombre_archivo}")
    ranking.sort(key=lambda x: x['tiempo']) # Ordena el ranking por tiempo. Lambda significa una función anónima para ordenar las entradas
    return ranking

def guardar_ranking(dificultad, nombre, tiempo): # Guarda una nueva entrada en el ranking
    ranking = cargar_ranking(dificultad) 
    ranking.append({'nombre': nombre, 'tiempo': tiempo}) # Añade la nueva entrada
    ranking.sort(key=lambda x: x['tiempo']) 
    ranking = ranking[:10] # Mantiene solo las 10 mejores entradas
    nombre_archivo = f'ranking_{dificultad}.txt'
    try: # Intenta escribir el ranking actualizado en el archivo
        with open(nombre_archivo, 'w') as f: # Abre el archivo en modo escritura
            for entrada in ranking: # Itera sobre las entradas del ranking
                f.write(f"{entrada['nombre']},{entrada['tiempo']}\n") # Escribe cada entrada en el archivo
    except IOError:
        messagebox.showerror("Error", f"No se pudo escribir en {nombre_archivo}") # Muestra un mensaje de error si no se puede escribir en el archivo