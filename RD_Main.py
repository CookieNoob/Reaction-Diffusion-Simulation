import numpy as np
import copy
import random
import RD_Grafics
import pygame
import time
random.seed()



def laplace(grid):
    # input:  any two dimensional array
    # output: returns the second order derivative of the grid. The border is treated by copying the result at the position one pixel away from the border to the outer pixels.
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
                    value += mask[xm+1][ym+1]*grid[x+xm][y+ym]
            resultline.append(value)
        resultline.insert(0,-0.5)
        resultline.append(-0.5)
        result.append(resultline)
    result.insert(0,[-0.5 for i in range(sizeY)])
    result.append([-0.5 for i in range(sizeY)])
    return result




def diffusionTimestep(Conc, DA, DB, feed, kill, dt):
    # calculate the concentration one timestep later based on the diffusion and addition of substances
    # input : Concentration in the current timestep, diffusion coefficients for both substances, feedrate
    #         killrate and time step size
    # output: returns the new concentrations 
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
                                        - (feed + kill) * Conc[1][x][y])        \
                                        * dt 
            for i in range(2):
                if newconcentration[i][x][y] > 1:
                    newconcentration[i][x][y] = 1
                if newconcentration[i][x][y] < 0:
                    newconcentration[i][x][y] = 0
    return newconcentration


def addConcentration(Concentrations, color, scalefactor):
    # Changes the concentrations based on user input
    # input : current concentrations, type of substance to be added, scale of the window
    # output: none
    mov = pygame.mouse.get_rel()
    pos = pygame.mouse.get_pos()
    
    maxm = max(mov)
    if maxm == 0:
        return
    
    sizeX, sizeY = len(Concentrations[0]), len(Concentrations[0][0])
    
    if maxm > 0.1 * sizeX * scalefactor:
        return
        
    if pos[0] >= sizeX * scalefactor or pos[1]  >= sizeY * scalefactor:
        return
    if pos[0]+mov[0] >= sizeX * scalefactor or pos[1] + mov[1] >= sizeY * scalefactor:
        return
    
    for s in range(maxm+1):
        Concentrations[color]                                                   \
                          [(pos[0] + int(s * mov[0]/maxm))//scalefactor]        \
                          [(pos[1] + int(s * mov[1]/maxm))//scalefactor] += 0.3
                          
        if Concentrations[color]                                                \
                          [(pos[0] + int(s * mov[0]/maxm))//scalefactor]        \
                          [(pos[1] + int(s * mov[1]/maxm))//scalefactor] > 1:
            Concentrations[color]                                               \
                          [(pos[0] + int(s * mov[0]/maxm))//scalefactor]        \
                          [(pos[1] + int(s * mov[1]/maxm))//scalefactor] = 1
    
    
    
    
    
    
    


def main():
    sizeX, sizeY    = 100   , 100
    DA, DB          = 1.0   , 0.5
    # feed, kill      = 0.045 , 0.062 # standard value
    feed, kill      = 0.0545, 0.062 # coral
    dt              = 1.0
    scalefactor     = 3
    
    SubstanceA = [[1 for y in range(sizeY)] for x in range(sizeX)] 
    SubstanceB = [[0 for y in range(sizeY)] for x in range(sizeX)] 

    for x in range(int(8*sizeX/20), int(12*sizeX/20)):
        for y in range(int(8*sizeY/20), int(12*sizeY/20)):
            SubstanceB[x][y] = 1
    for x in range(int(4*sizeX/20), int(5*sizeX/20)):
        for y in range(int(5*sizeY/20), int(6*sizeY/20)):
            SubstanceB[x][y] = 1
    for x in range(int(4*sizeX/20), int(5*sizeX/20)):
        for y in range(int(8*sizeY/20), int(9*sizeY/20)):
            SubstanceB[x][y] = 1
    for x in range(int(4*sizeX/20), int(5*sizeX/20)):
        for y in range(int(14*sizeY/20), int(16*sizeY/20)):
            SubstanceB[x][y] = 1
            
    Concentrations = []
    Concentrations.append(SubstanceA)
    Concentrations.append(SubstanceB)
    
    window = RD_Grafics.display(sizeX, sizeY, Concentrations, scalefactor)

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
                if keystroke.button == 3:       # right mousebutton
                    paint = True
                    color = 1
            if keystroke.type == pygame.MOUSEBUTTONUP:
                paint = False
            if keystroke.type == pygame.QUIT:
                running = False
            if keystroke.type == pygame.KEYDOWN:
                if keystroke.key == pygame.K_SPACE:
                    simulate = not simulate
        if paint:
            time.sleep(0.01)
            addConcentration(Concentrations, color, scalefactor)
            window.update(Concentrations)
        
        if simulate:
            print("updatestep", step)
            step += 1
            Concentrations = diffusionTimestep(Concentrations, DA, DB, feed, kill, dt)
            window.update(Concentrations)
        


if __name__ == "__main__":
    main()