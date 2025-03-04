import numpy as np
import parameters as p

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

def check_list(list):
    full = True
    for elem in list:
        if not elem.filled:
            full = False
    return full