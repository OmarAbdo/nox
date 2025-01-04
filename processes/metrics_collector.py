import math
import random
import simpy
from typing import List, Tuple

from entities.order import Order

class MetricsCollector:
    """Collects and processes simulation metrics."""

    def __init__(self):
        self.delivery_times: List[float] = []
        self.total_deliveries: int = 0

    def record_delivery(self, order: Order, delivery_time: float):
        self.delivery_times.append(delivery_time)
        self.total_deliveries += 1

    def get_average_delivery_time(self) -> float:
        if not self.delivery_times:
            return 0.0
        return sum(self.delivery_times) / len(self.delivery_times)
