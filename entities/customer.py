import math
import random
import simpy
from typing import List, Tuple

class Customer:
    """Represents a customer with a unique ID and location."""

    def __init__(self, customer_id: int, location: Tuple[float, float]):
        self.id = customer_id
        self.location = location
