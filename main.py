###########################
## Conway's Game of Life ##
###########################
import sys
import pygame
import scipy
from scipy.signal import convolve2d
import numpy as np
import random as r
import math as m
FPS=10
FR_TIME_MS=1000/FPS
CELL_W=10
CELL_H=10
SCREEN_DIM=(800,600)
GRID=np.zeros(shape=(SCREEN_DIM[0]//CELL_W,SCREEN_DIM[1]//CELL_H),dtype='uint8')
# Init
C_GREEN=(0,255,0)
C_BLACK=(0,0,0)
# Pygame
pygame.init()
WINDOW=pygame.display.set_mode(SCREEN_DIM)
WINDOW.fill((255,255,255))
# Patterns
def gen_blinker(x,y):
    GRID[y][x]=1
    GRID[y+1][x]=1
    GRID[y+2][x]=1
def gen_glider(x,y):
    GRID[y][x+1]=1
    GRID[y+1][x+2]=1
    GRID[y+2][x]=1
    GRID[y+2][x+1]=1
    GRID[y+2][x+2]=1
def gen_toad(x,y):
    GRID[y][x+1]=1
    GRID[y][x+2]=1
    GRID[y][x+3]=1
    GRID[y+1][x]=1
    GRID[y+1][x+1]=1
    GRID[y+1][x+2]=1
def gen_r_pentomino(x,y):
    GRID[y][x+1]=1
    GRID[y][x+2]=1
    GRID[y+1][x]=1
    GRID[y+1][x+1]=1
    GRID[y+2][x+1]=1
# Game state
def init_grid():
    for ii in range(0,12):
        rx=r.randint(0,GRID.shape[1]-5)
        ry=r.randint(0,GRID.shape[0]-5)
        match ii%4:
            case 0:
                gen_toad(rx,ry)
            case 1:
                gen_blinker(rx,ry)
            case 2:
                gen_glider(rx,ry)
            case 3:
                gen_r_pentomino(rx,ry)
def update_grid():
    global GRID
    # Compute 3x3 Adj cells - cur
    adj_count_m=(convolve2d(GRID,np.ones((3,3)), mode='same', boundary='wrap') - GRID).astype('uint8')
    # Game of Life Rules:
    # Cell is alive (1) if it has 3 adjacent neighbors, or is currently live and has exactly 2.
    GRID=(adj_count_m == 3) | (GRID & (adj_count_m == 2))
# Draw
def render_grid():
    for ii in range(GRID.shape[0]): # Row
        for jj in range(GRID.shape[1]): # Col
            c=C_GREEN if GRID[ii][jj] else C_BLACK
            pygame.draw.rect(WINDOW,c,[ii*CELL_W,jj*CELL_H,CELL_W,CELL_H],0)
# Core loop
# Init
init_grid()
prev_frame=0
acc=0
while 1:
    t=pygame.time.get_ticks()
    dt=(t-prev_frame)
    prev_frame=t
    acc += dt
    if acc < FR_TIME_MS: # Update every FR_TIME_MS*1000 fps
        continue
    acc=0
    render_grid()
    pygame.display.update()
    update_grid()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit(0)

