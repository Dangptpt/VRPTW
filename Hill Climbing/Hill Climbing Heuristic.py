from Utils import Utils
import matplotlib.pyplot as plt
import random
import os

def prepareResult():
    for file in os.listdir("D:\Hust Study\Project\Project 1\Project\VRPTW\Instances\Data"):
        vrptw = Utils(file)
        initial_solution = vrptw.createFirstSolveGreedy()
        iterator = 0
        while (iterator < 1000):
            initial_solution.move(vrptw.rows[0], vrptw.number_vehicles, vrptw.capacity)
            initial_solution.exchangeInRoute()
            initial_solution.relocate()
            initial_solution.exchangeCross()
            iterator += 1

        with open(f'../Instances/Result/{file}') as txt:
            data = txt.readline()
        current_weight = float(data.split()[2])
        if current_weight <= initial_solution.getTotalWeight():
            continue

        f = open(f'../Instances/Result/{file}', 'w')

        f.write("Total weight: ")
        f.write(f'{initial_solution.getTotalWeight()}')
        f.write('\n')
        for id, vehicle in enumerate(initial_solution.vehicles):
            f.write("Route ")
            f.write(f'{id + 1}: ')
            for node in vehicle.nodes:
                f.write(f'{node.id}')
                f.write(" ")
            f.write('\n')


def show(file):
    result = ''
    with open(f'../Instances/Result/{file}') as txt:
        result = txt.readlines()
    vrptw = Utils(file)

    routes = []
    for i, line in enumerate(result):
        if i > 0:
            nodes = result[i].split()
            tmp = []
            for j, node in enumerate(nodes):
                if j > 1:
                    tmp.append(int(node))
            routes.append(tmp)
    plt.scatter(vrptw.rows[0].x, vrptw.rows[0].y, color='red', marker='^', s=100, label='Depot')
    for i, vehicle in enumerate(routes):
        x_values, y_values = [], []
        for node in vehicle:
            x_values.append(vrptw.rows[node].x)
            y_values.append(vrptw.rows[node].y)
            plt.scatter(vrptw.rows[node].x, vrptw.rows[node].y, color='black', marker='o', s=20)
            if vrptw.rows[node].id != 0:
                plt.annotate(f'{vrptw.rows[node].id}', (vrptw.rows[node].x, vrptw.rows[node].y), )
        color = (random.random(), random.random(), random.random())
        plt.plot(x_values, y_values, color=color)
    plt.legend()
    plt.show()

def main():
    #prepareResult()
    show("C101.txt")

if __name__ == "__main__" :
    main()