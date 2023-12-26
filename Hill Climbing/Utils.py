from Point import Point
from Solution import Solution
from Vehicle import Vehicle
from Candidate import Candidate
import math
class Utils:
    def __init__(self, test):
        self.test = test
        data = ""
        with open('../Data/{}.txt'.format(test)) as file:
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
        degree_depot = math.atan2(depot.y, depot.x) * 180.0 / math.pi
        newDegree = 0
        for i in range (1, len(self.rows)):
            customer = self.rows[i]
            newDegree = math.atan2(customer.y, customer.x) * 180.0 / math.pi
            d = depot.distance(customer)
            w = d*-0.7 + 0.1*customer.due_date + 0,2*(newDegree-degree_depot)/360*d
            list_customer.append({'weight':w, 'point': customer})

        list_customer.sort(key=lambda x:x['weight'])

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
                candidates.sort(key = lambda x:x.weight)
                chosen_custommer = candidates[0]
                solution.addNode(customer['point'], chosen_custommer.position, chosen_custommer.vehicle_id)
                candidates.clear()

            else:
                new_route = [depot,customer['point'], depot]
                new_vehicle = Vehicle(len(solution.vehicles), new_route, self.capacity)
                solution.vehicles.append(new_vehicle)

        return solution
