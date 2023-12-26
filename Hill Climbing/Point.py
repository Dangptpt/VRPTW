import math
class Point:
    def __init__(self, id, x, y, demand, ready_time, due_date, service_time):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.ready_time = ready_time
        self.due_date = due_date
        self.service_time = service_time

    def distance(self, point) -> float:
        return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)

