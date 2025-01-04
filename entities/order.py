import math
import random
import simpy
from typing import List, Tuple

from entities.customer import Customer
from utils import calculate_distance

class Order:
    """Represents an order placed by a customer."""

    def __init__(
        self,
        order_id: int,
        customer: Customer,
        order_time: float,
        service_time: float,
        hub_location: Tuple[float, float],
    ):
        self.id = order_id
        self.customer = customer
        self.order_time = order_time
        self.service_time = service_time  # Time to handle delivery at customer location
        self.distance = calculate_distance(hub_location, customer.location)
