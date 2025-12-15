# Nonogramas - Juego Interactivo en Python

## Descripción
Este proyecto es un juego de Nonogramas (también conocidos como Picross o Griddlers) desarrollado en Python usando la librería Tkinter para la interfaz gráfica. Este juego permite seleccionar la dificultad, resolver los puzzles manualmente o automáticamente, y registrar los mejores tiempos en un ranking.  

Los nonogramas se generan aleatoriamente según la dificultad, asegurando que cada puzzle tenga al menos una solución válida. Los jugadores pueden interactuar con el tablero, marcar celdas vacías, rellenarlas o indicar con una “X” las celdas que no deben estar llenas.  



## Autora del Proyecto
Izaro Rodriguez Brazal  
Estudiante de Física, primer año, en la Universidad Alfonso X el Sabio (UAX)  
Este proyecto se realizó como trabajo de Proyectos Individuales para la asignatura de Informática.



## Requisitos
- Python 3.8 o superior  
- Librería estándar de Python (`tkinter`) que está incluida por defecto  



## Archivos del Proyecto
- `main.py` : Punto de entrada del juego. Inicia la interfaz gráfica y crea la instancia del juego.  
- `game.py` : Contiene la clase principal `NonogramGame` que maneja la lógica del juego, la interfaz y el cronómetro.  
- `puzzles.py` : Funciones para generar puzzles aleatorios, calcular pistas y comprobar soluciones únicas.  
- `ranking.py` : Funciones para guardar y cargar los mejores tiempos según la dificultad.  



## Cómo ejecutar
1. Asegúrate de tener Python instalado.  
2. Descarga o clona todos los archivos del proyecto en la misma carpeta.  
3. Abre una terminal en la carpeta del proyecto.  
4. Ejecuta el juego con el comando:  
   ```bash
   python main.py
