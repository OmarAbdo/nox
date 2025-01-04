import math
import random
import simpy
from typing import List, Tuple

class DeliveryHub:
    """Represents the delivery hub managing loading docks and dispatching trucks."""

    def __init__(
        self, env: simpy.Environment, num_loading_docks: int, loading_time: float
    ):
        self.env = env
        self.loading_docks = simpy.Resource(env, num_loading_docks)
        self.loading_time = loading_time  # Time to load a truck at the hub
