import math
import random
import simpy
from typing import List, Tuple

from entities.delivery_hub import DeliveryHub
from entities.delivery_queue import DeliveryQueue
from processes.metrics_collector import MetricsCollector
from utils import calculate_travel_time

class Truck:
    """Represents a delivery truck."""

    def __init__(
        self,
        env: simpy.Environment,
        name: str,
        hub: DeliveryHub,
        delivery_queue: DeliveryQueue,
        metrics: MetricsCollector,
        capacity: int,
        speed: float,
        hub_location: Tuple[float, float],
    ):
        self.env = env
        self.name = name
        self.hub = hub
        self.delivery_queue = delivery_queue
        self.metrics = metrics
        self.capacity = capacity
        self.speed = speed  # km/h
        self.hub_location = hub_location
        self.action = env.process(self.run())

    def run(self):
        while True:
            # Request to load at the hub
            with self.hub.loading_docks.request() as request:
                yield request
                print(f"{self.name} starts loading at time {self.env.now:.2f}")
                yield self.env.timeout(self.hub.loading_time)
                print(f"{self.name} finished loading at time {self.env.now:.2f}")

            # Get deliveries assigned to this truck
            deliveries = self.delivery_queue.get_deliveries(self.capacity)
            if not deliveries:
                print(
                    f"{self.name} has no deliveries and is waiting at time {self.env.now:.2f}"
                )
                yield self.env.timeout(5)  # Wait before checking again
                continue

            # Start delivery route
            for delivery in deliveries:
                travel_time = calculate_travel_time(self.speed, delivery.distance)
                print(
                    f"{self.name} traveling to Customer {delivery.customer.id} at time {self.env.now:.2f}"
                )
                yield self.env.timeout(travel_time)
                print(
                    f"{self.name} delivered to Customer {delivery.customer.id} at time {self.env.now:.2f}"
                )
                delivery_time = self.env.now - delivery.order_time
                self.metrics.record_delivery(delivery, delivery_time)
                yield self.env.timeout(
                    delivery.service_time
                )  # Time spent at customer location

            # Return to hub
            # Assuming the truck returns directly from the last delivery location
            last_delivery = deliveries[-1]
            travel_time = calculate_travel_time(self.speed, last_delivery.distance)
            print(f"{self.name} returning to hub at time {self.env.now:.2f}")
            yield self.env.timeout(travel_time)
            print(f"{self.name} arrived at hub at time {self.env.now:.2f}")
