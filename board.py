import pygame

class Board:
    def __init__(self, width, height, matrix):
        self.width = width
        self.height = height
        self.board = [[0]*width for _ in range(height)]
        self.matrix = matrix

    def set_view(self, left, top, cell_size):
        self.left = left #position where init the board
        self.top = top #position where init the board
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (255,255,255), (
                    x * self.cell_size + self.left,
                    y * self.cell_size + self.top,
                    self.cell_size,
                    self.cell_size), 1)