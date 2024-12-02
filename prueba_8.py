import pygame
import noise
import random

# Configuración inicial
WIDTH, HEIGHT = 800, 600  # Tamaño de la pantalla
GRID_SIZE = 2  # Tamaño de cada celda
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE * 2  # Doble del ancho
FPS = 60

# Colores según alturas
COLORS = {
    0: (0, 191, 255),  # Agua
    1: (255, 255, 0),  # Playa
    2: (144, 238, 144),  # Llanura
}

def get_color(height):
    """Retorna el color basado en la altura."""
    if height <= 2:
        return COLORS[height]
    else:
        # Gradiente de verde a marrón
        green = max(0, 144 - (height - 2) * 10)
        red = min(139, (height - 2) * 10)
        return (red, green, 0)

def generate_terrain(rows, cols):
    """Genera el terreno usando ruido Perlin."""
    scale = 100  # Escala para el ruido Perlin
    terrain = []
    for y in range(rows):
        row = []
        for x in range(cols):
            noise_value = noise.pnoise2(x / scale, y / scale, octaves=6, persistence=0.5, lacunarity=2.0)
            height = int((noise_value + 1) * 7.5)  # Mapea valores de ruido (-1 a 1) a alturas (0-15)
            row.append(height)
        terrain.append(row)
    return terrain

def draw_terrain(screen, terrain, offset_x):
    """Dibuja el terreno en pantalla."""
    for y, row in enumerate(terrain):
        for x, height in enumerate(row):
            if 0 <= x - offset_x < COLS // 2:  # Ajusta para el desplazamiento
                color = get_color(height)
                pygame.draw.rect(
                    screen, color, 
                    ((x - offset_x) * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                )

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulador de Placas Tectónicas")
    clock = pygame.time.Clock()

    terrain = generate_terrain(ROWS, COLS)
    offset_x_left, offset_x_right = 0, COLS // 2  # Offset para las placas
    running = True

    while running:
        screen.fill((0, 0, 0))
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                terrain = generate_terrain(ROWS, COLS)  # Reinicia el terreno
                offset_x_left, offset_x_right = 0, COLS // 2

        # Dibujar terreno
        draw_terrain(screen, terrain, offset_x_left)
        draw_terrain(screen, terrain, offset_x_right)

        # Dibujar línea divisoria
        pygame.draw.line(screen, (255, 255, 255), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

        # Actualizar movimiento de placas
        if offset_x_left < COLS // 4 and offset_x_right > COLS // 4:
            offset_x_left += 1
            offset_x_right -= 1

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()