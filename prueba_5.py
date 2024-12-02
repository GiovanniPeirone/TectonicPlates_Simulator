import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Línea con movimiento y rastro gradual")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Variables para la línea
line_col = COLS // 2  # Comienza en el centro
line_colors = [[0 for _ in range(COLS)] for _ in range(ROWS)]  # Inicializar matriz de degradado

# Función para calcular el color según el valor en la matriz de degradado
def get_color_from_degradation(value):
    if value == 0:
        return WHITE
    factor = value / 10  # Ajustar el rango del degradado
    r = max(0, RED[0] * (1 - factor))
    g = max(0, RED[1] * (1 - factor))
    b = max(0, RED[2] * (1 - factor))
    return (int(r), int(g), int(b))

# Función para mover la línea aleatoriamente
def move_line():
    global line_col
    direction = random.choice([-1, 1])  # Izquierda o derecha
    new_col = line_col + direction

    # Asegurarse de que no salga de los límites
    if 0 <= new_col < COLS:
        line_col = new_col

# Función para actualizar el degradado
def update_degradation():
    for row in range(ROWS):
        for col in range(COLS):
            if col == line_col:  # La línea blanca actualiza su celda a blanco
                line_colors[row][col] = 0
            else:  # Incrementa el valor de degradado para otras celdas
                line_colors[row][col] = min(line_colors[row][col] + 1, 10)

# Dibujar la cuadrícula
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = get_color_from_degradation(line_colors[row][col])
            pygame.draw.rect(screen, color, rect)

# Bucle principal
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar estado
    move_line()
    update_degradation()

    # Dibujar todo
    screen.fill(BLACK)
    draw_grid()

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(10)  # Controlar la velocidad (10 FPS)

# Salir
pygame.quit()