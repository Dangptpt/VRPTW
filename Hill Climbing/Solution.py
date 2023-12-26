import random
from Candidate import Candidate
class Solution:
    def __init__(self, vehicles):
        self.vehicles = vehicles

    def addNode(self, p, position, vehicle_id):
        self.vehicles[vehicle_id].nodes.insert(position, p)

    def removeNode(self, position, vehicle_id):
        self.vehicles[vehicle_id].nodes.pop(position)

    def getTotalWeight(self) -> int:
        total = 0
        for vehicle in self.vehicles:
            total += vehicle.getWeight()

        return total

    def mutate(self):
        random_vehicle = random.randint(0, len(self.vehicles)-1)
        random_node = random.randint(1, len(self.vehicles[random_vehicle].nodes)-2)

        original_node = self.vehicles[random_vehicle].nodes[random_node]
        self.removeNode(random_node, random_vehicle)

        candidate = Candidate(self.getTotalWeight(), random_node, random_vehicle)

        for vehicle_id, vehicle in enumerate(self.vehicles):
            list_nodes = vehicle.nodes
            for position in range(1, len(list_nodes)):
                self.addNode(original_node, position, vehicle_id)

                if vehicle.validateState() == True:
                    current_weight = self.getTotalWeight()

                    if current_weight <= candidate.weight:
                        candidate.weight = current_weight
                        candidate.position = position
                        candidate.vehicle_id = vehicle_id

                self.removeNode(position, vehicle_id)

        self.addNode(original_node, candidate.position, candidate.vehicle_id)

        return candidate.weight

