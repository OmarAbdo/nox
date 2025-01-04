import math
import random
import simpy
from typing import List, Tuple


def calculate_distance(loc1: Tuple[float, float], loc2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points."""
    return math.hypot(loc1[0] - loc2[0], loc1[1] - loc2[1])


def calculate_travel_time(speed_kmh: float, distance_km: float) -> float:
    """Calculate travel time in minutes."""
    return (distance_km / speed_kmh) * 60  # Convert hours to minutes
