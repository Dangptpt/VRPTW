from Utils import Utils
import matplotlib.pyplot as plt
import random
def main():
    vrptw = Utils("C206")
    initial_solution = vrptw.createFirstSolveGreedy()
    iterator = 0

    while (iterator < 1000):
        initial_solution.mutate()
        iterator += 1

    for id, vehicle in enumerate(initial_solution.vehicles):
        print("Route", end=" ")
        print(id+1, end=": ")
        for node in vehicle.nodes:
            print(node.id, end=" ")
        print()
    print("Total weight:", end = " ")
    print(initial_solution.getTotalWeight())

    plt.scatter(vrptw.rows[0].x, vrptw.rows[0].y, color='red', marker='^', s=100, label='Depot')
    for vehicle in initial_solution.vehicles:
        x_values, y_values = [], []
        for node in vehicle.nodes:
            x_values.append(node.x)
            y_values.append(node.y)
            plt.scatter(node.x, node.y, color='black', marker='o', s=20)
            if node.id != 0:
                plt.annotate(f'{node.id}', (node.x, node.y),)
        color = (random.random(), random.random(), random.random())
        plt.plot(x_values, y_values, color=color)
    plt.legend()
    plt.show()
if __name__ == "__main__" :
    main()