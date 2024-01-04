from ortools.linear_solver import pywraplp
def solve() :
    with open('test.txt', 'r') as file:
        data = file.readlines()
    n, v, capacity = [int(i) for i in data[0].split()]
    distance = []
    for i in range(n+1):
        distance.append([int(j) for j in data[i+2].split()])

    for i in range(n+1):
        distance[i].append(distance[i][0])
    for i in range(0, n+1):
        for j in range(0, n+2):
            if distance[i][j] == -1:
                distance[i][j] = 99999

    demand = [int(i) for i in data[n+4].split()]
    demand.insert(0, 0)
    timeOpen = [int(i) for i in data[n+6].split()]
    timeClose = [int(i) for i in data[n+7].split()]
    timeService = [int(i) for i in data[n+9].split()]
    timeService.insert(0,0)

    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return

    inf = solver.infinity()
    x, t, y = {}, {}, {}

    '''Variables'''
    for i in range(0, n+1):
        for j in range(1, n+2):
            for k in range(v):
                x[i, j, k] = solver.IntVar(0, 1, "x[{},{},{}]".format(i, j, k))

    for i in range(0, n+2):
        for k in range(v):
            t[i, k] = solver.IntVar(0, inf, "t[{},{}]".format(i, k))

    for i in range(0, n+1):
        for k in range(v):
            y[i, k] = solver.IntVar(0, capacity, "y[{}, {}]".format(i, k))

    '''Constraint 1: t0k = 0'''
    for k in range(v):
        solver.Add(t[0, k] == 0)

    '''Constraint 2: xiik = 0'''
    for i in range(1, n+1):
        for k in range(v):
            solver.Add(x[i, i, k] == 0)

    '''Constraint 3: Sum xijk = 1'''
    for i in range(1, n+1):
        solver.Add(sum(x[i, j, k] for j in range(1, n+2) for k in range(v)) == 1)

    '''Constraint 4: Sum xijk = 1'''
    # for j in range(n):
    #     solver.Add(sum(x[i, j+1, k] for i in range(n+1) for k in range(v)) == 1)

    '''Constraint 5: Sum x[0, j, k] = 1'''
    for k in range(v):
        solver.Add(sum(x[0, j, k] for j in range(1, n+2)) == 1)

    '''Constraint 6: Sum x[i, n+1, k] = 1'''
    for k in range(v):
        solver.Add(sum(x[i, n+1, k] for i in range(n+1)) == 1)

    '''Constraint 7: xajk = xiak'''
    for a in range(1, n+1):
        for k in range(v):
            solver.Add(sum(x[i, a, k] for i in range(n+1)) == sum(x[a, j, k] for j in range(1, n+2)))

    '''Constraint 8: Sum demand < q'''
    # for k in range(v):
    #     solver.Add(sum(demand[i] * x[i, j, k] for i in range(1, n+1) for j in range(1, n+2)) <= capacity)

    '''Constraint 9: time service '''
    for i in range(0, n+1):
        for j in range(1, n+2):
            for k in range(v):
                solver.Add((t[i, k] + distance[i][j] + timeService[i] - t[j, k] - (1-x[i, j, k])*inf) <= 0)

    '''Constraint 10: time window'''
    for i in range(n):
        for k in range(v):
            solver.Add(timeOpen[i] - t[i+1, k] <= 0)

    '''Constraint 11: time window'''
    for i in range(n):
        for k in range(v):
            solver.Add(timeClose[i] - t[i+1, k] >= 0)

    '''Constraint 12: load in truck after serving'''
    for i in range(1, n+1):
        for j in range(1, n+1):
            for k in range(v):
                if i == j:
                    continue
                solver.Add(y[j, k] <= y[i, k] - demand[j] * x[i, j, k] + capacity * (1 - x[i, j, k]))


    objective = []
    for i in range(0, n+1):
        for j in range(1, n+2):
            for k in range(v):
                objective.append(distance[i][j] * x[i, j, k])

    solver.Minimize(sum(objective))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("Objective value =", solver.Objective().Value())
        for i in range(n + 1):
            for j in range(n + 1):
                for k in range(v):
                    print(x[i, j + 1, k].name(), x[i, j + 1, k].solution_value(), end=" ")
                print()
    else:
        print("The problem does not have an optimal solution.")

    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    #print(f"Problem solved in {solver.nodes():d} branch-and-bound nodes")

    return

def output():
    pass
def main() :
    solve()
    output()

if __name__ == "__main__" :
    main()