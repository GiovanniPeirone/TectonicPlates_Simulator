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
pygame.display.set_caption("Línea y rastro fijo")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Variables para la línea
line_col = COLS // 2  # Comienza en el centro
line_direction = random.choice([-1, 1])  # Dirección inicial: -1 (izquierda) o 1 (derecha)
grid_colors = [[WHITE for _ in range(COLS)] for _ in range(ROWS)]  # Colores iniciales de la cuadrícula

# Función para calcular el color según la distancia de la línea
def get_color_from_distance(distance):
    factor = distance / 10  # Ajustar el rango del degradado
    r = max(0, RED[0] * (1 - factor))
    g = max(0, RED[1] * (1 - factor))
    b = max(0, RED[2] * (1 - factor))
    return (int(r), int(g), int(b))

# Función para mover la línea en la dirección actual
def move_line():
    global line_col
    new_col = line_col + line_direction

    # Asegurarse de que no salga de los límites
    if 0 <= new_col < COLS:
        line_col = new_col
        return True
    return False

# Dibujar la cuadrícula
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, grid_colors[row][col], rect)

# Actualizar colores de la cuadrícula
def update_grid():
    for row in range(ROWS):
        if grid_colors[row][line_col] == WHITE:  # Si la celda aún no ha sido coloreada
            grid_colors[row][line_col] = RED

    # Aplicar degradado a las columnas que ya ha pasado la línea
    for col in range(COLS):
        if col != line_col:
            for row in range(ROWS):
                if grid_colors[row][col] != WHITE:  # Solo modificar celdas ya coloreadas
                    distance = abs(line_col - col)
                    grid_colors[row][col] = get_color_from_distance(distance)

# Bucle principal
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mover la línea
    if not move_line():  # Si llega al borde, termina
        running = False

    # Actualizar colores de la cuadrícula
    update_grid()

    # Dibujar todo
    screen.fill(BLACK)
    draw_grid()

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(1)  # Controlar la velocidad (10 FPS)

# Salir
pygame.quit()