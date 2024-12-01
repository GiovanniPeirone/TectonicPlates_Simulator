import pygame
from pygame.locals import *

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 600, 400  # Tamaño de la ventana
ROWS, COLS = 100, 100  # Filas y columnas de la cuadrícula
CELL_WIDTH = WIDTH // COLS  # Ancho de cada celda
CELL_HEIGHT = HEIGHT // ROWS  # Altura de cada celda

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid con Sprites")

# Colores
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Sprite de ejemplo
sprite = pygame.Surface((CELL_WIDTH - 10, CELL_HEIGHT - 10))
sprite.fill(RED)

# Función para dibujar la cuadrícula
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            pygame.draw.rect(screen, GRAY, rect, 1)  # Dibuja las líneas de la cuadrícula

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Dibujar todo
    screen.fill(WHITE)
    draw_grid()

    # Colocar el sprite en una celda específica (por ejemplo, celda [1, 2])
    sprite_x = 2 * CELL_WIDTH + 5  # Columna 2
    sprite_y = 1 * CELL_HEIGHT + 5  # Fila 1
    screen.blit(sprite, (sprite_x, sprite_y))

    # Actualizar pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()