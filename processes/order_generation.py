import math
import random
import simpy
from typing import List, Tuple

from entities.customer import Customer
from entities.delivery_queue import DeliveryQueue
from entities.order import Order

class OrderGenerator:
    """Generates orders based on a specified arrival rate."""

    def __init__(
        self,
        env: simpy.Environment,
        delivery_queue: DeliveryQueue,
        hub_location: Tuple[float, float],
        order_rate: float,
    ):
        self.env = env
        self.delivery_queue = delivery_queue
        self.hub_location = hub_location
        self.order_rate = order_rate
        self.process = env.process(self.run())
        self.order_id = 0

    def run(self):
        while True:
            inter_arrival = random.expovariate(self.order_rate)
            yield self.env.timeout(inter_arrival)
            customer = self.generate_random_customer()
            service_time = random.uniform(5, 10)  # minutes
            order = Order(
                order_id=self.order_id,
                customer=customer,
                order_time=self.env.now,
                service_time=service_time,
                hub_location=self.hub_location,
            )
            print(
                f"Order {order.id} placed by Customer {customer.id} at {self.env.now:.2f}"
            )
            self.delivery_queue.add_order(order)
            self.order_id += 1

    def generate_random_customer(self) -> Customer:
        x = random.uniform(-5, 5)
        y = random.uniform(-5, 5)
        customer_id = random.randint(1000, 9999)
        return Customer(customer_id=customer_id, location=(x, y))
