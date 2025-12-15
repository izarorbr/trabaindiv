"""
Solitario Español con Pygame
Autor: Estudiante
Descripción: Solitario con baraja española, ventana gráfica, colores,
ranking por tiempo y modo de 1 o 3 cartas por salida.
"""

import pygame
import random
import time
import os

# --- Configuración ---
ANCHO, ALTO = 900, 600
FPS = 30
IMAGENES_PATH = "imagenes/"
RANKING_FILE = "ranking.txt"
FUENTE = "freesansbold.ttf"

# --- Clase Carta ---
class Carta:
    def __init__(self, numero, palo, imagen):
        self.numero = numero
        self.palo = palo
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.mostrada = False

# --- Clase Baraja ---
class Baraja:
    def __init__(self):
        self.palos = ["Oros", "Copas", "Espadas", "Bastos"]
        self.numeros = list(range(1, 8)) + [10, 11, 12]
        self.cartas = []
        self.cargar_cartas()
        random.shuffle(self.cartas)

    def cargar_cartas(self):
        for palo in self.palos:
            for num in self.numeros:
                path = f"{IMAGENES_PATH}{num}_{palo}.png"
                imagen = pygame.image.load(path)
                imagen = pygame.transform.scale(imagen, (80, 120))
                self.cartas.append(Carta(num, palo, imagen))

# --- Clase Solitario ---
class Solitario:
    def __init__(self, pantalla, modo, nombre):
        self.pantalla = pantalla
        self.modo = modo
        self.nombre = nombre
        self.baraja = Baraja()
        self.taco_index = 0
        self.monton = []
        self.inicio = time.time()
        self.reverso = pygame.image.load(f"{IMAGENES_PATH}reverso.png")
        self.reverso = pygame.transform.scale(self.reverso, (80, 120))
        self.juego_terminado = False

    def mostrar_taco(self):
        x_inicio = 50
        y = 200
        self.cartas_a_mostrar = self.baraja.cartas[self.taco_index:self.taco_index+self.modo]
        for i, carta in enumerate(self.cartas_a_mostrar):
            self.pantalla.blit(carta.imagen, (x_inicio + i*100, y))
            carta.rect.topleft = (x_inicio + i*100, y)

    def manejar_click(self, pos):
        if self.juego_terminado:
            return
        for i, carta in enumerate(self.cartas_a_mostrar):
            if carta.rect.collidepoint(pos):
                self.monton.append(carta)
                self.taco_index += self.modo
                if self.taco_index >= len(self.baraja.cartas):
                    self.finalizar()
                break

    def finalizar(self):
        self.juego_terminado = True
        tiempo = round(time.time() - self.inicio, 2)
        self.guardar_ranking(tiempo)
        print(f"¡Felicidades {self.nombre}! Tiempo: {tiempo} s")

    def guardar_ranking(self, tiempo):
        ranking = []
        if os.path.exists(RANKING_FILE):
            with open(RANKING_FILE, "r") as f:
                for linea in f:
                    try:
                        n, t = linea.strip().split(",")
                        ranking.append((n, float(t)))
                    except:
                        continue
        ranking.append((self.nombre, tiempo))
        ranking.sort(key=lambda x: x[1])
        with open(RANKING_FILE, "w") as f:
            for n, t in ranking:
                f.write(f"{n},{t}\n")

    def mostrar_ranking(self):
        if not os.path.exists(RANKING_FILE):
            return
        y = 50
        fuente = pygame.font.Font(FUENTE, 20)
        with open(RANKING_FILE, "r") as f:
            for pos, linea in enumerate(f, start=1):
                n, t = linea.strip().split(",")
                texto = fuente.render(f"{pos}. {n} - {t}s", True, (255, 255, 0))
                self.pantalla.blit(texto, (600, y))
                y += 25

# --- Función principal ---
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Solitario Español")
    clock = pygame.time.Clock()

    # Pantalla de inicio
    fuente = pygame.font.Font(FUENTE, 30)
    nombre = input("Ingresa tu nombre: ").strip()
    modo = input("Modo de cartas por salida (1 o 3): ").strip()
    while modo not in ["1", "3"]:
        modo = input("Modo inválido. Ingresa 1 o 3: ").strip()
    modo = int(modo)

    juego = Solitario(pantalla, modo, nombre)

    running = True
    while running:
        pantalla.fill((30, 30, 60))  # Fondo oscuro

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                juego.manejar_click(event.pos)

        if not juego.juego_terminado:
            juego.mostrar_taco()
        juego.mostrar_ranking()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
