import pygame
from pygame.locals import *

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600  # Tamaño de la ventana
CELL_SIZE = 20  # Tamaño de cada celda
COLS = WIDTH // CELL_SIZE  # Número de columnas
ROWS = HEIGHT // CELL_SIZE  # Número de filas

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid con Altura y Color Cambiante")

# Colores base
BASE_COLORS = {
    "low": (0, 0, 255),  # Azul para baja altura
    "mid": (0, 255, 0),  # Verde para altura media
    "high": (255, 0, 0),  # Rojo para alta altura
}

# Crear sprite básico
def create_sprite():
    sprite = pygame.Surface((CELL_SIZE - 2, CELL_SIZE - 2))
    return sprite

# Función para determinar el color basado en la altura
def get_color_based_on_height(altura):
    if altura < 50:
        return BASE_COLORS["low"]
    elif altura < 100:
        return BASE_COLORS["mid"]
    else:
        return BASE_COLORS["high"]

# Matriz para almacenar datos
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

# Llenar la cuadrícula con datos (posY, posX, altura)
for row in range(ROWS):
    for col in range(COLS):
        altura = (row + col) % 150  # Solo un ejemplo de cómo generar la altura
        grid[row][col] = {"posY": row * CELL_SIZE, "posX": col * CELL_SIZE, "altura": altura}

# Función para dibujar la cuadrícula
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Línea gris

# Función para dibujar los sprites y cambiar el color basado en la altura
def draw_sprites():
    for row in range(ROWS):
        for col in range(COLS):
            data = grid[row][col]  # Obtener datos de la celda
            sprite = create_sprite()  # Crear un sprite para cada celda
            color = get_color_based_on_height(data["altura"])  # Obtener el color según la altura
            sprite.fill(color)  # Rellenar el sprite con el color correspondiente

            # Dibujar el sprite en la celda
            x = data["posX"] + 1
            y = data["posY"] + 1
            screen.blit(sprite, (x, y))  # Colocar el sprite en su lugar

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Dibujar todo
    screen.fill((255, 255, 255))  # Fondo blanco
    draw_grid()
    draw_sprites()

    # Actualizar pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()