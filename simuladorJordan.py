import pygame
import random
import math
import noise  # Para la generación procedural de terreno con Perlin Noise
import numpy as np

# Configuración inicial
WIDTH, HEIGHT = 800, 600  # Tamaño de la pantalla
GRID_SIZE = 2  # Tamaño de cada celda
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE  # Reajustamos para que se dibuje correctamente
FPS = 60
NOISE_SCALE = 100.0  # Escala para el ruido Perlin

# Colores para representar diferentes alturas
COLORS = {
    'water': (0, 191, 255),  # Agua (mar)
    'beach': (255, 255, 0),  # Playa
    'land': (144, 238, 144),  # Tierra (verde claro)
    'mountain': (139, 69, 19),  # Montañas (marrón)
    'line': (255, 255, 255),  # Línea divisoria
    'button': (50, 50, 200),  # Color para el botón
    'button_hover': (70, 70, 255),  # Color para el botón al pasar el mouse
    'volcano': (255, 69, 0),
    'fault': (139, 0, 0),
    'earthquake': (255, 255, 0),
    'subduction': (128, 0, 128)
}

# Botones de reset y elevar se eliminaron

SIMULATION_SPEED = 0.5
EROSION_RATE = 0.01
PLATE_TYPES = ['oceanic', 'continental']

class TectonicPlate:
    """Clase para manejar las placas tectónicas"""
    def __init__(self, points, plate_type='continental'):
        self.points = points
        self.type = plate_type
        self.velocity = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        self.velocity *= SIMULATION_SPEED

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
    """Genera un terreno utilizando Perlin Noise para un mapa más natural."""
    terrain = []
    for y in range(rows):
        row = []
        for x in range(cols):
            # Usamos Perlin noise para generar un valor de altura
            noise_value = noise.pnoise2(x / NOISE_SCALE, y / NOISE_SCALE, octaves=6, persistence=0.5, lacunarity=2.0)
            height = noise_value * 10  # Multiplicamos por un factor para amplificar la variabilidad
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

