import pygame
import noise
import numpy as np

# Configuración inicial
WIDTH, HEIGHT = 800, 600  # Tamaño de la pantalla
GRID_SIZE = 2  # Tamaño del grid en píxeles
ROWS, COLS = (HEIGHT // GRID_SIZE) * 2, (WIDTH // GRID_SIZE) * 2  # Doble del tamaño de la pantalla

# Colores para las alturas
COLORS = {
    0: (135, 206, 235),  # Celeste
    1: (240, 230, 140),  # Amarillo
    2: (144, 238, 144),  # Verde claro
}
for i in range(3, 16):
    intensity = int(144 - (i - 2) * 9)  # Oscurece progresivamente
    COLORS[i] = (0, intensity, 0)

# Generar terreno
def generate_terrain(rows, cols):
    scale = 100
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    terrain = np.zeros((rows, cols), dtype=int)

    for i in range(rows):
        for j in range(cols):
            x = i / scale
            y = j / scale
            noise_value = noise.pnoise2(
                x, y,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=cols,
                repeaty=rows,
                base=42
            )
            height = int((noise_value + 0.5) * 15)  # Escala el ruido a valores entre 0 y 15
            terrain[i, j] = min(max(height, 0), 15)
    return terrain

# Dibujar el terreno
def draw_terrain(screen, terrain):
    for i in range(ROWS):
        for j in range(COLS):
            color = COLORS[terrain[i, j]]
            pygame.draw.rect(
                screen, color,
                (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )

# Configuración de pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de choque de placas tectónicas")
clock = pygame.time.Clock()

# Generar el terreno inicial
terrain = generate_terrain(ROWS, COLS)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Reiniciar la simulación
            terrain = generate_terrain(ROWS, COLS)

    # Dibujar el terreno
    screen.fill((0, 0, 0))
    draw_terrain(screen, terrain)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()