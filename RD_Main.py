import numpy as np
import copy
import random
import RD_Grafics
import pygame
random.seed()



def main():
    sizeX, sizeY = 400, 500
    
    SubstanceA = [[0 for y in range(sizeY)] for x in range(sizeX)] 
    SubstanceB = [[0 for y in range(sizeY)] for x in range(sizeX)] 

    Concentrations = []
    Concentrations.append(SubstanceA)
    Concentrations.append(SubstanceB)
    
    window = RD_Grafics.display(sizeX, sizeY, Concentrations)

    running = True
    paint = False
    while(running):
        for keystroke in pygame.event.get():
            if keystroke.type == pygame.MOUSEBUTTONDOWN:
                if keystroke.button == 1:       # left mousebutton
                    paint = True
                    color = 0
                if keystroke.button == 3:       # right mousebutton
                    paint = True
                    color = 1
            if keystroke.type == pygame.QUIT:
                running = False
        if paint:
            pass
        


if __name__ == "__main__":
    main()