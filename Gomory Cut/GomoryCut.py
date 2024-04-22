from Simplex import simplex_two_phase as simplex
import numpy as np
import math
from fractions import  Fraction
def isInteger(fraction):
    if fraction.denominator == 1:
        return True
    else:
        return False

def gomoryCut(A, b, c):

    table = simplex.solveLP(A, b, c)

    while True:
        A_new, b_new = [], 0
        cut = 1
        for i in range(len(table)):
            if not isInteger(Fraction(table[i][2]).limit_denominator(100)):
                cut = 0
                for j in range(len(table[0]) - 3):
                    A_new.append(table[i][j + 3] - math.floor(table[i][j + 3]))
                b_new = table[i][2] - math.floor(table[i][2])
                print("Gomory cut: x{}".format(int(table[i][0])), end='\n\n')
                break

        if cut == 1:
            print("Tất cả nghiệm đều nguyên")
            return table

        A_new.append(-1)

        A = np.hstack((A, np.zeros((len(A), 1))))
        A = np.vstack((A, A_new))
        b = np.hstack((b, b_new))
        c = np.hstack((c, [0]))

        table = simplex.solveLP(A, b, c)

def input():
    f = open("test2.txt", 'r')
    nConstraint = int(f.readline())
    c = [float(ci) for ci in f.readline().split()]
    A = []
    for i in range(nConstraint):
        A.append([float(Aij) for Aij in f.readline().split()])
    b = [float(bi) for bi in f.readline().split()]
    return np.asarray(A), np.asarray(b), np.asarray(c)

def print_solve(table, n):
    obj = np.sum(table[:, 1] * table[:, 2])
    print("Objective = ", Fraction(obj).limit_denominator(100), end='\n\n')
    result = np.zeros((len(table[0]) - 3))
    for i in range(len(table)):
        result[int(table[i][0])] = table[i][2]
    for i in range(n):
        print("X" + str(i), "=", Fraction(result[i]).limit_denominator(100))

def main():
    A, b, c = input()
    g_table = gomoryCut(A, b, c)
    print_solve(g_table, len(c))


if __name__ == "__main__":
    main()