import pygame
import map

def program():
    pygame.init()
    screen = pygame.display.set_mode((1180, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        # ------------------ Codigo -------------------------------

        new_world = map.map(20,20)
        new_world.Maping()

        # fill the screen with a color to wipe away anything from last frame
        

        dt = clock.tick(60) / 1000

    pygame.quit()