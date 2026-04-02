import pygame

class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy, board):
        new_x = self.x + dx
        new_y = self.y + dy

        if board.grid[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

    def draw(self, screen, tile_size):

        rect = pygame.Rect(
            self.x * tile_size,
            self.y * tile_size,
            tile_size,
            tile_size
        )

        pygame.draw.rect(screen, (0,255,0), rect)