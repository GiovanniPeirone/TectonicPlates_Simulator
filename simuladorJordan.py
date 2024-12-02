import pygame
import random
import math

# Configuración inicial
WIDTH, HEIGHT = 800, 600  # Tamaño de la pantalla
GRID_SIZE = 2  # Tamaño de cada celda
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE * 2  # Doble del ancho
FPS = 60

# Colores para representar diferentes alturas
COLORS = {
    'water': (0, 191, 255),  # Agua (mar)
    'beach': (255, 255, 0),  # Playa
    'land': (144, 238, 144),  # Tierra (verde claro)
    'mountain': (139, 69, 19),  # Montañas (marrón)
}

# Botones
BUTTONS = {
    "reset": pygame.Rect(WIDTH - 120, HEIGHT - 40, 100, 30)
}

def get_color(height):
    """Retorna el color basado en la altura del terreno."""
    if height < 0:
        return COLORS['water']  # Agua (mar)
    elif height < 2:
        return COLORS['beach']  # Playa
    elif height < 5:
        return COLORS['land']  # Tierra (verde claro)
    else:
        return COLORS['mountain']  # Montañas (marrón)

def generate_terrain(rows, cols):
    """Genera un terreno sencillo utilizando ruido de manera más predecible."""
    terrain = []
    
    for y in range(rows):
        row = []
        for x in range(cols):
            # Generar valores aleatorios para simular el terreno (simulando ruido sin usar Perlin)
            random_value = random.random()
            # Definir las alturas de agua, playa, y tierra basados en valores aleatorios
            if random_value < 0.4:
                height = -1  # Agua
            elif random_value < 0.6:
                height = 1  # Playa
            elif random_value < 0.9:
                height = 3  # Tierra
            else:
                height = 6  # Montañas
            row.append(height)
        terrain.append(row)
    
    return terrain

def apply_influence(terrain, center_x, center_y, radius, intensity):
    """Modifica la altura del terreno con una influencia circular."""
    for y in range(max(0, center_y - radius), min(ROWS, center_y + radius + 1)):
        for x in range(max(0, center_x - radius), min(COLS, center_x + radius + 1)):
            distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            if distance <= radius:
                influence = max(0, math.exp(-distance ** 2 / (2 * radius ** 2)))
                terrain[y][x] = min(15, max(-1, terrain[y][x] + int(intensity * influence)))

def draw_terrain(screen, terrain, offset_x):
    """Dibuja el terreno en pantalla."""
    for y, row in enumerate(terrain):
        for x, height in enumerate(row):
            color = get_color(height)
            pygame.draw.rect(
                screen, color, 
                ((x - offset_x) * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )

def draw_buttons(screen, radius):
    """Dibuja los botones y el estado actual."""
    pygame.draw.rect(screen, (255, 0, 0), BUTTONS["reset"])

    font = pygame.font.SysFont(None, 24)
    screen.blit(font.render("Reset", True, (255, 255, 255)), (WIDTH - 100, HEIGHT - 35))

    # Mostrar tamaño de radio
    screen.blit(font.render(f"Radius: {radius}", True, (255, 255, 255)), (230, HEIGHT - 35))

def handle_mouse_click(event, terrain, radius, lines, offset_x_left, offset_x_right, mode):
    """Maneja los clics del ratón y actualiza el estado del terreno."""
    mouse_x, mouse_y = event.pos
    if event.button == 1:  # Clic izquierdo: modificar terreno
        grid_x = (mouse_x // GRID_SIZE) + offset_x_left if mouse_x < WIDTH // 2 else (mouse_x // GRID_SIZE) + offset_x_right
        grid_y = mouse_y // GRID_SIZE
        if 0 <= grid_y < ROWS and 0 <= grid_x < COLS:
            apply_influence(terrain, grid_x, grid_y, radius, intensity=3 if mode == "Elevate" else -3)
    elif event.button == 3:  # Clic derecho: dibujar línea de división
        grid_x = (mouse_x // GRID_SIZE) + offset_x_left if mouse_x < WIDTH // 2 else (mouse_x // GRID_SIZE) + offset_x_right
        grid_y = mouse_y // GRID_SIZE
        lines.append((grid_x, grid_y))  # Almacenar las coordenadas para la línea

    return terrain, lines

def handle_mouse_wheel(event, radius):
    """Maneja el evento de la rueda del mouse para ajustar el radio de influencia."""
    if event.y > 0:  # Rueda hacia arriba
        radius = min(20, radius + 1)
    elif event.y < 0:  # Rueda hacia abajo
        radius = max(1, radius - 1)
    
    return radius

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulador de Placas Tectónicas")
    clock = pygame.time.Clock()

    terrain = generate_terrain(ROWS, COLS)
    offset_x_left, offset_x_right = 0, COLS // 2  # Offset para las placas
    running = True
    lines = []  # Líneas que representan los límites de placas
    radius = 10  # Radio inicial para la influencia
    mode = "Elevate"  # Alterna entre elevar o reducir terreno

    while running:
        screen.fill((0, 0, 0))
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                terrain, lines = handle_mouse_click(event, terrain, radius, lines, offset_x_left, offset_x_right, mode)
            if event.type == pygame.MOUSEMOTION:
                # Arrastrar el mouse mientras se mantiene presionado el botón
                if pygame.mouse.get_pressed()[0]:  # Clic izquierdo para modificar terreno
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = (mouse_x // GRID_SIZE) + offset_x_left if mouse_x < WIDTH // 2 else (mouse_x // GRID_SIZE) + offset_x_right
                    grid_y = mouse_y // GRID_SIZE
                    if 0 <= grid_y < ROWS and 0 <= grid_x < COLS:
                        apply_influence(terrain, grid_x, grid_y, radius, intensity=3 if mode == "Elevate" else -3)
            if event.type == pygame.MOUSEWHEEL:
                radius = handle_mouse_wheel(event, radius)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Si presionas la tecla 'r', reinicia el mapa
                    terrain = generate_terrain(ROWS, COLS)
                    lines = []

        # Dibujar terreno
        draw_terrain(screen, terrain, offset_x_left)
        draw_terrain(screen, terrain, offset_x_right)

        # Dibujar botones
        draw_buttons(screen, radius)

        # Dibujar líneas de división
        if lines:
            for i in range(1, len(lines)):
                pygame.draw.line(screen, (255, 255, 255), 
                                 (lines[i - 1][0] * GRID_SIZE - offset_x_left, lines[i - 1][1] * GRID_SIZE), 
                                 (lines[i][0] * GRID_SIZE - offset_x_left, lines[i][1] * GRID_SIZE), 2)

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
