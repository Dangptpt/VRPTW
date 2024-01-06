import numpy as np
from fractions import Fraction
def initTable(A_sub, b, c_sub):
    size = list(A_sub.shape)
    cb = np.array(c_sub[size[1] - size[0]])
    B = np.array([size[1] - size[0]])

    for i in range(size[1] - size[0] + 1, size[1]):
        cb = np.vstack((cb, c_sub[i]))
        B = np.vstack((B, i))
        xb = np.transpose([b])

    table = np.hstack((B, cb))
    table = np.hstack((table, xb))
    table = np.hstack((table, A_sub))
    table = np.array(table, dtype='float')

    return table

# Thuật toán đơn hình
def simplex(table, c):
    itr = 0
    while 1:
        # In bảng đơn hình
        print()
        print("Iteration:", itr)
        for row in table:
            for el in row:
                print(Fraction(str(el)).limit_denominator(100), end='\t')
            print()
        profits = []
        # Tính các ước lượng delta k
        for i in range(len(table[0]) - 3):
            profits.append(np.sum(table[:, 1] * table[:, 3 + i]) - c[i])

        print("Delta k: ", end=" ")
        for profit in profits:
            print(Fraction(str(profit)).limit_denominator(100), end=", ")
        print(end='\n\n')

        # Kiểm tra điều kiện tối ưu
        flag = 0
        for profit in profits:
            if profit > 0:
                flag = 1
                break
        if flag == 0:
            print("All profits are <= 0, optimality reached")
            break

        # Tìm vector Ak để đưa vào cơ sở mới
        k = profits.index(max(profits))
        min_value = 9999999
        r = -1
        # Tìm vector Ar để đưa ra cơ sở cũ
        for i in range(len(table)):
            if table[:, 3 + k][i] > 0:
                val = table[:, 2][i] / table[:, 3 + k][i]
                if val < min_value:
                    min_value = val
                    r = i
        # Kiểm tra bài toán không có lời giải
        if r == -1:
            print("Min value is -inf")
            break

        # Phần tử chính
        print("pivot index:", np.array([r, 3 + k]))
        pivot = table[r][3 + k]
        print("pivot value:", Fraction(pivot).limit_denominator(100))

        # Dòng chính = Dòng quay / phần tử chính
        table[r, 2:len(table[0])] = table[r, 2:len(table[0])] / pivot

        # Dòng mới = Dòng cũ tương ứng - (phần tử quay tương ứng) * (dòng chính)
        for i in range(len(table)):
            if i != r:
                table[i, 2:len(table[0])] = table[i, 2:len(table[0])] - table[i][3 + k] * table[r, 2:len(table[0])]

        table[r][0] = k
        table[r][1] = c[k]
        itr += 1

# Đẩy hết vector giả khỏi cơ sở
def fix_degenerate_basis(table, r, k):
    pivot = table[r][k]
    print(pivot)
    # Dòng chính = Dòng quay / phần tử chính
    table[r, 2:len(table[0])] = table[r, 2:len(table[0])] / pivot

    # Dòng mới = Dòng cũ tương ứng - (phần tử quay tương ứng) * (dòng chính)
    for i in range(len(table)):
        print(i)
        if i != r:
            table[i, 2:len(table[0])] = table[i, 2:len(table[0])] - table[i][k] * table[r, 2:len(table[0])]
    table[r][0] = k-3
    table[r][1] = 0
    print (table)

def phase1(table, c_sub):
    print("Phase 1:")
    simplex(table, c_sub)
    i = 0
    while i < len(table):
        if int(table[i][0]) >= (len(table[0]) - 3 - len(table)):
            if int(table[i][2]) != 0:
                print("khong co nghiem co so chap nhan duoc")
                exit()
            else:
                for j in range(3, len(table[0])):
                    if abs(table[i][j]) > 1e-5:
                        r = i
                        k = j
                        break
                fix_degenerate_basis(table, r, k)
                i -= 1
        i += 1
    new_table = table

    for i in range(len(table)):
        a = len(new_table[0]) - 1
        new_table = np.delete(new_table, a, axis=1)

    return new_table

def phase2(table, c):
    print()
    print("Phase 2:")
    for i in range(len(table)):
        if int(table[i][0]) <= len(table[0]) - 3:
            table[i][1] = c[int(table[i][0])]
    simplex(table, c)
    return table

# Thiết lập hàm mục tiêu cho bài toán phase 1:
def prepare_objective_phase1(A, c):
    A_sub = np.hstack((A, np.eye(len(A))))
    c_sub = np.zeros((len(c) + len(A)))
    for i in range(len(c), len(c) + len(A)):
        c_sub[i] = 1

    return A_sub, c_sub

def print_solve(table):
    obj = np.sum(table[:, 1] * table[:, 2])
    print("Objective = ", Fraction(obj).limit_denominator(100), end='\n\n')
    result = np.zeros((len(table[0])-3))
    for i in range(len(table)):
        result[int(table[i][0])] = table[i][2]
    for i in range(len(result)):
        print("X" + str(i), "=", Fraction(result[i]).limit_denominator(100))

def input():
    f = open("simplextest2.txt", 'r')
    nConstraint = int(f.readline())
    c = [float(ci) for ci in f.readline().split()]
    A = []
    for i in range(nConstraint):
        A.append([float(Aij) for Aij in f.readline().split()])
    b = [float(bi) for bi in f.readline().split()]
    return np.asarray(A), np.asarray(b), np.asarray(c)

def solveLP(A, b, c):
    A_sub, c_sub = prepare_objective_phase1(A, c)

    # Khởi tạo bảng đơn hình
    table = initTable(A_sub, b, c_sub)

    # Pha 1: Tìm phương án cực biên
    table = phase1(table, c_sub)

    # Pha 2: Tìm phương án tối ưu
    table = phase2(table, c)

    print_solve(table)
    return table

def main():
    A, b, c = input()
    solveLP(A, b, c)

if __name__ == "__main__":
    main()
