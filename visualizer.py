import pygame
import board
import search
import player

#this is only for run, i think that after this will be must eliminate
city = search.City("city1.txt")

#game--------

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GAME")

#create the grid
board = board.Board(10, 10, city.matrix)
board.set_view(150, 100, 50)

#create the player
player = player.Player(2,0)

#game loop
run = True

while run:

    #render the grid
    board.render(SCREEN)
    player.draw(SCREEN, 30)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()