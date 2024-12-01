import pygame
import random
import numpy as np
import sys
from pygame.locals import *
from collections import deque

# Configuración de la ventana y parámetros
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 15
NUM_PLATES = 5
EVENT_PROBABILITY = 0.02  # Probabilidad de un evento aleatorio (terremoto)
PLATE_SPEED = 1  # Velocidad de movimiento de las placas

# Colores suaves y seguros
WATER_COLOR = (0, 102, 204)  # Azul tranquilo para el agua
TERRAIN_COLOR = (139, 69, 19)  # Marrón para el terreno
MOUNTAIN_COLOR = (101, 67, 33)  # Marrón oscuro para las montañas
PLATE_COLOR = (173, 216, 230)  # Azul claro para las placas
BUTTON_COLOR = (0, 153, 0)  # Verde suave para los botones
BUTTON_HOVER_COLOR = (0, 128, 0)  # Verde oscuro para el hover de botones
LIGHT_COLOR = (255, 255, 255)  # Blanco para iluminar las zonas elevadas

# Función para mejorar la forma de los continentes (algoritmo de difusión)
def generate_terrain_map(width, height):
    terrain_map = np.random.random((height, width))  # Crear un mapa de terreno aleatorio

    # Aplicar suavizado para generar un terreno más realista (Filtro de promedio 3x3)
    for y in range(1, height-1):
        for x in range(1, width-1):
            neighborhood = terrain_map[y-1:y+2, x-1:x+2]
            terrain_map[y, x] = np.mean(neighborhood)
    
    # Convertir valores para representar agua (0) y tierra (1)
    terrain_map = np.where(terrain_map < 0.5, 255, 1)  # Agua o tierra
    return terrain_map

# Algoritmo para identificar continentes (búsqueda en profundidad)
def find_continents(terrain):
    visited = np.zeros_like(terrain)
    continents = []
    
    def dfs(x, y, continent_id):
        stack = deque([(x, y)])
        continent = []
        while stack:
            cx, cy = stack.pop()
            if 0 <= cx < len(terrain[0]) and 0 <= cy < len(terrain) and terrain[cy][cx] == 1 and not visited[cy][cx]:
                visited[cy][cx] = 1
                continent.append((cx, cy))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    stack.append((cx + dx, cy + dy))
        return continent

    for y in range(len(terrain)):
        for x in range(len(terrain[0])):
            if terrain[y][x] == 1 and not visited[y][x]:
                continent = dfs(x, y, len(continents))
                continents.append(continent)
    
    return continents

class Plate:
    def __init__(self, plate_id, x, y, color):
        self.plate_id = plate_id
        self.color = color
        self.blocks = {(x, y)}
        self.direction = np.array([random.choice([-1, 0, 1]), random.choice([-1, 0, 1])])  # Movimiento aleatorio
        self.speed = PLATE_SPEED

    def move(self, terrain_width, terrain_height):
        new_blocks = set()
        for x, y in self.blocks:
            new_x = (x + self.direction[0] * self.speed) % terrain_width
            new_y = (y + self.direction[1] * self.speed) % terrain_height
            new_blocks.add((new_x, new_y))
        self.blocks = new_blocks

    def handle_collision(self, terrain):
        for x, y in self.blocks:
            if 0 <= x < len(terrain[0]) and 0 <= y < len(terrain):
                terrain[y][x] = self.plate_id + 1  # Asignar el id de la placa al terreno

    def add_block(self, x, y):
        self.blocks.add((x, y))

    def interact_with_plates(self, terrain, plates):
        for x, y in self.blocks:
            if 0 <= x < len(terrain[0]) and 0 <= y < len(terrain):
                neighbor_plate_id = terrain[y][x] - 1
                if neighbor_plate_id != self.plate_id and neighbor_plate_id >= 0:
                    plates[neighbor_plate_id].create_mountains(terrain, x, y)

    def create_mountains(self, terrain, x, y):
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if 0 <= x + dx < len(terrain[0]) and 0 <= y + dy < len(terrain):
                    terrain[y + dy][x + dx] = max(terrain[y + dy][x + dx], 2)  # Elevar el terreno

    def render(self, screen, block_size):
        for x, y in self.blocks:
            shadow_offset = 3
            pygame.draw.circle(screen, (50, 50, 50), (int(x * block_size + block_size / 2) + shadow_offset, int(y * block_size + block_size / 2) + shadow_offset), block_size // 2)
            pygame.draw.circle(screen, self.color, (int(x * block_size + block_size / 2), int(y * block_size + block_size / 2)), block_size // 2)

def initialize_plates(width, height, map_data):
    plates = []
    for i in range(NUM_PLATES):
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        while map_data[y][x] == 255:  # Si es agua, buscamos otro punto
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        plates.append(Plate(i, x, y, (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))))  # Color aleatorio
    return plates

def generate_earthquake(terrain):
    if random.random() < EVENT_PROBABILITY:
        x = random.randint(0, len(terrain[0]) - 1)
        y = random.randint(0, len(terrain) - 1)
        magnitude = random.randint(4, 9)  # Magnitud aleatoria
        print(f"Sismo generado en ({x}, {y}) con magnitud {magnitude}")
        # Simulamos el daño del terremoto afectando el terreno
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if 0 <= x + dx < len(terrain[0]) and 0 <= y + dy < len(terrain):
                    terrain[y + dy][x + dx] = max(0, terrain[y + dy][x + dx] - magnitude)

def render_map(screen, terrain, plates, block_size, continents):
    for y in range(len(terrain)):
        for x in range(len(terrain[y])):
            value = terrain[y][x]
            if value == 0:
                color = WATER_COLOR  # Agua
            elif value == 1:
                color = TERRAIN_COLOR  # Terreno
            else:
                color = MOUNTAIN_COLOR  # Montañas (cuando el terreno está elevado)

            pygame.draw.rect(screen, color, (x * block_size, y * block_size, block_size, block_size))
            if value > 1:  # Agregar iluminación a las zonas elevadas
                pygame.draw.rect(screen, LIGHT_COLOR, (x * block_size, y * block_size, block_size, block_size), 2)

    # Dibujar los continentes con colores dinámicos
    for continent in continents:
        continent_color = (random.randint(120, 180), random.randint(120, 180), random.randint(120, 180))
        for x, y in continent:
            pygame.draw.rect(screen, continent_color, (x * block_size, y * block_size, block_size, block_size))

    # Dibujar las placas con sombras y efectos
    for plate in plates:
        plate.render(screen, block_size)

def draw_ui(screen):
    font = pygame.font.SysFont('Arial', 24)
    earthquake_button = pygame.Rect(600, 10, 180, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, earthquake_button)
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR, earthquake_button, 2)
    text = font.render('Generar Terremoto', True, (255, 255, 255))
    screen.blit(text, (earthquake_button.x + 10, earthquake_button.y + 10))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Simulador de Placas Tectónicas')

    terrain = generate_terrain_map(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE)
    continents = find_continents(terrain)
    plates = initialize_plates(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE, terrain)

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((0, 0, 0))  # Fondo negro
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Lógica del simulador
        generate_earthquake(terrain)

        for plate in plates:
            plate.move(WINDOW_WIDTH // BLOCK_SIZE, WINDOW_HEIGHT // BLOCK_SIZE)
            plate.handle_collision(terrain)
            plate.interact_with_plates(terrain, plates)

        render_map(screen, terrain, plates, BLOCK_SIZE, continents)
        draw_ui(screen)

        pygame.display.flip()
        clock.tick(30)  # FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()