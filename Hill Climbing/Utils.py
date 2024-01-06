from Point import Point
from Solution import Solution
from Vehicle import Vehicle
from Candidate import Candidate
import math
import matplotlib.pyplot as plt
class Utils:
    def __init__(self, test):
        self.test = test
        data = ""
        with open(f'../Instances/Data/{test}'.format(test)) as file:
            data = file.readlines()
        number_vehicles, capacity = [int(i) for i in data[4].split()]
        rows = []
        for i in range(9, len(data)):
            id, x, y, demand, ready_time, due_date, service_time = [int(j) for j in data[i].split()]
            p = Point(id, x, y, demand, ready_time, due_date, service_time)
            rows.append(p)
        self.number_vehicles = number_vehicles
        self.capacity = capacity
        self.rows = rows

    # khoi tao loi gian ban dau
    def createFirstSolveGreedy(self):
        list_customer = []
        depot = self.rows[0]
        degree_depot = math.atan2(depot.y, depot.x)
        for i in range(1, len(self.rows)):
            customer = self.rows[i]
            newDegree = math.atan2(customer.y, customer.x)
            d1 = math.sqrt(customer.x**2 + customer.y**2)
            d = depot.distance(customer)
            r = d1*math.sin(newDegree-degree_depot)/d
            if (math.fabs(r)-1 <= 1e-7):
                r = 1
            alpha = math.asin(r) * 180 / math.pi
            if customer.x * depot.x + customer.y * depot.y - depot.x ** 2 - depot.y ** 2 > 0:
                if alpha < 0:
                    alpha = -(180 + alpha)
                else:
                    alpha = 180 - alpha
            if alpha < 0:
                w = alpha - 0.5 * d - 0.1 * customer.due_date
            else:
                w = alpha + 0.5 * d + 0.1 * customer.due_date

            list_customer.append({'weight': w, 'point': customer})

        list_customer.sort(key=lambda x : x['weight'])

        # x_values, y_values = [], []
        # for i, customer in enumerate(list_customer):
        #     w = customer['weight']
        #     x_values.append(customer['point'].x)
        #     y_values.append(customer['point'].y)
        #     plt.scatter(customer['point'].x, customer['point'].y, color='black', marker='o', s=20)
        #     plt.annotate(f'{w}', (customer['point'].x, customer['point'].y),)
        # plt.scatter(self.rows[0].x, self.rows[0].y, color='red', marker='^', s=100, label='Depot')
        # plt.show()

        new_route = [depot, depot]
        vehicle = Vehicle(0, new_route, self.capacity)

        list_vehicle = [vehicle]
        solution = Solution(list_vehicle)

        candidates = []

        for customer in list_customer:
            for vehicle_id, vehicle in enumerate(solution.vehicles):
                list_nodes = vehicle.nodes
                for position in range(1, len(list_nodes)):
                    solution.addNode(customer['point'], position, vehicle_id)
                    if vehicle.validateState() == True:
                        candidate = Candidate(solution.getTotalWeight(), position, vehicle_id)
                        candidates.append(candidate)
                    solution.removeNode(position, vehicle_id)

            if len(candidates) != 0:
                candidates.sort(key=lambda x : x.weight)
                chosen_custommer = candidates[0]
                solution.addNode(customer['point'], chosen_custommer.position, chosen_custommer.vehicle_id)
                candidates.clear()

            else:
                new_route = [depot,customer['point'], depot]
                new_vehicle = Vehicle(len(solution.vehicles), new_route, self.capacity)
                solution.vehicles.append(new_vehicle)

        if len(solution.vehicles) > self.number_vehicles:
            print(f'Can\'t create solution by gready method, the vehicle needed is {len(solution.vehicles)} ')
            return solution

        return solution
