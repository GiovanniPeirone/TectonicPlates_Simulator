import pygame
from pygame.locals import *

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 1000, 900  # Tamaño de la ventana
CELL_SIZE = 10  # Tamaño más pequeño de cada celda (ancho y alto)
COLS = WIDTH // CELL_SIZE  # Número de columnas
ROWS = HEIGHT // CELL_SIZE  # Número de filas

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Super Denso con Sprites")

# Colores
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Cargar sprite
sprite_red = pygame.Surface((CELL_SIZE - 2, CELL_SIZE - 2))  # Sprite más pequeño
sprite_red.fill((255, 0, 0))  # Rojo

# Matriz para almacenar los sprites en la cuadrícula
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

# Colocar sprites aleatoriamente en algunas celdas
grid[5][5] = sprite_red
grid[20][25] = sprite_red
grid[30][40] = sprite_red

# Función para dibujar la cuadrícula
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)  # Dibujar línea de celda

# Función para dibujar los sprites
def draw_sprites():
    for row in range(ROWS):
        for col in range(COLS):
            sprite = grid[row][col]
            if sprite:  # Si hay un sprite en la celda
                x = col * CELL_SIZE + 1  # Posición en X
                y = row * CELL_SIZE + 1  # Posición en Y
                screen.blit(sprite, (x, y))

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Dibujar todo
    screen.fill(WHITE)
    draw_grid()
    draw_sprites()

    # Actualizar pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()