import pygame

pygame.init()
screen = pygame.display.set_mode(size=(1000, 800))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #Close Screen
            quit() #End
