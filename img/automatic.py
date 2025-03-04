import parameters as p
import numpy as np
import random

def empty_list(rows, columns, fill = 0):
    lista = []
    for i in range(columns):
        lista.append([])
        for j in range(rows):
            lista[i].append(fill)
    
    return lista

def fill_shape(lista, shape, row, column, fill):
    able = True
    for elem in p.shape_dict[shape]:
        r = row + elem[0]
        c = column + elem[1]
        if r >= 0 and r <= 8 and c >= 0 and c <= 8:   ## check celda inside the map
            if lista[row + elem[0]][column + elem[1]].filled:
                able = False
        else:
            able = False
    
    if able:
        if not fill: ## only check for able
            return True
        for elem in p.shape_dict[shape]:
            lista[row + elem[0]][column + elem[1]].filled = True
        return True
    return False


def check_list(list):
    full = True
    for elem in list:
        if not elem.filled:
            full = False
    return full

def delete_full(lista):
    rows = []
    for row in lista:
        rows.append([check_list(row), row])
    tr_lista = np.transpose(lista)
    columns = []
    for column in tr_lista:
        columns.append([check_list(column), column])
    squares = []
    for square in range(9):
        cels = []
        n1 = square//3
        n2 = square%3
        for i in range(3):
            for j in range(3):
                cels.append(lista[n1*3+i][n2*3+j])
        squares.append([check_list(cels), cels.copy()])
    
    points = 0
    for column in columns:
        if column[0]:
            for i in column[1]:
                if i.filled:
                    points += 1
                i.filled = False
    for row in rows:
        if row[0]:
            for i in row[1]:
                if i.filled:
                    points += 1
                i.filled = False
    for square in squares:
        if square[0]:
            for i in square[1]:
                if i.filled:
                    points += 1
                i.filled = False
    
    return points

class Celda:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.filled = False

class Game:
    def __init__(self):
        self.tablero = empty_list(9,9)
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                self.tablero[i][j] = Celda(i, j)
        
        self.up2date = True
        self.score = 0
        self.shape = random.randint(0,26)
        self.plays, self.dead= self.get_plays()
    
    def get_tablero(self):
        lista = []
        for i in self.tablero:
            l = []
            for j in i:
                l.append(j.filled)
            lista.append(l)
        return lista

    def get_plays(self):
        any_play = False  ## ¿any play left?
        lista = []
        for i in range(9):
            l = []
            for j in range(9):
                l.append(fill_shape(self.tablero, self.shape, i,j,False))
            if True in l:
                any_play = True
            lista.append(l)
        return lista, any_play
    
    def get_shape(self):
        lista = [[False],[False,False,False],[False,False,False,False,False],[False,False,False],[False]]
        shape = p.shape_dict[self.shape]
        if (-2,0) in shape:
            lista[0][0] = True
        if (-1,-1) in shape:
            lista[1][0] = True
        if (-1,0) in shape:
            lista[1][1] = True
        if (-1,1) in shape:
            lista[1][2] = True
        if (0,-2) in shape:
            lista[2][0] = True
        if (0,-1) in shape:
            lista[2][1] = True
        if (0,0) in shape:
            lista[2][2] = True
        if (0,1) in shape:
            lista[2][3] = True
        if (0,2) in shape:
            lista[2][4] = True
        if (1,-1) in shape:
            lista[3][0] = True
        if (1,0) in shape:
            lista[3][1] = True
        if (1,1) in shape:
            lista[3][2] = True
        if (2,0) in shape:
            lista[4][0] = True
        return lista
    
    def number2rc(self, number):
        row = number%9
        column = number-row*9
        return row, column
    
    def rc2number(self, row, column):
        number = 9*row+column
        return number

    def play_number(self, number):
        if not self.up2date:
            self.plays, self.dead = self.get_plays()
            self.up2date = True
        row, column = self.number2rc(number)

        if self.plays[row][column]:
            fill_shape(self.tablero, self.shape, row, column, True)
            delete_full(self.tablero)
            self.shape = random.randint(0,26)
            self.up2date = False
            self.plays, self.dead = self.get_plays()
            if self.dead:
                return self.score  ## end of the game
            else:
                return True       ## correctly filled number
        else:
            return False          ## cannont fill that number

            

j = Game()
fill_shape(j.tablero, j.shape ,0,0,True)


print(j.get_shape())