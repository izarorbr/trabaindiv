import random


def generar_pistas(matriz): #Genera pistas de filas y columnas para un Nonograma
    pistas_filas, pistas_columnas = [], [] # Listas para almacenar las pistas
    num_columnas = len(matriz[0]) 

    # Filas
    for fila in matriz: # Itera sobre cada fila de la matriz
        pistas = []
        contador = 0
        for celda in fila: 
            if celda == 1: # Si la celda está rellena, incrementa el contador
                contador += 1
            elif contador > 0: # Si hay un conteo en curso, lo añade a las pistas
                pistas.append(contador)
                contador = 0
        if contador > 0: # Añade el último conteo si existe
            pistas.append(contador)
        pistas_filas.append(pistas or [0]) # Añade las pistas de la fila (o [0] si está vacía)

    # Columnas
    for j in range(num_columnas): # Itera sobre cada columna
        pistas = []
        contador = 0
        for i in range(len(matriz)): # Itera sobre cada fila para la columna j
            if matriz[i][j] == 1:
                contador += 1
            elif contador > 0: # Si hay un conteo en curso, lo añade a las pistas
                pistas.append(contador)
                contador = 0
        if contador > 0: # Añade el último conteo si existe
            pistas.append(contador) 
        pistas_columnas.append(pistas or [0]) # Añade las pistas de la columna (o [0] si está vacía)

    return pistas_filas, pistas_columnas # Devuelve las pistas generadas



def generar_nonograma_aleatorio(tamano, densidad=0.4): # Densidad es la probabilidad de que una celda esté rellena 

    """
    Genera un nonograma aleatorio de tamaño `tamano x tamano`.
    `densidad` es la probabilidad de que una celda esté rellena.
    Devuelve: matriz, pistas_filas, pistas_columnas
    """
 
    while True: # Genera hasta encontrar un nonograma válido
        matriz = [[1 if random.random() < densidad else 0 for _ in range(tamano)] for _ in range(tamano)]
        
        # Evitar filas o columnas completamente vacías
        pistas_filas, pistas_columnas = generar_pistas(matriz) # Genera las pistas para la matriz generada
        if all(any(n > 0 for n in fila) for fila in pistas_filas) and \
           all(any(n > 0 for n in col) for col in pistas_columnas): # Verifica que no haya filas o columnas vacías
            return matriz, pistas_filas, pistas_columnas # Devuelve la matriz y las pistas


def generar_puzzle_por_dificultad(dificultad): # Devuelve un nonograma según la dificultad

    """
    Devuelve un nonograma aleatorio según la dificultad:
    - 'facil'  -> 5x5, densidad 0.4
    - 'medio'  -> 7x7, densidad 0.45
    - 'dificil'-> 9x9, densidad 0.5
    """
    
    if dificultad == 'facil':
        return generar_nonograma_aleatorio(5, densidad=0.4) 
    elif dificultad == 'medio':
        return generar_nonograma_aleatorio(7, densidad=0.45)
    elif dificultad == 'dificil':
        return generar_nonograma_aleatorio(9, densidad=0.5)
    else:
        raise ValueError(f"Dificultad desconocida: {dificultad}")
    