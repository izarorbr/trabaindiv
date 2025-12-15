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
        raise ValueError(f"Dificultad desconocida: {dificultad}") # Maneja la dificultad desconocida
    
    # --- Funciones de comprobación de soluciones únicas ---
def contar_soluciones(nonograma):
    """
    Cuenta cuántas soluciones tiene un nonograma.
    Devuelve el número de soluciones.
    """
    filas = nonograma['rows']
    columnas = nonograma['cols']
    n_filas = len(filas)
    n_columnas = len(columnas)

    def generar_fila(longitud, pistas):
        if not pistas:
            yield [0]*longitud
            return
        primero, *resto = pistas
        for prefijo in range(longitud - sum(pistas) - len(pistas) + 2):
            for sufijo in generar_fila(longitud - prefijo - primero - 1, resto):
                yield [0]*prefijo + [1]*primero + ([0] if resto else []) + sufijo

    def es_valido(grilla, indice_fila, candidato):
        for indice_col in range(n_columnas):

         # Si el candidato no tiene esa columna, es inválido
            if indice_col >= len(candidato):
                return False

            col = [grilla[r][indice_col] for r in range(indice_fila)] + [candidato[indice_col]]

            pistas_col = columnas[indice_col]
            bloques = []
            contador = 0
            for celda in col:
                if celda == 1:
                    contador += 1
                elif contador > 0:
                    bloques.append(contador)
                    contador = 0
            if contador > 0:
                bloques.append(contador)
            if any(b > c for b, c in zip(bloques, pistas_col)):
                return False
            if len(bloques) > len(pistas_col):
                return False
        return True

    soluciones = 0
    grilla = [[0]*n_columnas for _ in range(n_filas)]

    def backtrack(indice_fila):
        nonlocal soluciones
        if soluciones > 1:
            return
        if indice_fila == n_filas:
            soluciones += 1
            return
        for candidato in generar_fila(n_columnas, filas[indice_fila]):
            if es_valido(grilla, indice_fila, candidato):
                grilla[indice_fila] = candidato
                backtrack(indice_fila + 1)
                grilla[indice_fila] = [0]*n_columnas

    backtrack(0)
    return soluciones

def mostrar_nonograma(nonograma):
    """
    Muestra la solución del nonograma en consola con bloques █ para las celdas rellenas.
    """
    n_filas = len(nonograma['rows'])
    n_columnas = len(nonograma['cols'])
    grilla = [[0]*n_columnas for _ in range(n_filas)]

    def generar_fila(longitud, pistas):
        if not pistas:
            yield [0]*longitud
            return
        primero, *resto = pistas
        for prefijo in range(longitud - sum(pistas) - len(pistas) + 2):
            for sufijo in generar_fila(longitud - prefijo - primero - 1, resto):
                yield [0]*prefijo + [1]*primero + ([0] if resto else []) + sufijo

    def es_valido(grilla, indice_fila, candidato):
        for indice_col in range(n_columnas):
            col = [grilla[r][indice_col] for r in range(indice_fila)] + [candidato[indice_col]]
            pistas_col = nonograma['cols'][indice_col]
            bloques = []
            contador = 0
            for celda in col:
                if celda == 1:
                    contador += 1
                elif contador > 0:
                    bloques.append(contador)
                    contador = 0
            if contador > 0:
                bloques.append(contador)
            if any(b > c for b, c in zip(bloques, pistas_col)):
                return False
            if len(bloques) > len(pistas_col):
                return False
        return True

    def backtrack_solucion(indice_fila):
        if indice_fila == n_filas:
            return True
        for candidato in generar_fila(n_columnas, nonograma['rows'][indice_fila]):
            if es_valido(grilla, indice_fila, candidato):
                grilla[indice_fila] = candidato
                if backtrack_solucion(indice_fila + 1):
                    return True
                grilla[indice_fila] = [0]*n_columnas
        return False

    backtrack_solucion(0)
    for fila in grilla:
        print(''.join('█' if c else ' ' for c in fila))

# Bucle principal para generar nonogramas con solución única
def generar_nonograma_unico(dificultad):
    """
    Genera un nonograma que tiene exactamente UNA solución.
    No devuelve nada hasta encontrar uno válido.
    """

    while True:
        matriz, pistas_filas, pistas_columnas = generar_puzzle_por_dificultad(dificultad)
        nonograma = {
            'rows': pistas_filas,
            'cols': pistas_columnas
        }

        numero_soluciones = contar_soluciones(nonograma)
        if numero_soluciones == 1:
            return matriz, pistas_filas, pistas_columnas
