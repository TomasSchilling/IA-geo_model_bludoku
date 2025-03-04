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

def check_list(list):
    full = True
    for elem in list:
        if not elem:
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
        squares.append([check_list(cels), cels])
    
    points = 0
    for column in columns:
        if column[0]:
            for i in column[1]:
                points += 1
                i = False
    for row in rows:
        if row[0]:
            for i in row[1]:
                points += 1
                i = False
    for square in squares:
        if square[0]:
            for i in square[1]:
                points += 1
                i = False
    
    return points

class Game:
    def __init__(self):
        self.tablero = empty_list(9,9, fill = False)
        self.up2date = True
        self.score = 0
        self.shape = 0#random.randint(0,26)
        self.plays, self.live= self.get_plays()
    
    def get_tablero(self):
        return self.tablero

    def get_plays(self):
        any_play = False  ## ¿any play left?
        lista = []
        for i in range(9):
            l = []
            for j in range(9):
                l.append(self.fill_shape(i,j,False))
            if True in l:
                any_play = True
            lista.append(l)
        return lista, any_play
    
    def fill_shape(self, row, column, fill):
        able = True
        for elem in p.shape_dict[self.shape]:
            r = row + elem[0]
            c = column + elem[1]
            if r >= 0 and r <= 8 and c >= 0 and c <= 8:   ## check celda inside the map
                if self.tablero[r][c]:
                    able = False
            else:
                able = False
        
        if able:
            if not fill: ## only check for able
                return True
            for elem in p.shape_dict[self.shape]:
                self.tablero[row + elem[0]][column + elem[1]] = True
            return True
        return False

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
        row = number//9
        column = number-row*9
        return row, column
    
    def rc2number(self, row, column):
        number = 9*row+column
        return number

    def play_number(self, number):
        if not self.up2date:
            self.plays, self.live = self.get_plays()
            self.up2date = True
        row, column = self.number2rc(number)

        if self.plays[row][column]:
            self.fill_shape(row, column, True)
            self.score += delete_full(self.tablero)
            self.shape = 0#random.randint(0,26)
            self.up2date = False
            self.plays, self.live = self.get_plays()
            if not self.live:
                return self.score  ## end of the game
            else:
                self.score+=1
                return True       ## correctly filled number
        else:
            self.score-=1
            return self.score     ## cannont fill that number
        
    def join_input(self):
        flat_list1 = [item for sublist in self.get_shape() for item in sublist]
        flat_list2 = [item for sublist in self.get_tablero() for item in sublist]
        self.joined_list = flat_list1 + flat_list2
        return self.joined_list
    
    def reset_game(self):
        self.__init__()

            

j = Game()

for i in range(9):
    j.play_number(i)

print(j.get_shape())
print(j.get_tablero())
print(j.get_plays())


