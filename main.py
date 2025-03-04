import pygame
import numpy as np
from objects import Celda, Punto, Shape
import functions as f
import random

pygame.init()
screen = pygame.display.set_mode((800,600))

tablero = f.empty_list(9,9)

mouse_sprite = Punto((0,0))
shape_sprite = Shape(screen, (0,0))

for i in range(len(tablero)):
    for j in range(len(tablero[i])):
        tablero[i][j] = Celda(screen, i, j)

group_celdas = pygame.sprite.Group(tablero)


shape = 0
shape_sprite.set_shape(shape)


true = True
while true:
    screen.fill((50,50,50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            true = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_sprite.set_pos(event.pos)
            celda_click = pygame.sprite.spritecollide(mouse_sprite, group_celdas, False)
            for celda in celda_click:
                if f.fill_shape(tablero, shape, celda.row, celda.column, True):
                    shape = random.randint(0,26)
                    shape_sprite.set_shape(shape)
                    shape_sprite.set_pos(event.pos)
                f.delete_full(tablero)
        elif event.type == pygame.MOUSEMOTION:
            shape_sprite.set_pos(event.pos)
    group_celdas.update()
    shape_sprite.update() 
    pygame.display.flip()