def draw_terrain(screen, terrain):
    """Dibuja el terreno en pantalla solo donde es necesario para optimizar rendimiento."""
    for y in range(ROWS):
        for x in range(COLS):
            color = get_color(terrain[y][x])
            pygame.draw.rect(
                screen, color, 
                (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )

def draw_dividing_lines(screen, lines):
    """Dibuja las líneas divisorias entre las placas tectónicas."""
    if len(lines) > 1:
        for i in range(1, len(lines)):
            pygame.draw.line(screen, COLORS['line'], 
                             (lines[i - 1][0] * GRID_SIZE, lines[i - 1][1] * GRID_SIZE), 
                             (lines[i][0] * GRID_SIZE, lines[i][1] * GRID_SIZE), 2)

def draw_instructions(screen, simulation_started, can_cut):
    """Dibuja las instrucciones para el usuario en la pantalla."""
    font = pygame.font.SysFont("Arial", 24)
    if not simulation_started:
        instructions = font.render("Presiona 'E' para elevar/reducir el terreno", True, (255, 255, 255))
        screen.blit(instructions, (10, 10))
        instructions2 = font.render("Arrastra para crear divisorias entre placas", True, (255, 255, 255))
        screen.blit(instructions2, (10, 40))
        if can_cut:
            instructions3 = font.render("Haz clic derecho para cortar el trazado", True, (255, 255, 255))
            screen.blit(instructions3, (10, 70))
    else:
        instructions = font.render("Simulación comenzada. Presiona 'R' para reiniciar.", True, (255, 255, 255))
        screen.blit(instructions, (10, 10))

def draw_button(screen, mouse_pos, start_button):
    """Dibuja el botón 'Empezó la simulación' y maneja su estado de hover."""
    button_rect = pygame.Rect(start_button[0], start_button[1], 200, 50)
    color = COLORS['button_hover'] if button_rect.collidepoint(mouse_pos) else COLORS['button']
    pygame.draw.rect(screen, color, button_rect)

    font = pygame.font.SysFont("Arial", 24)
    text = font.render("Empezó la simulación", True, (255, 255, 255))
    screen.blit(text, (start_button[0] + 40, start_button[1] + 15))
    
    return button_rect

def handle_mouse_click(event, terrain, radius, lines, mode, dragging_line, simulation_started, start_button, can_cut):
    """Maneja los clics del ratón y actualiza el estado del terreno y líneas divisorias."""
    mouse_x, mouse_y = event.pos
    grid_x = mouse_x // GRID_SIZE
    grid_y = mouse_y // GRID_SIZE
    button_rect = pygame.Rect(start_button[0], start_button[1], 200, 50)

    if event.button == 1:  # Clic izquierdo: modificar terreno
        if 0 <= grid_y < ROWS and 0 <= grid_x < COLS:
            apply_influence(terrain, grid_x, grid_y, radius, intensity=3 if mode == "Elevate" else -3)
    elif event.button == 3:  # Clic derecho: cortar o continuar con el trazado
        if can_cut:  # Si es posible cortar, interrumpimos el trazado
            dragging_line = False
            can_cut = False  # Ya no se puede cortar una vez que la simulación comenzó
        else:  # Si no se ha cortado, comenzamos una nueva línea
            dragging_line = True
            if 0 <= grid_y < ROWS and 0 <= grid_x < COLS:
                lines.append((grid_x, grid_y))  # Empezar línea divisoria

    if event.button == 1 and button_rect.collidepoint(mouse_x, mouse_y) and not simulation_started:
        simulation_started = True  # Empieza la simulación

    return terrain, lines, dragging_line, simulation_started, can_cut

def handle_mouse_motion(event, terrain, radius, lines, dragging_line, mode):
    """Maneja el movimiento del ratón para dibujar divisorias y modificar terreno."""
    mouse_x, mouse_y = event.pos
    grid_x = mouse_x // GRID_SIZE
    grid_y = mouse_y // GRID_SIZE
    
    if pygame.mouse.get_pressed()[0]:  # Arrastrar para modificar terreno
        if 0 <= grid_y < ROWS and 0 <= grid_x < COLS:
            apply_influence(terrain, grid_x, grid_y, radius, intensity=3 if mode == "Elevate" else -3)

    if dragging_line:  # Arrastrar para dibujar línea divisoria
        if 0 <= grid_y < ROWS and 0 <= grid_x < COLS:
            if len(lines) > 0:
                lines[-1] = (grid_x, grid_y)  # Actualizar la última coordenada de la línea divisoria
    
    return lines

def handle_mouse_wheel(event, radius):
    """Maneja el evento de la rueda del mouse para ajustar el radio de influencia."""
    if event.y > 0:  # Rueda hacia arriba
        radius = min(20, radius + 1)
    elif event.y < 0:  # Rueda hacia abajo
        radius = max(1, radius - 1)
    return radius

def create_plates_from_lines(lines):
    """Convierte las líneas dibujadas en placas tectónicas"""
    if len(lines) < 2:
        return []
    
    plates = []
    current_points = []
    for point in lines:
        current_points.append(point)
    
    plate_type = random.choice(PLATE_TYPES)
    plates.append(TectonicPlate(current_points, plate_type))
    return plates

def simulate_plate_tectonics(terrain, plates):
    """Simula los efectos de las placas tectónicas"""
    if not plates:
        return terrain, []
    
    earthquake_points = []
    
    # Simular colisiones y efectos
    for plate in plates:
        for i in range(len(plate.points) - 1):
            x1, y1 = plate.points[i]
            x2, y2 = plate.points[i + 1]
            
            # Zona de deformación
            collision_radius = 5
            for y in range(max(0, int(y1-collision_radius)), min(ROWS, int(y1+collision_radius))):
                for x in range(max(0, int(x1-collision_radius)), min(COLS, int(x1+collision_radius))):
                    if 0 <= y < ROWS and 0 <= x < COLS:
                        # Probabilidad de efectos geológicos
                        if random.random() < 0.05:  # Actividad tectónica
                            if plate.type == 'continental':
                                # Formación de montañas
                                terrain[y][x] = min(15, terrain[y][x] + random.uniform(0.2, 0.5))
                                if random.random() < 0.01:  # Probabilidad de terremoto
                                    earthquake_points.append((x, y))
                            else:
                                # Subducción en placas oceánicas
                                terrain[y][x] = max(-1, terrain[y][x] - random.uniform(0.1, 0.3))
    
    return terrain, earthquake_points

def apply_erosion(terrain):
    """Aplica efectos de erosión al terreno"""
    for y in range(ROWS):
        for x in range(COLS):
            if terrain[y][x] > 0:  # Solo erosiona tierra sobre el nivel del mar
                # Erosión básica
                terrain[y][x] -= EROSION_RATE * random.random()
                
                # Erosión por pendiente
                for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < ROWS and 0 <= nx < COLS:
                        height_diff = terrain[y][x] - terrain[ny][nx]
                        if height_diff > 1:  # Si hay una pendiente pronunciada
                            terrain[y][x] -= height_diff * EROSION_RATE
                            terrain[ny][nx] += height_diff * EROSION_RATE * 0.5

def draw_geological_effects(screen, terrain, earthquake_points):
    """Dibuja efectos geológicos especiales"""
    # Dibujar volcanes en puntos altos
    for y in range(ROWS):
        for x in range(COLS):
            if terrain[y][x] > 10:  # Altura suficiente para volcán
                if random.random() < 0.001:  # Probabilidad de volcán
                    pygame.draw.circle(screen, COLORS['volcano'], 
                                    (x * GRID_SIZE, y * GRID_SIZE), 3)
    
    # Dibujar terremotos
    for x, y in earthquake_points:
        pygame.draw.circle(screen, COLORS['earthquake'],
                         (x * GRID_SIZE, y * GRID_SIZE), 4)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Generador de Terreno")
    clock = pygame.time.Clock()

    terrain = generate_terrain(ROWS, COLS)
    lines = []  # Almacena las coordenadas de las líneas divisorias
    radius = 5
    mode = "Elevate"
    dragging_line = False  # Flag para arrastre de la línea divisoria
    simulation_started = False
    can_cut = True  # Si es posible cortar la línea divisoria
    start_button = (WIDTH // 2 - 100, HEIGHT - 80)  # Posición del botón "Empezó la simulación"

    plates = []
    earthquake_points = []
    
    while True:
        screen.fill((0, 0, 0))  # Limpiar pantalla

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                terrain, lines, dragging_line, simulation_started, can_cut = handle_mouse_click(event, terrain, radius, lines, mode, dragging_line, simulation_started, start_button, can_cut)
            if event.type == pygame.MOUSEMOTION:
                lines = handle_mouse_motion(event, terrain, radius, lines, dragging_line, mode)
            if event.type == pygame.MOUSEWHEEL:
                radius = handle_mouse_wheel(event, radius)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Resetear el terreno
                    terrain = generate_terrain(ROWS, COLS)
                    lines = []  # Limpiar las líneas divisorias
                elif event.key == pygame.K_e:  # Alternar modo de elevar/reducir
                    mode = "Lower" if mode == "Elevate" else "Elevate"
        
        # Actualizar simulación
        if simulation_started:
            if not plates:
                plates = create_plates_from_lines(lines)
            terrain, earthquake_points = simulate_plate_tectonics(terrain, plates)
            apply_erosion(terrain)
        
        # Dibujar terreno
        draw_terrain(screen, terrain)
        
        # Dibujar líneas divisorias
        draw_dividing_lines(screen, lines)

        # Mostrar instrucciones
        draw_instructions(screen, simulation_started, can_cut)

        # Dibujar botón
        button_rect = draw_button(screen, pygame.mouse.get_pos(), start_button)

        draw_geological_effects(screen, terrain, earthquake_points)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
