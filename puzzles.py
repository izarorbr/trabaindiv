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
    
    # Funciones de comprobación de soluciones únicas
def contar_soluciones(nonograma): # Contar cuántas soluciones tiene un nonograma
    """
    Cuenta cuántas soluciones tiene un nonograma.
    Devuelve el número de soluciones.
    """
    filas = nonograma['rows']
    columnas = nonograma['cols']
    n_filas = len(filas)
    n_columnas = len(columnas)

    def generar_fila(longitud, pistas): # Genera todas las combinaciones posibles para una fila dada su longitud y pistas
        if not pistas: # Si no hay pistas, la fila es completamente vacía
            yield [0]*longitud # Yield es una fila de ceros
            return
        primero, *resto = pistas # Desempaqueta la primera pista y el resto
        for prefijo in range(longitud - sum(pistas) - len(pistas) + 2): # Itera sobre posibles posiciones del primer bloque
            for sufijo in generar_fila(longitud - prefijo - primero - 1, resto): # Genera el resto de la fila recursivamente
                yield [0]*prefijo + [1]*primero + ([0] if resto else []) + sufijo # Combina prefijo, bloque y sufijo

    def es_valido(grilla, indice_fila, candidato): # Verifica si un candidato es válido hasta la fila actual
        for indice_col in range(n_columnas): 

         # Si el candidato no tiene esa columna, es inválido
            if indice_col >= len(candidato): # Si el candidato no tiene esa columna, es inválido
                return False

            col = [grilla[r][indice_col] for r in range(indice_fila)] + [candidato[indice_col]] # Construye la columna hasta la fila actual

            pistas_col = columnas[indice_col] # Obtiene las pistas de la columna
            bloques = [] # Lista para contar bloques en la columna
            contador = 0 # Contador de bloques
            for celda in col:
                if celda == 1: # Si la celda está rellena, incrementa el contador 
                    contador += 1
                elif contador > 0: # Si hay un conteo en curso, lo añade a los bloques
                    bloques.append(contador) 
                    contador = 0
            if contador > 0: # Añade el último conteo si existe
                bloques.append(contador)
            if any(b > c for b, c in zip(bloques, pistas_col)): # Verifica si algún bloque excede las pistas
                return False
            if len(bloques) > len(pistas_col): # Verifica si hay más bloques que pistas
                return False
        return True

    soluciones = 0 # Contador de soluciones encontradas
     # Grilla es la representación actual del nonograma
    grilla = [[0]*n_columnas for _ in range(n_filas)] # Inicializa la grilla vacía

    def backtrack(indice_fila): # Función recursiva para explorar todas las combinaciones posibles
        nonlocal soluciones # Permite modificar la variable soluciones del ámbito externo
        if soluciones > 1: # Si ya se encontraron más de una solución, no es necesario continuar
            return # Salir de la función
        if indice_fila == n_filas: # Si se han llenado todas las filas, se encontró una solución
            soluciones += 1 # Incrementa el contador de soluciones
            return
        for candidato in generar_fila(n_columnas, filas[indice_fila]): # Genera candidatos para la fila actual
            if es_valido(grilla, indice_fila, candidato): # Verifica si el candidato es válido
                grilla[indice_fila] = candidato # Asigna el candidato a la grilla
                backtrack(indice_fila + 1) # Llama recursivamente para la siguiente fila
                grilla[indice_fila] = [0]*n_columnas # Resetea la fila después de explorar todas las opciones

    backtrack(0) # Inicia el backtracking desde la primera fila
    return soluciones # Devuelve el número total de soluciones encontradas

def mostrar_nonograma(nonograma): # Muestra la solución del nonograma en consola con bloques llenos y espacios vacíos
    
    n_filas = len(nonograma['rows']) # Número de filas del nonograma
    n_columnas = len(nonograma['cols']) # Número de columnas del nonograma
    grilla = [[0]*n_columnas for _ in range(n_filas)] 

    def generar_fila(longitud, pistas): # Genera todas las combinaciones posibles para una fila dada su longitud y pistas
        if not pistas:
            yield [0]*longitud # Si no hay pistas, la fila es completamente vacía
            return
        primero, *resto = pistas # Desempaqueta la primera pista y el resto, primero es el tamaño del primer bloque
        for prefijo in range(longitud - sum(pistas) - len(pistas) + 2): # Itera sobre posibles posiciones del primer bloque
            for sufijo in generar_fila(longitud - prefijo - primero - 1, resto): # Genera el resto de la fila recursivamente
                yield [0]*prefijo + [1]*primero + ([0] if resto else []) + sufijo # Combina prefijo, bloque y sufijo

    def es_valido(grilla, indice_fila, candidato): # Verifica si un candidato es válido hasta la fila actual
        for indice_col in range(n_columnas):
            col = [grilla[r][indice_col] for r in range(indice_fila)] + [candidato[indice_col]] # Construye la columna hasta la fila actual
            pistas_col = nonograma['cols'][indice_col] # Obtiene las pistas de la columna
            bloques = [] # Lista para contar bloques en la columna
            contador = 0 # Contador de bloques
            for celda in col: # Itera sobre cada celda en la columna
                if celda == 1: # Si la celda está rellena, incrementa el contador
                    contador += 1 # Si hay un conteo en curso, lo añade a los bloques
                elif contador > 0: # Si hay un conteo en curso, lo añade a los bloques
                    bloques.append(contador)
                    contador = 0 # Resetea el contador
            if contador > 0: # Añade el último conteo si existe
                bloques.append(contador)
            if any(b > c for b, c in zip(bloques, pistas_col)): # Verifica si algún bloque excede las pistas
                return False
            if len(bloques) > len(pistas_col): # Verifica si hay más bloques que pistas
                return False
        return True

    def backtrack_solucion(indice_fila): # Función recursiva para encontrar una solución, backtracking es una función de búsqueda de soluciones
        if indice_fila == n_filas: # Si se han llenado todas las filas, se encontró una solución
            return True
        for candidato in generar_fila(n_columnas, nonograma['rows'][indice_fila]): # Genera candidatos para la fila actual
            if es_valido(grilla, indice_fila, candidato): # Verifica si el candidato es válido
                grilla[indice_fila] = candidato # Asigna el candidato a la grilla
                if backtrack_solucion(indice_fila + 1): # Llama recursivamente para la siguiente fila   
                    return True
                grilla[indice_fila] = [0]*n_columnas  # Resetea la fila después de explorar todas las opciones
        return False

    backtrack_solucion(0) # Inicia el backtracking desde la primera fila
    for fila in grilla: # Muestra la grilla en consola
        print(''.join('█' if c else ' ' for c in fila)) # Usa bloques llenos para 1 y espacios para 0

# Bucle principal para generar nonogramas con solución única
def generar_nonograma_unico(dificultad): # Genera un nonograma con una única solución, no devuelve nada hasta encontrar uno válido

    while True: # Bucle hasta encontrar un nonograma con solución única
        matriz, pistas_filas, pistas_columnas = generar_puzzle_por_dificultad(dificultad) # Genera un nonograma según la dificultad
        nonograma = {
            'rows': pistas_filas,
            'cols': pistas_columnas
        }

        numero_soluciones = contar_soluciones(nonograma) # Cuenta el número de soluciones del nonograma generado
        if numero_soluciones == 1: # Si tiene una única solución, lo devuelve
            return matriz, pistas_filas, pistas_columnas # Devuelve la matriz y las pistas
