# A package to visualize your matrices easily. Just pass in the matrix (2-D array) to have it visualized for bette understanding of
# the data you are working with.

import random

def visualize(matrix):
    nrow = len(matrix)
    print("----- "*len(matrix[0]))
    for i in range(0, nrow):
        ncol = len(matrix[i])
        for j in range(0, ncol):
            if(j==ncol-1):
                print("| ", matrix[i][j], " |", end="\n")
            else:
                print("| ", matrix[i][j], end=" ")
        print("----- "*ncol)


# def randomMatrix():
#     nrow = random.randint(1, 10)
#     ncol = random.randint(1, 10)
#     matrix = [[0 for i in range(ncol)] for j in range(nrow)]
#     for i in range(0, nrow):
#         for j in range(0, ncol):
#             matrix[i][j] = random.randint(-127, 128)
#     visualize(matrix)
#     return matrix

# def randomMatrixDim(nrow, ncol):
#     matrix = [[0 for i in range(ncol)] for j in range(nrow)]
#     for i in range(0, nrow):
#         for j in range(0, ncol):
#             matrix[i][j] = random.randint(-127, 128)
#     visualize(matrix)
#     return matrix

def randomMatrix(nrow = None, ncol = None):
    if(nrow == None and ncol == None):
        nrow = random.randint(1, 10)
        ncol = random.randint(1, 10)
        matrix = [[0 for i in range(ncol)] for j in range(nrow)]
        for i in range(0, nrow):
            for j in range(0, ncol):
                matrix[i][j] = random.randint(-127, 128)
        visualize(matrix)
        return matrix
    elif(nrow!=None and ncol!=None):
        matrix = [[0 for i in range(ncol)] for j in range(nrow)]
        for i in range(0, nrow):
            for j in range(0, ncol):
                matrix[i][j] = random.randint(-127, 128)
        visualize(matrix)
        return matrix
    elif(nrow==None or ncol==None):
        print("Please provide both dimensions!")

def zeroElements(matrix):
    zeroCounter = 0
    nrow = len(matrix)
    for i in range(0, nrow):
        ncol = len(matrix[i])
        for j in range(0, ncol):
            if matrix[i][j]==0:
                zeroCounter+=1
    return zeroCounter

def matSum(matrix):
    sumOfMat = 0
    nrow = len(matrix)
    for i in range(0, nrow):
        ncol = len(matrix[i])
        for j in range(0, ncol):
            sumOfMat += matrix[i][j]
    return sumOfMat

def evenCheck(matrix): # returns a tuple with first value being number of even elements and second value being number of odd elements
    evenCounter = 0
    oddCounter = 0
    nrow = len(matrix)
    for i in range(0, nrow):
        ncol = len(matrix[i])
        for j in range(0, ncol):
            if matrix[i][j]%2==0:
                evenCounter+=1
            else:
                oddCounter+=1
    return evenCounter, oddCounter

def transpose(matrix):
    nrow = len(matrix)
    ncol = len(matrix[0])
    transposeMat = [[0 for i in range(nrow)] for j in range(ncol)]
    for i in range(0, ncol):
        for j in range(0, nrow):
            transposeMat[i][j] = matrix[j][i]
    visualize(transposeMat)
    return transposeMat

def dim(matrix):
    nrow = len(matrix)
    ncol = len(matrix[0])
    return nrow, ncol

def matAdd(matrix1, matrix2):
    nrow1 = len(matrix1)
    ncol1 = len(matrix1[0])
    nrow2 = len(matrix2)
    ncol2 = len(matrix2[0])
    if(nrow1 == nrow2 and ncol1 == ncol2):
        matrix3 = [[0 for i in range(ncol1)] for j in range(nrow1)]
        for i in range(0, nrow1):
            for j in range(0, ncol1):
                matrix3[i][j] = matrix1[i][j] + matrix2[i][j]
        visualize(matrix3)
        return matrix3
    else:
        print("Incompatible Matrices!")

def matMul(matrix1, matrix2):
    nrow1 = len(matrix1)
    ncol1 = len(matrix1[0])
    nrow2 = len(matrix2)
    ncol2 = len(matrix2[0])
    if(ncol1 == nrow2):
        matrix3 = [[0 for i in range(ncol2)] for j in range(nrow1)]
        for i in range(nrow1):
            for j in range(ncol2):
                for k in range(nrow2):
                    matrix3[i][j] += matrix1[i][k] * matrix2[k][j]
        visualize(matrix3)
        return matrix3
    else:
        print("Incompatible Matrices!")

def scalarMul(matrix, c):
    nrow1 = len(matrix)
    ncol1 = len(matrix[0])
    for i in range(nrow1):
            for j in range(ncol1):
                matrix[i][j] *= c
    visualize(matrix)
    return matrix