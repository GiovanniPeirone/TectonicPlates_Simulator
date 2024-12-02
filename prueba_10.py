import pygame
import noise
import random

# Tamaño de la ventana
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 10  # Tamaño de cada celda
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE  # El grid será del tamaño adecuado
FPS = 60

# Colores para las alturas
def get_color(height):
    """Retorna el color basado en la altura."""
    if height == 0:
        return (0, 0.75, 1)  # Agua (mar)
    elif height == 1:
        return (1, 1, 0)  # Playa
    elif height == 2:
        return (0.56, 0.93, 0.56)  # Llanura (verde claro)
    else:
        # Gradiente de verde a marrón para alturas 3 a 15
        green = max(0, 0.56 - (height - 2) * 0.05)  # De verde claro a más oscuro
        red = min(1, (height - 2) * 0.05)  # De verde a marrón
        return (red, green, 0)

def generate_terrain(rows, cols):
    """Genera el terreno usando ruido Perlin."""
    scale = 100  # Escala para el ruido Perlin
    terrain = []
    for y in range(rows):
        row = []
        for x in range(cols):
            # Genera el ruido Perlin para la posición x, y
            noise_value = noise.pnoise2(x / scale, y / scale, octaves=6, persistence=0.5, lacunarity=2.0)
            # Mapea los valores de ruido a un rango de alturas de 0 a 15
            height = int((noise_value + 1) * 7.5)  # Mapea el ruido (-1 a 1) a (0 a 15)
            row.append(height)
        terrain.append(row)
    return terrain

def draw_terrain(terrain):
    """Dibuja el terreno en pantalla, dividido en dos placas."""
    for y in range(ROWS):
        for x in range(COLS):
            color = get_color(terrain[y][x])  # Obtener el color de la altura
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def move_plates(terrain, offset_x_left, offset_x_right):
    """Simula el movimiento de las placas tectónicas."""
    if offset_x_right > COLS // 2:
        for y in range(ROWS):
            for x in range(COLS // 2, COLS):
                if x - offset_x_right < COLS // 2:
                    terrain[y][x - offset_x_left] = terrain[y][x]  # Mueve el terreno
                    terrain[y][x] = 0  # El terreno de la placa inferior desaparece
        return offset_x_left + 1, offset_x_right - 1
    return offset_x_left, offset_x_right

def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulador de Choque de Placas Tectónicas")
    clock = pygame.time.Clock()

    terrain = generate_terrain(ROWS, COLS)
    offset_x_left, offset_x_right = 0, COLS // 2  # Offset para las placas
    running = True

    while running:
        screen.fill((0, 0, 0))  # Limpiar pantalla

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                terrain = generate_terrain(ROWS, COLS)  # Reinicia el terreno
                offset_x_left, offset_x_right = 0, COLS // 2

        # Mueve las placas
        offset_x_left, offset_x_right = move_plates(terrain, offset_x_left, offset_x_right)
        
        # Dibujar terreno
        draw_terrain(terrain)

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()