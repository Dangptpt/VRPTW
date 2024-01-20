import random
from Vehicle import Vehicle
from Candidate import Candidate
from Candidate import Candidate2
class Solution:
    def __init__(self, vehicles):
        self.vehicles = vehicles

    def addNode(self, p, position, vehicle_id):
        self.vehicles[vehicle_id].nodes.insert(position, p)

    def removeNode(self, position, vehicle_id):
        self.vehicles[vehicle_id].nodes.pop(position)

    def getTotalWeight(self):
        total = 0
        for vehicle in self.vehicles:
            total += vehicle.getWeight()

        return total

    def relocate(self):
        random_vehicle = random.randint(0, len(self.vehicles)-1)
        random_node = random.randint(1, len(self.vehicles[random_vehicle].nodes)-2)
        original_node = self.vehicles[random_vehicle].nodes[random_node]

        w = self.getTotalWeight()
        candidate = Candidate(w, random_node, random_vehicle)

        self.removeNode(random_node, random_vehicle)
        check = 0
        if len(self.vehicles[random_vehicle].nodes) == 2:
            check = 1
        for vehicle_id, vehicle in enumerate(self.vehicles):
            for position in range(1, len(vehicle.nodes)-1):
                self.addNode(original_node, position, vehicle_id)

                if vehicle.validateState() == True:
                    current_weight = self.getTotalWeight()
                    if current_weight < candidate.weight:
                        candidate.weight = current_weight
                        candidate.position = position
                        candidate.vehicle_id = vehicle_id

                self.removeNode(position, vehicle_id)

        self.addNode(original_node, candidate.position, candidate.vehicle_id)
        if check == 1:
            if w != candidate.weight:
                self.vehicles.pop(random_vehicle)

        return candidate.weight

    def exchangeInRoute(self):
        random_vehicle = random.randint(0, len(self.vehicles)-1)

        candidate = Candidate2(self.getTotalWeight(), 0, len(self.vehicles[random_vehicle].nodes)-1)

        for i, customer_1 in enumerate(self.vehicles[random_vehicle].nodes[1: -1]):
            for j, customer_2 in enumerate(self.vehicles[random_vehicle].nodes[1: -1]):
                id_1 = i + 1
                id_2 = j + 1
                if id_2 <= id_1:
                    continue

                self.removeNode(id_2, random_vehicle)
                self.addNode(customer_2, id_1, random_vehicle)
                self.removeNode(id_1+1, random_vehicle)
                self.addNode(customer_1, id_2, random_vehicle)

                if self.vehicles[random_vehicle].validateState() == True:
                    current_weight = self.getTotalWeight()
                    if current_weight < candidate.weight:
                        candidate.weight = current_weight
                        candidate.position1 = id_1
                        candidate.position2 = id_2

                self.removeNode(id_2, random_vehicle)
                self.addNode(customer_1, id_1, random_vehicle)
                self.removeNode(id_1 + 1, random_vehicle)
                self.addNode(customer_2, id_2, random_vehicle)


        customer_1 = self.vehicles[random_vehicle].nodes[candidate.position1]
        customer_2 = self.vehicles[random_vehicle].nodes[candidate.position2]

        self.removeNode(candidate.position2, random_vehicle)
        self.addNode(customer_2, candidate.position1, random_vehicle)
        self.removeNode(candidate.position1 + 1, random_vehicle)
        self.addNode(customer_1, candidate.position2, random_vehicle)

        return candidate.weight

    def exchangeCross(self):
        random_vehicle = random.randint(0, len(self.vehicles) - 1)
        random_node = random.randint(1, len(self.vehicles[random_vehicle].nodes) - 2)

        original_node = self.vehicles[random_vehicle].nodes[random_node]

        w = self.getTotalWeight()
        candidate = Candidate(w, random_node, random_vehicle)
        self.removeNode(random_node, random_vehicle)

        for vehicle_id, vehicle in enumerate(self.vehicles):
            if vehicle_id == random_vehicle:
                continue
            for i, customer in enumerate(vehicle.nodes[1:-1]):
                position = i + 1
                self.removeNode(position, vehicle_id)
                self.addNode(customer, random_node, random_vehicle)
                self.addNode(original_node, position, vehicle_id)

                if self.vehicles[vehicle_id].validateState() == True:
                    current_weight = self.getTotalWeight()
                    if current_weight < candidate.weight:
                        candidate.weight = current_weight
                        candidate.position = position
                        candidate.vehicle_id = vehicle_id

                self.removeNode(position, vehicle_id)
                self.removeNode(random_node, random_vehicle)
                self.addNode(customer, position, vehicle_id)

        if (w == candidate.weight):
            self.addNode(original_node, random_node, random_vehicle)
            return w

        self.addNode(self.vehicles[candidate.vehicle_id].nodes[candidate.position], random_node, random_vehicle)
        self.removeNode(candidate.position, candidate.vehicle_id)
        self.addNode(original_node, candidate.position, candidate.vehicle_id)

        return candidate.weight
    def move(self, depot, number_vehicles, capacity):
        if len(self.vehicles) >= number_vehicles:
            return 999999
        iterator = 0
        new_solution = self
        candidate = Candidate (self.getTotalWeight(), 0, 0)
        while (iterator < 50):
            iterator += 1
            random_vehicle = random.randint(0, len(self.vehicles) - 1)
            if (len(self.vehicles[random_vehicle].nodes) == 3):
                continue
            random_node = random.randint(1, len(self.vehicles[random_vehicle].nodes) - 2)

            original_node = new_solution.vehicles[random_vehicle].nodes[random_node]
            new_solution.removeNode(random_node, random_vehicle)
            new_route = [depot, original_node, depot]
            new_vehicle = Vehicle(len(self.vehicles), new_route, capacity)
            new_solution.vehicles.append(new_vehicle)
            current_weight = new_solution.getTotalWeight()

            if current_weight < candidate.weight:
                candidate.weight = current_weight
                candidate.position = random_node
                candidate.vehicle_id = random_vehicle

            new_solution.addNode(original_node, random_node, random_vehicle)
            new_solution.vehicles.pop()

        if candidate.position != 0:
            new_node = self.vehicles[candidate.vehicle_id].nodes[candidate.position]
            new_route = [depot, new_node, depot]
            self.removeNode(candidate.position, candidate.vehicle_id)
            new_vehicle = Vehicle(len(self.vehicles), new_route, capacity)
            self.vehicles.append(new_vehicle)
            return self.getTotalWeight()
        else:
            return 99999


    def move2(self, depot, number_vehicles, capacity):
        if len(self.vehicles) >= number_vehicles:
            return 999999
        iterator = 0
        new_solution = self
        candidate = Candidate (self.getTotalWeight(), 0, 0)

        random_vehicle = random.randint(0, len(self.vehicles) - 1)
        random_node = random.randint(1, len(self.vehicles[random_vehicle].nodes) - 2)

        original_node = new_solution.vehicles[random_vehicle].nodes[random_node]
        new_solution.removeNode(random_node, random_vehicle)
        new_route = [depot, original_node, depot]
        new_vehicle = Vehicle(len(self.vehicles), new_route, capacity)
        new_solution.vehicles.append(new_vehicle)
        current_weight = new_solution.getTotalWeight()
