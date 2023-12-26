class Vehicle:
    def __init__(self, id, nodes, capacity):
        self.id = id
        self.nodes = nodes
        self.capacity = capacity
    def validateState(self):
        w = 0
        # kiem tra rang buoc thoi gian
        current_time = 0
        for i in range(1, len(self.nodes)):
            # cap nhan thoi gian hien tai
            current_time += int(self.nodes[i].distance(self.nodes[i-1]))

            if current_time > self.nodes[i].due_date:
                return False

            if current_time < self.nodes[i].ready_time:
                current_time = self.nodes[i].ready_time

            current_time += self.nodes[i].service_time
            w += self.nodes[i].demand

        if w > self.capacity:
            return False

        return True

    def getWeight(self) -> int:
        distance = 0
        for i in range(1, len(self.nodes)):
            distance += self.nodes[i].distance(self.nodes[i - 1])
        return distance