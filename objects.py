import pygame
import os
import parameters as p
import functions as f
size = 66

file = os.path.join("img", "Blue_square.png")

class Celda(pygame.sprite.Sprite):
    def __init__(self, screen, row, column):
        super().__init__()
        self.screen = screen
        self.row = row
        self.column = column
        self.rect = (column*size, row*size, size, size)
        self.image = pygame.image.load(file).convert_alpha()
        self.filled = False

    def update(self):
        if self.filled:
            self.image.fill((50,50,200))
            self.screen.blit(self.image, self.rect)
        else:
            self.image.fill((100,100,100 ))
            self.screen.blit(self.image, self.rect)

class Punto(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(pygame.sprite.Sprite, self).__init__()
        self.rect = pygame.Rect(pos[0], pos[1], 1, 1)
    
    def set_pos(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 1, 1)

class Shape(pygame.sprite.Sprite):
    def __init__(self, screen, pos):
        super(pygame.sprite.Sprite, self).__init__()
        self.screen = screen
        self.image = pygame.image.load(file).convert_alpha()
        self.pos = pos
        self.subshapes = []
        self.shape = 0
    
    def set_pos(self, pos):
        self.pos = pos
        self.subshapes = []
        for elem in p.shape_dict[self.shape]:
            x = self.pos[0]-30 + 66*elem[1]
            y = self.pos[1]-30 + 66*elem[0]
            self.subshapes.append(pygame.Rect(x, y, 60, 60))
    
    def set_shape(self, shape):
        self.shape = shape
    
    def update(self):
        for shape in self.subshapes:
            self.screen.blit(self.image, shape)

class Celda_2:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.filled = False

class Game:
    def __init__(self):
        self.tablero = f.empty_list(9,9)
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                self.tablero[i][j] = Celda_2(i, j)
        
        self.shape = 0
    
    def get_tablero(self):
        lista = []
        for i in self.tablero:
            l = []
            for j in i:
                l.append(j.filled)
            lista.append(l)
        return lista



