# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 09:53:56 2021

@author: Chirayu
"""

'''Pathfinding Algorithm to find shortest path between two nodes. Make a class of grid points
the grid points will contain the g cost (from start), h cost (from end) from which the fcost is implied.
 will also contain colour (for whether it is being checked on a boundary, node, normal). The grid points
 will also contain parent which gives it the lowest fcost.
 '''

import pygame
import random
import time
grid=(100,50)
blue=(0,0,255)
red=(255,0,0)
green=(0,255,0)
white=(255,255,255)
black=(0,0,0)
cyan=(0,255,255)
pixel=10 #number of pixels each square is across
#gen_per_frame=1
#frame_per_sec=2
class point():
    def __init__(self, x, y, Node):
        '''
        black squares are the default ones in the grid.
        white squares correspond to obstacles
        red squares correspond to the minimal cost square for a given iteration of the algorithm
        green squares correspond to the squares whose costs have been caluclated'''
        
        self.gcost=0
        self.hcost=0
        self.colour=black
        self.x=x
        self.y=y
        self.producer=[]
        
def Make_grid(grid):
    #This function makes the initial random grid with obstacles
    squares=[[point(j, i, False) for i in range(grid[1])]for j in range(grid[0])]
    print(len(squares))
    print(len(squares[0]))
    obstacles_no=random.randint(int(38*grid[0]), int(42*grid[0]))#can change numbers in this to adjust no of obstacles
    for i in range(obstacles_no):
        x=random.randint(1, grid[0]-1)
        y=random.randint(1, grid[1]-1)
        squares[x][y].colour=white #obstacle is represented by white
    node1x=random.randint(18, grid[0]-15) #Make the node somewhat away from the edges
    node1y=random.randint(18, grid[1]-15)
    squares[node1x][node1y].colour=blue
    node2x=random.randint(18, grid[0]-15)
    node2y=random.randint(18, grid[1]-15)
    squares[node2x][node2y].colour=blue
    return squares, node1x, node1y, node2x, node2y


def dist(point, end):
    return (((end[0]-point.x)**2+(end[1]-point.y)**2)**0.5)

def cost( end, squares,i,j): 
    '''This function goes over all the neighbouring squares, if they are not red or white (obstacles) then a cost
    is calculated for the grid points. Note that the costs are only updated if they are less than the previous
    cost or if a cost has not been assigned yet. Note that parent.x can easily be replaced by i, and 
    parent.y can be replaced by j and this would improve efficiency'''
    parent=squares[i][j]
    a=parent.gcost+parent.hcost+1
    c=parent.gcost+parent.hcost+1.414
    if i+1<=grid[0]-1 and j<=grid[1]-1:
        if squares[parent.x+1][parent.y].colour!=white and squares[parent.x+1][parent.y].colour!=red:
            if a<squares[parent.x+1][parent.y].gcost+squares[parent.x+1][parent.y].hcost or squares[parent.x+1][parent.y].gcost+squares[parent.x+1][parent.y].hcost==0:
                squares[parent.x+1][parent.y].producer=[i,j]
                squares[parent.x+1][parent.y].colour=green
                squares[parent.x+1][parent.y].gcost=parent.gcost+1
                squares[parent.x+1][parent.y].hcost=dist(squares[parent.x+1][parent.y], end)
    if i<=grid[0]-1 and j+1<=grid[1]-1 :
        if squares[parent.x][parent.y+1].colour!=white and squares[parent.x][parent.y+1].colour!=red:
            if a<squares[parent.x][parent.y+1].gcost+squares[parent.x][parent.y+1].hcost or squares[parent.x][parent.y+1].gcost+squares[parent.x][parent.y+1].hcost==0:
                squares[parent.x][parent.y+1].producer=[i,j]
                squares[parent.x][parent.y+1].colour=green
                squares[parent.x][parent.y+1].gcost=parent.gcost+1
                squares[parent.x][parent.y+1].hcost=dist(squares[parent.x][parent.y+1], end)
    if i<=grid[0]-1 and j-1<=grid[1]-1 and j-1>=0:
        if squares[parent.x][parent.y-1].colour!=white and squares[parent.x][parent.y-1].colour!=red:
            if a<squares[parent.x][parent.y-1].gcost+squares[parent.x][parent.y-1].hcost or squares[parent.x][parent.y-1].gcost+squares[parent.x][parent.y-1].hcost==0:
                squares[parent.x][parent.y-1].producer=[i,j]
                squares[parent.x][parent.y-1].colour=green
                squares[parent.x][parent.y-1].gcost=parent.gcost+1
                squares[parent.x][parent.y-1].hcost=dist(squares[parent.x][parent.y-1], end)
    if i-1<=grid[0]-1 and j<=grid[1]-1 and i-1>=0:
        if squares[parent.x-1][parent.y].colour!=white and squares[parent.x-1][parent.y].colour!=red:
            if a<squares[parent.x-1][parent.y].gcost+squares[parent.x-1][parent.y].hcost or squares[parent.x-1][parent.y].gcost+squares[parent.x-1][parent.y].hcost==0:
                squares[parent.x-1][parent.y].producer=[i,j]
                squares[parent.x-1][parent.y].colour=green
                squares[parent.x-1][parent.y].gcost=parent.gcost+1
                squares[parent.x-1][parent.y].hcost=dist(squares[parent.x-1][parent.y], end)
    if i-1<=grid[0]-1 and j+1<=grid[1]-1 and i-1>=0:
        if squares[parent.x-1][parent.y+1].colour!=white and squares[parent.x-1][parent.y+1].colour!=red:
            if c<squares[parent.x-1][parent.y+1].gcost+squares[parent.x-1][parent.y+1].hcost or squares[parent.x-1][parent.y+1].gcost+squares[parent.x-1][parent.y+1].hcost==0:
                squares[parent.x-1][parent.y+1].producer=[i,j]
                squares[parent.x-1][parent.y+1].colour=green
                squares[parent.x-1][parent.y+1].gcost=parent.gcost+1
                squares[parent.x-1][parent.y+1].hcost=dist(squares[parent.x-1][parent.y+1], end)
    if i+1<=grid[0]-1 and j+1<=grid[1]-1:
        if squares[parent.x+1][parent.y+1].colour!=white and squares[parent.x+1][parent.y+1].colour!=red:
            if c<squares[parent.x+1][parent.y+1].gcost+squares[parent.x+1][parent.y+1].hcost or squares[parent.x+1][parent.y+1].gcost+squares[parent.x+1][parent.y+1].hcost==0:
                squares[parent.x+1][parent.y+1].producer=[i,j]
                squares[parent.x+1][parent.y+1].colour=green
                squares[parent.x+1][parent.y+1].gcost=parent.gcost+1
                squares[parent.x+1][parent.y+1].hcost=dist(squares[parent.x+1][parent.y+1], end)
    if i+1<=grid[0]-1 and j-1<=grid[1]-1 and j-1>=0:
        if squares[parent.x+1][parent.y-1].colour!=white and squares[parent.x+1][parent.y-1].colour!=red:
            if c<squares[parent.x+1][parent.y-1].gcost+squares[parent.x+1][parent.y-1].hcost or squares[parent.x+1][parent.y-1].gcost+squares[parent.x+1][parent.y-1].hcost==0:
                squares[parent.x+1][parent.y-1].producer=[i,j]
                squares[parent.x+1][parent.y-1].colour=green
                squares[parent.x+1][parent.y-1].gcost=parent.gcost+1
                squares[parent.x+1][parent.y-1].hcost=dist(squares[parent.x+1][parent.y-1], end)
    if i-1<=grid[0]-1 and j-1<=grid[1]-1 and i-1>=0 and j-1>=0:
        if squares[parent.x-1][parent.y-1].colour!=white and squares[parent.x-1][parent.y-1].colour!=red:
            if c<squares[parent.x-1][parent.y-1].gcost+squares[parent.x-1][parent.y-1].hcost or squares[parent.x-1][parent.y-1].gcost+squares[parent.x-1][parent.y-1].hcost==0:
                squares[parent.x-1][parent.y-1].producer=[i,j]
                squares[parent.x-1][parent.y-1].colour=green
                squares[parent.x-1][parent.y-1].gcost=parent.gcost+1
                squares[parent.x-1][parent.y-1].hcost=dist(squares[parent.x-1][parent.y-1], end)
    return squares
        
def minima(squares, end, gen):
    '''This function finds the square with the minimum cost for a given iteration of the program'''
    finish=False
    coordinates=[]
    mini=100000
    for i in range(len(squares)):
        for j in range(len(squares[0])):
            if squares[i][j].gcost+squares[i][j].hcost>0 and squares[i][j].gcost+squares[i][j].hcost<mini:
                if squares[i][j].colour!=red:
                    mini=squares[i][j].gcost+squares[i][j].hcost
                    coordinates.append([i,j])
    if len(coordinates)==0 and gen !=0: #caught in a box for example:
        return squares, [0,0], True
    minimal=squares[coordinates[0][0]][coordinates[0][1]].hcost #when there are multiple squares with same lowerst cost, then the square with lowest hcost wins
    index=[coordinates[0][0], coordinates[0][1]]
    for a in coordinates:
       if squares[a[0]][a[1]].hcost<minimal:
            minimal=squares[a[0]][a[1]].hcost
            index=[a[0],a[1]]
    squares[index[0]][index[1]].colour=red #the minima for a genration that will get fed into new cost function
    if index==end:
        finish=True
    return squares, index, finish

def display_screen():
    pygame.init()
    screen=pygame.display.set_mode((grid[0]*pixel,grid[1]*pixel))
    screen.fill(pygame.Color('black'))
    clock=pygame.time.Clock()
    
    return screen, clock

def draw(screen, squares):
    for i in range(grid[0]):
        for j in range(grid[1]):
            pygame.draw.rect(screen, squares[i][j].colour, (i*pixel, j*pixel, pixel, pixel))
    
def traceback(end, squares, start):
    '''This function calculates the path taken to get to the end node by 
    looking at the parents of each node until we get back to the start node.
    Note that the parent of a square is a neighbouring square which the program
    finds to give the lowest cost.'''
    loop=True
    path=[]
    par=end
    print('par: ', par)
    while loop:
        ob=squares[par[0]][par[1]]
        path.append(par)
        par=ob.producer
        if par==start or par==[]:
            loop=False
    return path
        
        
    
def draw_final(squares, screen, path):
    for i in path:
        pygame.draw.rect(screen, cyan, (i[0]*pixel, i[1]*pixel, pixel, pixel))
    pygame.draw.rect(screen, blue, (path[len(path)-1][0]*pixel, path[len(path)-1][1]*pixel, pixel, pixel))
    pygame.draw.rect(screen, blue, (path[0][0]*pixel, path[0][1]*pixel, pixel, pixel))
            
    
def main():
    gen=0
    screen, clock=display_screen()
    pygame.display.set_caption('A* pathfinding visualiser')
    squares, node1x, node1y, node2x, node2y=Make_grid(grid)
    end=[node2x, node2y]
    start=[node1x, node1y]
    #print('end: ', end)
    draw(screen, squares)
    squares=cost( end, squares, node1x, node1y)
    squares, index, finish=minima(squares, end, gen)
    pygame.display.update()
    time.sleep(1)
    run=True
    while run:
        
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
        while finish==False:
            gen+=1
            squares=cost( end, squares, index[0], index[1])
            squares, index, finish=minima(squares, end, gen)
            draw(screen, squares)
            
            pygame.display.update()
            if finish:
                path=traceback(end, squares, start)
                draw_final(squares, screen, path)
                pygame.display.update()
            pygame.display.set_caption('A* pathfinding visualiser |Generation: {0}'.format(gen))

main()
    

                
    
    
    
    
    
    
    
    
    
    
    
