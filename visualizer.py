import pygame
import board

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GAME")

#create the grid
board = board.Board(10, 10)
board.set_view(150, 100, 50)

#game loop
run = True

while run:

    #render the grid
    board.render(SCREEN)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()