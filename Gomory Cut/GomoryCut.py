from Simplex import simplex_two_phase as simplex
import numpy as np
import math
from fractions import  Fraction
def isInteger(fraction):
    if fraction.denominator == 1:
        return True
    else:
        return False

def init_constraint(table):
    constraint = []
    cut = 1
    for i in range(len(table)):
        if not isInteger(Fraction(table[i][2]).limit_denominator(100)):
            cut = 0
            for j in range(len(table[0])-3):
                constraint.append(table[i][j+3] - math.floor(table[i][j+3]))
                b = table[i][2] - math.floor(table[i][2])
            print("Gomory cut:", end='\n\n')
            break

    constraint.append(-1)
    if cut == 1:
        print("Tất cả nghiệm đều nguyên")
        exit()
    return constraint, b
def gomory_cut(table):
     pass
def input():
    f = open("../Simplex/simplextest1.txt", 'r')
    nConstraint = int(f.readline())
    c = [float(ci) for ci in f.readline().split()]
    A = []
    for i in range(nConstraint):
        A.append([float(Aij) for Aij in f.readline().split()])
    b = [float(bi) for bi in f.readline().split()]
    return np.asarray(A), np.asarray(b), np.asarray(c)

def main():
    A, b, c = input()
    table = simplex.solveLP(A, b, c)
    A_new, b_new = init_constraint(table)
    A = np.hstack((A, np.zeros((len(A), 1))))
    A = np.vstack((A, A_new))
    b = np.hstack((b, b_new))
    c = np.hstack((c, [0]))
    print (A, b, c)
    g_table = simplex.solveLP(A, b, c)

if __name__ == "__main__":
    main()