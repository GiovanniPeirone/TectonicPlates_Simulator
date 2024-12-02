import pygame
import random
import math
import noise  # Para la generación procedural de terreno con Perlin Noise
import numpy as np
from pygame import gfxdraw

# Configuración inicial
WIDTH, HEIGHT = 800, 600  # Tamaño de la pantalla
GRID_SIZE = 2  # Tamaño de cada celda
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE  # Reajustamos para que se dibuje correctamente
FPS = 60
NOISE_SCALE = 100.0  # Escala para el ruido Perlin

# Colores para representar diferentes alturas
COLORS = {
    'water_deep': (0, 0, 139),      # Agua profunda
    'water': (0, 191, 255),         # Agua
    'water_shallow': (65, 105, 225), # Agua poco profunda
    'beach': (238, 214, 175),       # Playa
    'land': (34, 139, 34),          # Tierra
    'forest': (0, 100, 0),          # Bosque
    'mountain': (139, 137, 137),    # Montañas
    'snow': (255, 250, 250),        # Nieve
    'volcano': (165, 42, 42),       # Volcán
    'lava': (255, 69, 0),          # Lava
    'earthquake': (255, 215, 0),    # Terremoto
    'ui_bg': (45, 45, 45),         # Fondo UI
    'ui_button': (65, 65, 65),     # Botones
    'ui_hover': (85, 85, 85),      # Hover
    'ui_text': (200, 200, 200)     # Texto
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

class UI:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 16)
        self.title_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.buttons = {}
        self.sidebar_width = 200
        self.controls = {
            'simulation_speed': 1.0,
            'erosion_rate': 0.01,
            'volcanic_activity': 0.5,
            'earthquake_probability': 0.3
        }
        self.start_button = pygame.Rect(WIDTH - self.sidebar_width + 10, HEIGHT - 60, 180, 40)
        self.active_slider = None

    def handle_mouse_interaction(self, pos, clicked=False):
        """Maneja la interacción del mouse con los controles"""
        x, y = pos
        y_pos = 60
        for control_name in self.controls:
            slider_rect = pygame.Rect(WIDTH - self.sidebar_width + 10, y_pos + 20, 160, 10)
            if clicked and slider_rect.collidepoint(x, y - 5):
                self.active_slider = control_name
            elif clicked and not slider_rect.collidepoint(x, y - 5):
                self.active_slider = None
            
            if self.active_slider == control_name:
                relative_x = max(0, min(1, (x - slider_rect.x) / slider_rect.width))
                self.controls[control_name] = round(relative_x, 2)
            
            y_pos += 50

    def draw_sidebar(self, screen, simulation_started):
        # Dibujar fondo del panel lateral
        sidebar = pygame.Rect(WIDTH - self.sidebar_width, 0, self.sidebar_width, HEIGHT)
        pygame.draw.rect(screen, COLORS['ui_bg'], sidebar)
        
        # Título
        title = self.title_font.render("Panel de Control", True, COLORS['ui_text'])
        screen.blit(title, (WIDTH - self.sidebar_width + 10, 10))

        # Controles deslizantes
        y_pos = 60
        for control_name, value in self.controls.items():
            # Nombre del control
            label = self.font.render(f"{control_name.replace('_', ' ').title()}", True, COLORS['ui_text'])
            screen.blit(label, (WIDTH - self.sidebar_width + 10, y_pos))
            
            # Valor actual
            value_text = self.font.render(f"{value:.2f}", True, COLORS['ui_text'])
            value_pos = (WIDTH - self.sidebar_width + 170, y_pos)
            screen.blit(value_text, value_pos)
            
            # Barra deslizante
            slider_rect = pygame.Rect(WIDTH - self.sidebar_width + 10, y_pos + 20, 160, 10)
            pygame.draw.rect(screen, COLORS['ui_button'], slider_rect)
            
            # Indicador de posición
            handle_pos = slider_rect.x + value * slider_rect.width
            handle_rect = pygame.Rect(handle_pos - 5, slider_rect.y - 5, 10, 20)
            pygame.draw.rect(screen, COLORS['ui_text'], handle_rect)
            
            y_pos += 50

        # Botón de inicio/reinicio
        button_color = COLORS['ui_hover'] if simulation_started else COLORS['ui_button']
        pygame.draw.rect(screen, button_color, self.start_button)
        button_text = "Reiniciar" if simulation_started else "Iniciar Simulación"
        text = self.font.render(button_text, True, COLORS['ui_text'])
        text_rect = text.get_rect(center=self.start_button.center)
        screen.blit(text, text_rect)

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

