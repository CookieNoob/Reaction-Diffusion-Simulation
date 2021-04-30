import numpy as np
import copy
import random
import RD_Grafics
import pygame
import time
random.seed()



def laplace(grid):
    # returns the second order derivative of the grid. The border is treated by copying the result at the position one pixel away from the border to the outer pixels.
    sizeX, sizeY = len(grid), len(grid[0])
    if sizeX < 3 or sizeY < 3:
        raise Exception('Array is too small to calculate the second derivative')
    
    mask = [[0.05,0.2,0.05],[0.2,-1,0.2],[0.05,0.2,0.05]]
    
    result = []
    for x in range(1, sizeX-1):
        resultline = []
        for y in range(1,sizeY-1):
            value = 0
            for xm in range(-1,2):
                for ym in range(-1,2):
                    value += mask[xm][ym]*grid[x+xm][y+ym]
            resultline.append(value)
        resultline.insert(0,resultline[0])
        resultline.append(value)
        result.append(resultline)
    result.insert(0,result[0])
    result.append(resultline)
    return result



def diffusionTimestep(Conc, DA, DB, feed, kill, dt):
    sizeX, sizeY = len(Conc[0]), len(Conc[0][0])
    newconcentration = [[[0 for y in range(sizeY)] for x in range(sizeX)] for i in range(2)]
    secDer = [laplace(Conc[0]), laplace(Conc[1])]
    for x in range(sizeX):
        for y in range(sizeY):
            # the new concentration is the sum or difference of the following: 
            #   old concentration
            #   diffusion from neighbors
            #   transmutation from A to B
            #   feedrate of A into the system
            # whereas the change from the original value is multiplied by the size of the timestep
            newconcentration[0][x][y] = Conc[0][x][y]                           \
                                        + (DA * secDer[0][x][y]                 \
                                        - Conc[0][x][y] * (Conc[1][x][y] ** 2)  \
                                        + feed * (1 - Conc[0][x][y]))           \
                                        * dt                                    
                                           
            newconcentration[1][x][y]   = Conc[1][x][y]                         \
                                        + (DB * secDer[1][x][y]                 \
                                        + Conc[0][x][y] * (Conc[1][x][y] ** 2)  \
                                        + (feed + kill) * Conc[1][x][y])        \
                                        * dt                                    
    return newconcentration







def main():
    sizeX, sizeY    = 400   , 500
    DA, DB          = 1.0   , 0.5
    feed, kill      = 0.055 , 0.062
    dt              = 1.0
    
    SubstanceA = [[0 for y in range(sizeY)] for x in range(sizeX)] 
    SubstanceB = [[0.5 for y in range(sizeY)] for x in range(sizeX)] 

    Concentrations = []
    Concentrations.append(SubstanceA)
    Concentrations.append(SubstanceB)
    
    diffusionTimestep(Concentrations, DA, DB, feed, kill, dt)
    
    window = RD_Grafics.display(sizeX, sizeY, Concentrations)

    running = True
    paint = False
    simulate = False
    step = 0
    while(running):
        for keystroke in pygame.event.get():
            if keystroke.type == pygame.MOUSEBUTTONDOWN:
                if keystroke.button == 1:       # left mousebutton
                    paint = True
                    color = 0
                    simulate = True
                if keystroke.button == 3:       # right mousebutton
                    paint = True
                    color = 1
                    simulate = False
            if keystroke.type == pygame.QUIT:
                running = False
        if paint:
            pass
        
        if simulate:
            print("updatestep", step)
            step += 1
            time.sleep(0.04)
            Concentrations = diffusionTimestep(Concentrations, DA, DB, feed, kill, dt)
            window.update(Concentrations)
        


if __name__ == "__main__":
    main()