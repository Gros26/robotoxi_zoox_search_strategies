import pygame
import board
import search
import player

move_delay = 200
last_move = 0
route_index = 0

#init the game
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GAME")

#create the city
city = search.City("city1.txt")

#create the grid
board = board.Board(10, 10, city.matrix)
board.set_view(150, 100, 50)

#create the player that represent the robotaxi
player = player.Player(2, 0, board)

#
#obtain the route
robotaxi = search.Robotaxi(*(city.start), city) 
route = robotaxi.get_route(robotaxi.ucs())

#game loop
run = True

while run:

    #render the grid
    board.render(SCREEN)
    player.draw(SCREEN, 50)

    current_time = pygame.time.get_ticks()

    if route_index < len(route):

        if current_time - last_move > move_delay:

            row, column, _ = route[route_index]

            player.x = column
            player.y = row

            route_index += 1
            last_move = current_time

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()