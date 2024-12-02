import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import noise
import numpy as np

# Tamaño de la ventana
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 2  # Tamaño de cada celda
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE * 2  # Doble del ancho
FPS = 60

# Funciones para crear el terreno en 3D usando ruido Perlin
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
            noise_value = noise.pnoise2(x / scale, y / scale, octaves=6, persistence=0.5, lacunarity=2.0)
            height = int((noise_value + 1) * 7.5)  # Mapea valores de ruido (-1 a 1) a alturas (0-15)
            row.append(height)
        terrain.append(row)
    return terrain

def draw_cube(x, y, z, size):
    """Dibuja un cubo en la posición (x, y, z) con el tamaño 'size'."""
    vertices = [
        (x - size / 2, y - size / 2, z - size / 2),
        (x + size / 2, y - size / 2, z - size / 2),
        (x + size / 2, y + size / 2, z - size / 2),
        (x - size / 2, y + size / 2, z - size / 2),
        (x - size / 2, y - size / 2, z + size / 2),
        (x + size / 2, y - size / 2, z + size / 2),
        (x + size / 2, y + size / 2, z + size / 2),
        (x - size / 2, y + size / 2, z + size / 2)
    ]

    faces = [
        (0, 1, 2, 3),  # Front face
        (4, 5, 6, 7),  # Back face
        (0, 1, 5, 4),  # Left face
        (1, 2, 6, 5),  # Bottom face
        (2, 3, 7, 6),  # Right face
        (3, 0, 4, 7)   # Top face
    ]

    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_terrain(terrain, offset_x_left, offset_x_right):
    """Dibuja el terreno en 3D."""
    for y, row in enumerate(terrain):
        for x, height in enumerate(row):
            if 0 <= x - offset_x_left < COLS // 2:  # Placa izquierda
                color = get_color(height)
                glColor3fv(color)
                glPushMatrix()
                glTranslatef((x - offset_x_left) * GRID_SIZE, height * GRID_SIZE, y * GRID_SIZE)
                draw_cube(0, 0, 0, GRID_SIZE)  # Usamos la nueva función para dibujar el cubo
                glPopMatrix()
            elif COLS // 2 <= x - offset_x_right < COLS:  # Placa derecha
                color = get_color(height)
                glColor3fv(color)
                glPushMatrix()
                glTranslatef((x - offset_x_right) * GRID_SIZE, height * GRID_SIZE, y * GRID_SIZE)
                draw_cube(0, 0, 0, GRID_SIZE)  # Usamos la nueva función para dibujar el cubo
                glPopMatrix()

def main():
    pygame.init()
    display = (WIDTH, HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(-WIDTH / 2, -HEIGHT / 2, -200)  # Desplazamiento inicial
    clock = pygame.time.Clock()

    terrain = generate_terrain(ROWS, COLS)
    offset_x_left, offset_x_right = 0, COLS // 2  # Offset para las placas
    running = True

    while running:
        # Limpiar la pantalla antes de dibujar nuevamente
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                terrain = generate_terrain(ROWS, COLS)  # Reinicia el terreno
                offset_x_left, offset_x_right = 0, COLS // 2

        # Dibujar terreno de ambas placas
        draw_terrain(terrain, offset_x_left, offset_x_right)

        # Mover las placas hacia el centro
        if offset_x_left < COLS // 2 and offset_x_right > COLS // 2:
            offset_x_left += 1
            offset_x_right -= 1

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()