from ortools.linear_solver import pywraplp

def identity(numRows, numCols, val=1, rowStart=0):
   return [[(val if i == j else 0) for j in range(numCols)]
               for i in range(rowStart, numRows)]
def standardForm(cost, greaterThans=[], gtThreshold=[], lessThans=[], ltThreshold=[],
                equalities=[], eqThreshold=[], maximization=True):
   newVars = 0
   numRows = 0
   if gtThreshold != []:
      newVars += len(gtThreshold)
      numRows += len(gtThreshold)
   if ltThreshold != []:
      newVars += len(ltThreshold)
      numRows += len(ltThreshold)
   if eqThreshold != []:
      numRows += len(eqThreshold)

   if not maximization:
      cost = [-x for x in cost]

   if newVars == 0:
      return cost, equalities, eqThreshold

   newCost = list(cost) + [0] * newVars

   constraints = []
   threshold = []

   oldConstraints = [(greaterThans, gtThreshold, -1), (lessThans, ltThreshold, 1),
                     (equalities, eqThreshold, 0)]

   offset = 0
   for constraintList, oldThreshold, coefficient in oldConstraints:
      constraints += [c + r for c, r in zip(constraintList,
         identity(numRows, newVars, coefficient, offset))]

      threshold += oldThreshold
      offset += len(oldThreshold)

   return newCost, constraints, threshold

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