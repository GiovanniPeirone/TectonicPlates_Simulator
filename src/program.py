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
        WHITE =     (255, 255, 255)
        # ------------------ Codigo -------------------------------
        
        mapArr = []

        new_world = map.maps(20,20)
        #new_world.Maping()
        
        for i in new_world.height:
            for o in new_world.widhgt:
                mapArr[i][o].append(1)

        for i in mapArr:
            if mapArr[i] == 1:
                pygame.draw.circle(screen, WHITE, i, 20)

        


        # fill the screen with a color to wipe away anything from last frame
        

        dt = clock.tick(60) / 1000

    pygame.quit()