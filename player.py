import pygame

class Player:

    def __init__(self, y, x, board):
        self.x = x
        self.y = y
        self.board = board

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if self.board.grid[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

    def draw(self, screen, tile_size):

        rect = pygame.Rect(
            self.x * tile_size + self.board.left,
            self.y * tile_size + self.board.top,
            tile_size,
            tile_size
        )

        pygame.draw.rect(screen, (0,255,0), rect)