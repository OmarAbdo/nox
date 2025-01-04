import math
import random
import simpy
from typing import List, Tuple

from entities.order import Order

class DeliveryQueue:
    """Manages the queue of pending orders awaiting delivery."""

    def __init__(self):
        self.queue: List[Order] = []

    def add_order(self, order: Order):
        self.queue.append(order)
        print(
            f"Order {order.id} added to the delivery queue at time {order.order_time:.2f}"
        )

    def get_deliveries(self, capacity: int) -> List[Order]:
        deliveries = self.queue[:capacity]
        self.queue = self.queue[capacity:]
        return deliveries
