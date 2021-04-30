# Create window and display functions to visualize the simulation results

import pygame
pygame.font.init()

class display:
    def __init__(self, sizeX, sizeY, initialgrid):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.grid = initialgrid
        self.window = pygame.display.set_mode( (sizeX,sizeY) )
        pygame.display.set_caption("Reaction-Diffusion Simulation")

    def update(self, grid):
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                pygame.draw.rect(self.window, (int(255*self.grid[0][x][y]), int(255*self.grid[1][x][y]), 0), (x,y,1,1), 0) # surface, color, position and size, fillmode
        pygame.display.update()