def handle_mouse_click(event, terrain, radius, lines, mode, dragging_line, simulation_started, ui, can_cut):
    """Maneja los clics del ratón y actualiza el estado del terreno y líneas divisorias."""
    mouse_x, mouse_y = event.pos

    # Verificar si el clic fue en la UI
    if mouse_x > WIDTH - ui.sidebar_width:
        if ui.start_button.collidepoint(event.pos):
            simulation_started = not simulation_started
            if simulation_started:
                can_cut = False
        ui.handle_mouse_interaction(event.pos, True)
        return terrain, lines, dragging_line, simulation_started, can_cut

    grid_x = mouse_x // GRID_SIZE
    grid_y = mouse_y // GRID_SIZE

    if event.button == 1:  # Clic izquierdo
        if 0 <= grid_y < ROWS and 0 <= grid_x < COLS:
            apply_influence(terrain, grid_x, grid_y, radius, intensity=3 if mode == "Elevate" else -3)
    elif event.button == 3:  # Clic derecho
        if can_cut:
            dragging_line = False
            can_cut = False
        else:
            dragging_line = True
            if 0 <= grid_y < ROWS and 0 <= grid_x < COLS:
                lines.append((grid_x, grid_y))

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

def add_visual_effects(screen, terrain, earthquake_points):
    """Añade efectos visuales avanzados"""
    # Efecto de brillo para agua
    for y in range(ROWS):
        for x in range(COLS):
            if terrain[y][x] < 0:  # Agua
                if random.random() < 0.001:
                    brightness = random.randint(100, 255)
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if 0 <= x * GRID_SIZE + dx < WIDTH and 0 <= y * GRID_SIZE + dy < HEIGHT:
                                pygame.gfxdraw.pixel(screen, 
                                                   x * GRID_SIZE + dx, 
                                                   y * GRID_SIZE + dy, 
                                                   (brightness, brightness, brightness, 100))

    # Efectos de partículas para terremotos
    for x, y in earthquake_points:
        for _ in range(8):  # Más partículas
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            alpha = random.randint(50, 200)
            size = random.randint(1, 3)
            pos = (int(x * GRID_SIZE + offset_x), int(y * GRID_SIZE + offset_y))
            if 0 <= pos[0] < WIDTH and 0 <= pos[1] < HEIGHT:
                pygame.draw.circle(screen, (*COLORS['earthquake'], alpha), pos, size)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulador de Placas Tectónicas")
    clock = pygame.time.Clock()
    ui = UI()

    terrain = generate_terrain(ROWS, COLS)
    lines = []
    radius = 5
    mode = "Elevate"
    dragging_line = False
    simulation_started = False
    can_cut = True
    plates = []
    earthquake_points = []
    
    while True:
        screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                terrain, lines, dragging_line, simulation_started, can_cut = handle_mouse_click(
                    event, terrain, radius, lines, mode, dragging_line, simulation_started, ui, can_cut)
            if event.type == pygame.MOUSEMOTION:
                if mouse_pos[0] > WIDTH - ui.sidebar_width:
                    ui.handle_mouse_interaction(mouse_pos)
                else:
                    lines = handle_mouse_motion(event, terrain, radius, lines, dragging_line, mode)
            if event.type == pygame.MOUSEWHEEL:
                radius = handle_mouse_wheel(event, radius)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    terrain = generate_terrain(ROWS, COLS)
                    lines = []
                    simulation_started = False
                    can_cut = True
                elif event.key == pygame.K_e:
                    mode = "Lower" if mode == "Elevate" else "Elevate"
        
        if simulation_started:
            if not plates:
                plates = create_plates_from_lines(lines)
            terrain, earthquake_points = simulate_plate_tectonics(terrain, plates)
            apply_erosion(terrain)
        
        draw_terrain(screen, terrain)
        draw_dividing_lines(screen, lines)
        add_visual_effects(screen, terrain, earthquake_points)
        
        ui.draw_sidebar(screen, simulation_started)
        draw_instructions(screen, simulation_started, can_cut)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
