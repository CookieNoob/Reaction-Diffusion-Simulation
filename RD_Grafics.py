# Create window and display functions to visualize the simulation results

import pygame
pygame.font.init()

class display:
    def __init__(self, sizeX, sizeY, initialgrid, scalefactor):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.window = pygame.display.set_mode( (scalefactor * sizeX, scalefactor * sizeY) )
        self.scalefactor = scalefactor
        pygame.display.set_caption("Reaction-Diffusion Simulation")
        self.update(initialgrid)

    def update(self, grid):
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                pygame.draw.rect(self.window, (0, int(178*grid[0][x][y]), int(220*grid[1][x][y])), (self.scalefactor*x, self.scalefactor*y, self.scalefactor, self.scalefactor), 0) # surface, color, position and size, fillmode
        pygame.display.update()